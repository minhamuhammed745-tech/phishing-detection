import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

def main():
    # File paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(BASE_DIR, "data", "dataset.parquet")
model_dir = os.path.join(BASE_DIR, "models")

os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "model.pkl")
encoder_path = os.path.join(model_dir, "label_encoder.pkl")
    
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.pkl")
    encoder_path = os.path.join(model_dir, "label_encoder.pkl")

    print(f"Loading data from {data_path}...")
    df = pd.read_parquet(data_path)
    print(f"Dataset loaded successfully with shape: {df.shape}")

    # Target column check
    target_column = 'status'
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    # Drop raw URL string column if present
    if 'url' in df.columns:
        df = df.drop(columns=['url'])

    # Separate features (X) and target (y)
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Handle missing values
    X = X.fillna(0)

    # Encode target labels ('legitimate'/'phishing' -> 0/1)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # ==========================================
    # 80:20 TRAIN-TEST SPLIT
    # ==========================================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, 
        test_size=0.20,      # Sets 20% for testing, leaving 80% for training
        random_state=42,     # Ensures reproducibility so you get the same split every time
        stratify=y_encoded   # Maintains the same proportion of phishing/legitimate in both sets
    )

    print(f"Training set shape: {X_train.shape} ({len(X_train)} samples)")
    print(f"Testing set shape: {X_test.shape} ({len(X_test)} samples)")

    # Train Model
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate model on the 20% test data
    print("\nEvaluating model on the 20% test set...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    # Save artifacts
    joblib.dump(model, model_path)
    joblib.dump(label_encoder, encoder_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()