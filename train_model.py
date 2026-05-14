# train_model.py — FIXED for your diabetes_data.csv

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

print("Loading your dataset...")
df = pd.read_csv("diabetes_data.csv")

print("Columns found:", df.columns.tolist())
print("Shape:", df.shape)

# These are YOUR 10 input features
features = [
    'weight', 'height', 'blood_glucose', 'physical_activity',
    'diet', 'medication_adherence', 'stress_level',
    'sleep_hours', 'hydration_level', 'bmi'
]

# This is what we want to predict
target = 'risk_score'

X = df[features]
y = df[target]

print(f"\nUsing {len(features)} features: {features}")
print(f"Predicting: {target}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
accuracy = r2 * 100

print(f"✅ Mean Absolute Error: {mae:.2f}")
print(f"✅ R2 Score: {r2:.2f} (closer to 1.0 is better)")
print(f"✅ Accuracy: {accuracy:.2f}%")

joblib.dump(model, "model.pkl")
joblib.dump(features, "features.pkl")  # Save feature list too
print("\n✅ model.pkl saved!")
print("✅ features.pkl saved!")
print("\nNow run: streamlit run app.py")