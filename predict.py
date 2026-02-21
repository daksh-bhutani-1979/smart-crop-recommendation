# ===================================================================
# CROP RECOMMENDATION MODEL - PREDICTION SCRIPT
# ===================================================================

import pandas as pd
import joblib
import numpy as np

print("🔮 CROP RECOMMENDATION - PREDICTION ON NEW DATA")
print("=" * 50)

# ===================================================================
# 1. LOAD TRAINED MODEL AND ENCODER
# ===================================================================

print("📦 Loading trained model and label encoder...")

try:
    # Load the trained model
    model = joblib.load('rf_crop_model.pkl')
    print("✅ Model loaded successfully!")
    
    # Load the label encoder
    label_encoder = joblib.load('label_encoder.pkl')
    print("✅ Label encoder loaded successfully!")
    
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("🔧 Make sure you have run the training script first to generate the .pkl files")
    exit()

# ===================================================================
# 2. LOAD NEW UNLABELED DATA
# ===================================================================

print("\n📁 Loading unlabeled data...")

try:
    # Load the unlabeled dataset
    new_data = pd.read_csv('unlabeled_data.csv')
    print(f"✅ Unlabeled data loaded successfully!")
    print(f"📊 Data shape: {new_data.shape}")
    
except FileNotFoundError:
    print("❌ Error: 'unlabeled_data.csv' not found!")
    print("📝 Creating sample unlabeled data for demonstration...")
    
    # Create sample data if file doesn't exist
    sample_data = {
        'N': [90, 70, 40, 100, 60],
        'P': [40, 60, 30, 40, 55],
        'K': [40, 55, 50, 35, 60],
        'temperature': [25.5, 22.0, 20.0, 27.0, 26.0],
        'humidity': [80, 65, 70, 85, 78],
        'ph': [6.5, 6.3, 6.7, 6.2, 6.1],
        'rainfall': [200, 140, 120, 250, 160]
    }
    
    new_data = pd.DataFrame(sample_data)
    new_data.to_csv('unlabeled_data.csv', index=False)
    print("✅ Sample unlabeled data created and saved as 'unlabeled_data.csv'")

# ===================================================================
# 3. VALIDATE INPUT DATA
# ===================================================================

print("\n🔍 Validating input data...")

# Expected column names
expected_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

# Check if all required columns are present
if list(new_data.columns) != expected_columns:
    print(f"❌ Column mismatch!")
    print(f"   Expected: {expected_columns}")
    print(f"   Found: {list(new_data.columns)}")
    exit()

print("✅ Column validation passed!")

# Check for missing values
if new_data.isnull().sum().sum() > 0:
    print("⚠️ Warning: Missing values detected!")
    print(new_data.isnull().sum())
else:
    print("✅ No missing values found!")

print(f"📋 Data preview:")
print(new_data.head())

# ===================================================================
# 4. MAKE PREDICTIONS
# ===================================================================

print("\n🤖 Making predictions...")

# Predict using the trained model
predictions = model.predict(new_data)

# Convert predictions back to crop names
predicted_crops = label_encoder.inverse_transform(predictions)

# Add predictions to the dataframe
new_data['Predicted Crop'] = predicted_crops

print("✅ Predictions completed!")

# ===================================================================
# 5. DISPLAY AND SAVE RESULTS
# ===================================================================

print("\n📊 PREDICTION RESULTS:")
print("=" * 50)

# Display first few predictions
print(new_data.head(10))

# Save results to CSV
output_filename = 'predicted_output.csv'
new_data.to_csv(output_filename, index=False)
print(f"\n💾 Results saved to '{output_filename}'")

# Summary statistics
print(f"\n📈 PREDICTION SUMMARY:")
print(f"   Total predictions made: {len(new_data)}")
print(f"   Unique crops predicted: {new_data['Predicted Crop'].nunique()}")
print(f"\n🌾 Crop distribution in predictions:")
crop_counts = new_data['Predicted Crop'].value_counts()
for crop, count in crop_counts.items():
    print(f"   {crop}: {count} ({count/len(new_data)*100:.1f}%)")

print(f"\n🎉 PREDICTION COMPLETED SUCCESSFULLY!")
print("=" * 50)