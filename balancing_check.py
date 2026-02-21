import pandas as pd

# Dataset load करें
df = pd.read_csv('Crop_recommendation.csv')

# Actual distribution देखें
print("🎯 Actual Crop Distribution:")
crop_counts = df['label'].value_counts()
print(crop_counts)

print(f"\n📊 Stats:")
print(f"Total samples: {len(df)}")
print(f"Number of crops: {df['label'].nunique()}")
print(f"Average per crop: {len(df) / df['label'].nunique():.1f}")
print(f"Min samples: {crop_counts.min()}")
print(f"Max samples: {crop_counts.max()}")

# Imbalance check
if crop_counts.max() / crop_counts.min() > 2:
    print("⚠️ Dataset is imbalanced!")
else:
    print("✅ Dataset is well balanced!")