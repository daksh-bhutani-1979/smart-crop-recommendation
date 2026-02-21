# ===================================================================
# CROP RECOMMENDATION MODEL - COMPLETE TRAINING PIPELINE
# ===================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

print("🌾 CROP RECOMMENDATION MODEL - TRAINING PIPELINE")
print("=" * 60)

# ===================================================================
# 1. DATA LOADING & PREPROCESSING
# ===================================================================

print("\n📁 Step 1: Loading and exploring dataset...")

# Load the dataset
df = pd.read_csv('data/Crop_recommendation.csv')

# Basic dataset information
print(f"✅ Dataset loaded successfully!")
print(f"📊 Dataset shape: {df.shape}")
print(f"📋 Dataset info:")
print(df.info())

print(f"\n🔍 Missing values:")
print(df.isnull().sum())

print(f"\n📈 Dataset description:")
print(df.describe())

print(f"\n🎯 Target variable distribution:")
print(df['label'].value_counts())

print(f"\n🔢 Number of unique crops: {df['label'].nunique()}")

# Optional: Correlation heatmap
plt.figure(figsize=(10, 8))
correlation_matrix = df.drop('label', axis=1).corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig('outputs/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("📊 Correlation heatmap saved as 'correlation_heatmap.png'")

# ===================================================================
# 2. DATA SPLITTING
# ===================================================================

print("\n✂️ Step 2: Splitting dataset...")

# Separate features and target
X = df.drop('label', axis=1)
y = df['label']

# Encode target variable
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"🔤 Label encoding completed. Classes: {len(label_encoder.classes_)}")

# First split: separate test set (20%)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y_encoded, 
    test_size=0.20, 
    stratify=y_encoded, 
    random_state=42
)

# Second split: divide remaining into train (60%) and validation (20%)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, 
    test_size=0.25,  # 0.25 of 80% = 20% of total
    stratify=y_temp, 
    random_state=42
)

print(f"📊 Data split completed:")
print(f"   🔹 Training set:   {X_train.shape[0]} samples ({X_train.shape[0]/len(df)*100:.1f}%)")
print(f"   🔹 Validation set: {X_val.shape[0]} samples ({X_val.shape[0]/len(df)*100:.1f}%)")
print(f"   🔹 Test set:       {X_test.shape[0]} samples ({X_test.shape[0]/len(df)*100:.1f}%)")

# ===================================================================
# 3. MODEL TRAINING
# ===================================================================

print("\n🤖 Step 3: Training Random Forest model...")

# Initialize Random Forest with specified parameters
rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# Train the model on training data only
rf_model.fit(X_train, y_train)
print("✅ Model training completed!")

# ===================================================================
# 4. MODEL EVALUATION
# ===================================================================

print("\n📊 Step 4: Model evaluation...")

# Cross-validation on training set
cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring='accuracy')
print(f"🔄 Cross-validation scores: {cv_scores}")
print(f"🎯 Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# Validation set evaluation
val_predictions = rf_model.predict(X_val)
val_accuracy = accuracy_score(y_val, val_predictions)

print(f"\n🧪 VALIDATION SET RESULTS:")
print(f"📈 Validation Accuracy: {val_accuracy:.4f}")
print("\n📋 Validation Classification Report:")
print(classification_report(y_val, val_predictions, target_names=label_encoder.classes_))

# Test set evaluation (final holdout)
test_predictions = rf_model.predict(X_test)
test_accuracy = accuracy_score(y_test, test_predictions)

print(f"\n🎯 FINAL TEST SET RESULTS:")
print(f"📈 Test Accuracy: {test_accuracy:.4f}")
print("\n📋 Test Classification Report:")
print(classification_report(y_test, test_predictions, target_names=label_encoder.classes_))

# ===================================================================
# 5. VISUALIZATION & ANALYSIS
# ===================================================================

print("\n📊 Step 5: Generating visualizations...")

# Confusion Matrix
plt.figure(figsize=(12, 10))
cm = confusion_matrix(y_test, test_predictions)
sns.heatmap(cm, 
            xticklabels=label_encoder.classes_, 
            yticklabels=label_encoder.classes_,
            annot=False, 
            cmap='Blues',
            fmt='d')
plt.title('Confusion Matrix - Test Set')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('outputs/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("📊 Confusion matrix saved as 'confusion_matrix.png'")

# Feature Importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance, x='importance', y='feature', palette='viridis')
plt.title('Feature Importance - Random Forest')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('outputs/feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("📊 Feature importance chart saved as 'feature_importance.png'")

print("\n🔍 Feature Importance Ranking:")
for idx, row in feature_importance.iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# ===================================================================
# 6. MODEL SAVING
# ===================================================================

print("\n💾 Step 6: Saving model and encoder...")

# Save the trained model
joblib.dump(rf_model, 'outputs/rf_crop_model.pkl')
print("✅ Model saved as 'rf_crop_model.pkl'")

# Save the label encoder
joblib.dump(label_encoder, 'outputs/label_encoder.pkl')
print("✅ Label encoder saved as 'label_encoder.pkl'")

# ===================================================================
# 7. SAMPLE PREDICTION TEST
# ===================================================================

print("\n🧪 Step 7: Testing sample prediction...")

# Test with a sample input
sample_input = np.array([[90, 40, 40, 25, 80, 6.5, 200]])  # N, P, K, temp, humidity, ph, rainfall
sample_prediction = rf_model.predict(sample_input)
sample_crop = label_encoder.inverse_transform(sample_prediction)[0]

print(f"🌱 Sample prediction test:")
print(f"   Input: N=90, P=40, K=40, temp=25°C, humidity=80%, pH=6.5, rainfall=200mm")
print(f"   Predicted crop: {sample_crop}")

print("\n🎉 MODEL TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("📁 Generated files:")
print("   • rf_crop_model.pkl (trained model)")
print("   • label_encoder.pkl (label encoder)")
print("   • confusion_matrix.png (evaluation plot)")
print("   • feature_importance.png (analysis plot)")
print("   • correlation_heatmap.png (data analysis)")