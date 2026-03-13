"""Entry point for the governed autonomous AI scientist system."""

from __future__ import annotations

import logging
from pathlib import Path

from ai_scientist_system.agents.analyst_agent import AnalystAgent
from ai_scientist_system.agents.critic_agent import CriticAgent
from ai_scientist_system.agents.literature_agent import LiteratureAgent
from ai_scientist_system.agents.paper_writer_agent import PaperWriterAgent
from ai_scientist_system.agents.planner_agent import PlannerAgent
from ai_scientist_system.agents.scientist_agent import ScientistAgent
from ai_scientist_system.config.settings import load_settings
from ai_scientist_system.core.checkpoint_manager import CheckpointManager
from ai_scientist_system.core.dataset_loader import DatasetLoader
from ai_scientist_system.core.evaluator import Evaluator
from ai_scientist_system.core.experiment_optimizer import ExperimentOptimizer
from ai_scientist_system.core.experiment_queue import ExperimentQueue
from ai_scientist_system.core.experiment_runner import ExperimentRunner
from ai_scientist_system.core.gemini_client import GeminiClient
from ai_scientist_system.core.governance import ExperimentGovernance, GovernanceViolation
from ai_scientist_system.memory.leaderboard import Leaderboard
from ai_scientist_system.memory.research_graph import ResearchGraph
from ai_scientist_system.memory.research_memory import ResearchMemory
from ai_scientist_system.reports.dashboard_generator import generate_dashboard_html
from ai_scientist_system.reports.report_generator import ReportGenerator
from ai_scientist_system.reports.visualization import (
    save_feature_importance_plot,
    save_leaderboard_plot,
    save_metrics_comparison_plot,
)
from ai_scientist_system.statistics.hypothesis_validator import StatisticalValidator
from ai_scientist_system.utils.logging_utils import configure_logging
from ai_scientist_system.utils.reproducibility_utils import attach_reproducibility_metadata

logger = logging.getLogger(__name__)


def run(goal: str = "discover predictive signals in dataset") -> None:
    settings = load_settings()
    configure_logging(settings.runtime.log_dir)

    dataset_loader = DatasetLoader(settings.data)
    datasets = dataset_loader.load_datasets()

    llm = GeminiClient(settings.gemini_keys, settings.gemini_model_name)
    literature_agent = LiteratureAgent(llm)
    planner_agent = PlannerAgent(llm)
    scientist_agent = ScientistAgent(settings.models, settings.novelty)
    critic_agent = CriticAgent()
    analyst_agent = AnalystAgent()
    paper_writer = PaperWriterAgent(llm)

    optimizer = ExperimentOptimizer(settings.models)
    queue = ExperimentQueue()
    runner = ExperimentRunner(dataset_loader, datasets)
    evaluator = Evaluator()
    stats_validator = StatisticalValidator(
        alpha=settings.statistics.alpha,
        correction_method=settings.statistics.correction_method,
    )
    governance = ExperimentGovernance(settings.budget)

    memory = ResearchMemory()
    graph = ResearchGraph.create()
    leaderboard = Leaderboard()
    reports = ReportGenerator(settings.runtime.report_dir)
    checkpoint = CheckpointManager(settings.runtime.checkpoint_dir)

    literature_summary = literature_agent.summarize(goal)
    governance.record_api_usage(llm.usage.total_calls, llm.usage.estimated_cost_usd)

    for iteration in range(settings.runtime.max_iterations):
        logger.info("Iteration %s started", iteration)
        direction = planner_agent.plan(goal, literature_summary)
        governance.record_api_usage(llm.usage.total_calls - governance.tracker.api_calls, llm.usage.estimated_cost_usd - governance.tracker.api_cost_usd)

        hypotheses = scientist_agent.generate_hypotheses(direction)
        filtered_hypotheses = scientist_agent.novelty_filter(hypotheses, memory.all_hypotheses())
        candidate_experiments = scientist_agent.design_experiments(
            filtered_hypotheses,
            dataset_loader.feature_columns(datasets.train),
        )

        for experiment in candidate_experiments:
            attach_reproducibility_metadata(experiment, datasets.dataset_hash)

        optimized_experiments = optimizer.optimize(candidate_experiments)
        validated_experiments = governance.validate_batch(optimized_experiments)
        queue.extend(validated_experiments)

        while len(queue) > 0:
            experiment = queue.pop()
            try:
                governance.check_budget()
            except GovernanceViolation:
                logger.warning("Stopping execution: budget exceeded")
                break

            result = runner.run(experiment)
            evaluation = evaluator.evaluate(result)

            baseline_scores = [0.5] * 30
            candidate_scores = [result.metrics["f1"]] * 30
            validation = stats_validator.validate(candidate_scores, baseline_scores)

            result.p_value = validation.p_value
            result.passed_statistics = bool(validation.valid and validation.p_value < 0.05)

            if evaluation.passed and result.passed_statistics:
                critic_feedback = critic_agent.review(experiment, result)
                memory.store(experiment, result, critic_feedback)
                graph.update_from_experiment(experiment, result)
                leaderboard.update(result)

            governance.record_experiment_completion(result.runtime_seconds)

        patterns = analyst_agent.analyze(memory)

        if iteration % 10 == 0:
            reports.generate(iteration, memory, leaderboard, patterns)
            draft = paper_writer.write(goal, memory)
            draft_path = settings.runtime.report_dir / f"paper_draft_{iteration:04d}.md"
            draft_path.write_text(draft)
            governance.record_api_usage(
                llm.usage.total_calls - governance.tracker.api_calls,
                llm.usage.estimated_cost_usd - governance.tracker.api_cost_usd,
            )

        leaderboard.save(settings.runtime.leaderboard_path)
        save_leaderboard_plot(
            leaderboard,
            settings.runtime.report_dir / f"leaderboard_{iteration:04d}.png",
        )

        if len(leaderboard.entries) > 0:
            save_metrics_comparison_plot(
                leaderboard,
                settings.runtime.report_dir / f"metrics_comparison_{iteration:04d}.png",
            )

            top_entry = leaderboard.top(1)[0]
            if top_entry.experiment_id in [e.experiment["experiment_id"] for e in memory.entries]:
                matching_entry = next(
                    e for e in memory.entries
                    if e.experiment["experiment_id"] == top_entry.experiment_id
                )
                save_feature_importance_plot(
                    matching_entry.result["feature_importance"],
                    settings.runtime.report_dir / f"feature_importance_{iteration:04d}.png",
                )

        generate_dashboard_html(
            iteration=iteration,
            memory=memory,
            leaderboard=leaderboard,
            patterns=patterns,
            budget_snapshot=governance.budget_snapshot(),
            report_dir=settings.runtime.report_dir,
        )

        checkpoint.save(
            iteration=iteration,
            queue_snapshot=queue.to_dict(),
            memory_snapshot=memory.snapshot(),
            leaderboard_snapshot=leaderboard.snapshot(),
            graph_snapshot=graph.snapshot(),
            budget_snapshot=governance.budget_snapshot(),
        )

        if governance.tracker.experiments_run >= settings.budget.max_experiments:
            logger.warning("Terminating loop due to max experiments cap")
            break

    logger.info("Research run complete. Experiments retained: %s", len(memory.entries))


def _ensure_data_placeholder() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)


if __name__ == "__main__":
    _ensure_data_placeholder()
    run()
