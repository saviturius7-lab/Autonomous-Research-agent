"""Generate sample dataset for testing the AI scientist system."""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_classification_dataset(n_samples: int, n_features: int, random_state: int = 42):
    np.random.seed(random_state)

    feature_names = [f"feature_{i}" for i in range(n_features)]

    X = np.random.randn(n_samples, n_features)

    coefficients = np.random.randn(n_features) * 0.5
    logits = X @ coefficients + np.random.randn(n_samples) * 0.3
    probabilities = 1 / (1 + np.exp(-logits))
    y = (probabilities > 0.5).astype(int)

    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    return df


def main():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    n_features = 20
    train_df = generate_classification_dataset(1000, n_features, random_state=42)
    validation_df = generate_classification_dataset(300, n_features, random_state=43)
    holdout_df = generate_classification_dataset(200, n_features, random_state=44)

    train_df.to_csv(data_dir / "train.csv", index=False)
    validation_df.to_csv(data_dir / "validation.csv", index=False)
    holdout_df.to_csv(data_dir / "holdout.csv", index=False)

    print(f"Generated datasets:")
    print(f"  Train: {len(train_df)} samples")
    print(f"  Validation: {len(validation_df)} samples")
    print(f"  Holdout: {len(holdout_df)} samples")
    print(f"  Features: {n_features}")
    print(f"\nFiles saved to {data_dir}/")


if __name__ == "__main__":
    main()
