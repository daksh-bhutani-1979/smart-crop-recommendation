# ===================================================================
# SAMPLE UNLABELED DATA GENERATOR
# ===================================================================

import pandas as pd
import numpy as np

print("📝 Creating sample unlabeled data for testing...")

# Generate realistic sample data
np.random.seed(42)

sample_data = {
    'N': np.random.randint(20, 140, 50),
    'P': np.random.randint(5, 145, 50),
    'K': np.random.randint(5, 205, 50),
    'temperature': np.round(np.random.uniform(8, 44, 50), 1),
    'humidity': np.round(np.random.uniform(14, 100, 50), 1),
    'ph': np.round(np.random.uniform(3.5, 10, 50), 2),
    'rainfall': np.round(np.random.uniform(20, 300, 50), 1)
}

df = pd.DataFrame(sample_data)
df.to_csv('unlabeled_data.csv', index=False)

print("✅ Sample unlabeled data created!")
print(f"📊 Generated {len(df)} samples")
print("📁 Saved as 'unlabeled_data.csv'")
print("\nFirst 5 rows:")
print(df.head())