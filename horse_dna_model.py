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
np.random.seed(42)  # For reproducibility
n_rows = 100

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

df = pd.DataFrame(data)

# Save dataset to CSV
DATASET_PATH = 'horse_dna_dataset.csv'
df.to_csv(DATASET_PATH, index=False)
print(f"Dataset saved to {DATASET_PATH}")

# ----------------------------
# 2. Prepare data for modeling
# ----------------------------
SNP_COLS = [f'SNP{i}' for i in range(1, 6)]
X = df[SNP_COLS]
y = df['Performance']

# Train-test split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Pipeline: One-hot encode SNP columns then fit RandomForest
preprocess = ColumnTransformer(
    [('ohe', OneHotEncoder(handle_unknown='ignore'), SNP_COLS)],
    remainder='drop'
)

pipeline = Pipeline(
    steps=[
        ('preprocess', preprocess),
        ('model', RandomForestClassifier(n_estimators=200, random_state=42))
    ]
)

# Fit the model
pipeline.fit(X_train, y_train)

# Predict on the test set
y_pred = pipeline.predict(X_test)

# ----------------------------
# 3. Evaluation metrics
# ----------------------------

# Classification report
report_dict = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
REPORT_PATH = 'classification_report.csv'
report_df.to_csv(REPORT_PATH)
print(f"Classification report saved to {REPORT_PATH}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=['High', 'Low'])
cm_df = pd.DataFrame(
    cm,
    index=['Actual High', 'Actual Low'],
    columns=['Predicted High', 'Predicted Low']
)
CM_PATH = 'confusion_matrix.csv'
cm_df.to_csv(CM_PATH)
print(f"Confusion matrix saved to {CM_PATH}")

# Feature importances
# Get feature names after one-hot encoding
ohe = pipeline.named_steps['preprocess'].named_transformers_['ohe']
feature_names = ohe.get_feature_names_out(SNP_COLS)
importances = pipeline.named_steps['model'].feature_importances_

feat_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
feat_df.sort_values(by='importance', ascending=False, inplace=True)
FI_PATH = 'feature_importances.csv'
feat_df.to_csv(FI_PATH, index=False)
print(f"Feature importances saved to {FI_PATH}")

# Print top-10 most important features
print("\nTop 10 feature importances:")
print(feat_df.head(10))

if __name__ == '__main__':
    # This allows the script to be run directly
    pass
