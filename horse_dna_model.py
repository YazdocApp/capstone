"""Simulate horse DNA data and train a RandomForest model.

Running this script will create a synthetic dataset, train a classifier,
and save several evaluation files.  Only pandas and scikit-learn are
required; NumPy comes as a dependency of scikit-learn.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# ----------------------------
# 1. Simulate the horse DNA dataset
# ----------------------------
def simulate_dataset(n_rows: int = 100) -> pd.DataFrame:
    """Create a synthetic horse DNA dataset."""

    np.random.seed(42)  # For reproducible results

    # Possible values for each column
    snp_options = ['AA', 'AG', 'GG', 'CC', 'CT', 'TT']
    performance_options = ['High', 'Low']
    coat_colors = ['Bay', 'Chestnut', 'Black', 'Grey']
    temperaments = ['Calm', 'Hot-blooded']

    # Generate random data for each column
    data = {
        f'SNP{i}': np.random.choice(snp_options, size=n_rows)
        for i in range(1, 6)
    }
    # Additional non-SNP columns
    data['Performance'] = np.random.choice(performance_options, size=n_rows)
    data['CoatColor'] = np.random.choice(coat_colors, size=n_rows)
    data['Temperament'] = np.random.choice(temperaments, size=n_rows)

    return pd.DataFrame(data)


def save_dataframe(df: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to CSV and confirm to the user."""

    df.to_csv(path, index=False)
    print(f"Dataset saved to {path}")


def build_pipeline(snp_cols: list[str]) -> Pipeline:
    """Create a preprocessing and modeling pipeline."""

    preprocess = ColumnTransformer(
        [('ohe', OneHotEncoder(handle_unknown='ignore'), snp_cols)],
        remainder='drop',
    )

    return Pipeline([
        ('preprocess', preprocess),
        ('model', RandomForestClassifier(n_estimators=200, random_state=42)),
    ])


def evaluate_model(pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the model and save relevant files."""

    y_pred = pipeline.predict(X_test)

    # Classification report
    report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
    REPORT_PATH = 'classification_report.csv'
    report_df.to_csv(REPORT_PATH)
    print(f"Classification report saved to {REPORT_PATH}")

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=['High', 'Low'])
    cm_df = pd.DataFrame(
        cm,
        index=['Actual High', 'Actual Low'],
        columns=['Predicted High', 'Predicted Low'],
    )
    CM_PATH = 'confusion_matrix.csv'
    cm_df.to_csv(CM_PATH)
    print(f"Confusion matrix saved to {CM_PATH}")

    # Feature importances
    ohe = pipeline.named_steps['preprocess'].named_transformers_['ohe']
    feature_names = ohe.get_feature_names_out(snp_cols)
    importances = pipeline.named_steps['model'].feature_importances_
    feat_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
    feat_df.sort_values(by='importance', ascending=False, inplace=True)
    FI_PATH = 'feature_importances.csv'
    feat_df.to_csv(FI_PATH, index=False)
    print(f"Feature importances saved to {FI_PATH}")

    # Print top-10 most important features
    print("\nTop 10 feature importances:")
    print(feat_df.head(10))


def main() -> None:
    """Run the full data simulation, training, and evaluation pipeline."""

    df = simulate_dataset()
    save_dataframe(df, 'horse_dna_dataset.csv')

    snp_cols = [f'SNP{i}' for i in range(1, 6)]
    X = df[snp_cols]
    y = df['Performance']

    # Train-test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pipeline = build_pipeline(snp_cols)
    pipeline.fit(X_train, y_train)

    evaluate_model(pipeline, X_test, y_test)


if __name__ == '__main__':
    main()
