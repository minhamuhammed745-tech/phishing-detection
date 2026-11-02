import joblib
le = joblib.load('models/label_encoder.pkl')
model = joblib.load('models/model.pkl')
print("Classes:", le.classes_)
print("0 ->", le.inverse_transform([0])[0])
print("1 ->", le.inverse_transform([1])[0])
print("Model OK:", type(model))

# Test google.com features
import sys
sys.path.insert(0, '.')
from app import extract_features
f = extract_features("https://google.com")
print(f.T.head(20))
print("Prediction for google.com:", le.inverse_transform(model.predict(f))[0])