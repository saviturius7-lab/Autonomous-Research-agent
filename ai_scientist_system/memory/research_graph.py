"""NetworkX knowledge graph of hypotheses, experiments, features and models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

import networkx as nx

from ai_scientist_system.experiments.experiment_schema import Experiment, ExperimentResult


@dataclass
class ResearchGraph:
    graph: nx.MultiDiGraph

    @classmethod
    def create(cls) -> "ResearchGraph":
        return cls(graph=nx.MultiDiGraph())

    def update_from_experiment(self, experiment: Experiment, result: ExperimentResult) -> None:
        h_node = f"hypothesis::{experiment.hypothesis_text}"
        e_node = f"experiment::{experiment.experiment_id}"
        m_node = f"model::{experiment.model_name}"

        self.graph.add_node(h_node, type="hypothesis")
        self.graph.add_node(e_node, type="experiment", score=result.metrics.get("f1", 0.0))
        self.graph.add_node(m_node, type="model")

        self.graph.add_edge(h_node, e_node, relation="tested_with")
        self.graph.add_edge(e_node, m_node, relation="supports")

        for feature in experiment.feature_set:
            f_node = f"feature::{feature}"
            self.graph.add_node(f_node, type="feature")
            self.graph.add_edge(e_node, f_node, relation="tested_with")
            if result.feature_importance.get(feature, 0.0) > 0.0:
                self.graph.add_edge(f_node, e_node, relation="improves")

    def snapshot(self) -> Dict:
        data = nx.node_link_data(self.graph)
        return data

    def feature_clusters(self) -> Dict[str, int]:
        undirected = self.graph.to_undirected()
        clusters = nx.connected_components(undirected)
        mapping = {}
        for i, component in enumerate(clusters):
            for node in component:
                mapping[node] = i
        return mapping
