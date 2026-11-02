import os
import pandas as pd
import joblib

def interactive_prediction():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "models", "model.pkl")
encoder_path = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
data_path = os.path.join(BASE_DIR, "data", "dataset.parquet")
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
    print("Model artifacts not found! Please run train.py first.")
    return

    # Load model, encoder, and dataset for reference
    model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)
    df = pd.read_parquet(data_path)
    
    expected_features = model.feature_names_in_

    print("="*50)
    print(" PHISHING DETECTION AI - INTERACTIVE TESTER")
    print("="*50)
    print("Options:")
    print("1. Test a random sample from the dataset")
    print("2. Test by entering custom feature values (JSON format)")
    
    choice = input("\nSelect an option (1 or 2): ").strip()
    
    if choice == '1':
        # Pick a random row from the dataset to test
        sample_row = df.sample(n=1)
        actual_status = sample_row['status'].values[0] if 'status' in sample_row.columns else "Unknown"
        
        # Prepare features
        X_sample = sample_row.drop(columns=['status', 'url'], errors='ignore')
        X_sample = X_sample.fillna(0)
        
        # Predict
        numeric_pred = model.predict(X_sample)
        probabilities = model.predict_proba(X_sample)
        text_pred = label_encoder.inverse_transform(numeric_pred)[0]
        confidence = max(probabilities[0]) * 100
        
        print("\n--- Random Sample Results ---")
        print(f"Actual Status in Dataset : {actual_status.upper()}")
        print(f"AI Prediction            : {text_pred.upper()}")
        print(f"Confidence               : {confidence:.2f}%")
        
    elif choice == '2':
        print("\nEnter custom values for key features (or press Enter to use defaults):")
        
        # Example interactive prompts for key phishing indicators
        try:
            length_url = int(input("Enter URL length (e.g., 25): ") or 25)
            nb_dots = int(input("Enter number of dots '.' (e.g., 1): ") or 1)
            nb_hyphens = int(input("Enter number of hyphens '-' (e.g., 0): ") or 0)
            ip_used = int(input("Is an IP address used instead of domain? (0 for No, 1 for Yes): ") or 0)
            login_form = int(input("Does it contain a login form? (0 for No, 1 for Yes): ") or 0)
            iframe = int(input("Does it contain an iframe? (0 for No, 1 for Yes): ") or 0)
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            return

        # Build a feature dictionary matching training structure, defaulting others to 0
        custom_data = {col: 0 for col in expected_features}
        custom_data.update({
            "length_url": length_url,
            "nb_dots": nb_dots,
            "nb_hyphens": nb_hyphens,
            "ip": ip_used,
            "login_form": login_form,
            "iframe": iframe
        })

        df_custom = pd.DataFrame([custom_data])
        df_custom = df_custom[expected_features].fillna(0)

        # Predict
        numeric_pred = model.predict(df_custom)
        probabilities = model.predict_proba(df_custom)
        text_pred = label_encoder.inverse_transform(numeric_pred)[0]
        confidence = max(probabilities[0]) * 100

        print("\n--- Custom Input Results ---")
        print(f"AI Prediction : {text_pred.upper()}")
        print(f"Confidence    : {confidence:.2f}%")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    interactive_prediction()