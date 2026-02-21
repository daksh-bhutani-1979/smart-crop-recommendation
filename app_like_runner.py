import joblib
import os
from farmer_input_mapper import map_farmer_answers_to_features

def get_crop_explanation(crop_name, confidence):
    """Generate a generic explanation based on crop characteristics."""
    explanations = {
        "rice": "Thrives in warm, humid conditions with high rainfall. Requires rich soil with good water retention.",
        "wheat": "Prefers cool temperatures and moderate rainfall. Grows well in loamy soils with balanced nutrients.",
        "maize": "Adaptable to warm climates with moderate rainfall. Tolerates various soil types but needs adequate nutrients.",
        "cotton": "Requires warm temperatures and moderate humidity. Prefers well-drained soils with good sunlight.",
        "sugarcane": "Needs hot, humid climate with high rainfall. Grows best in fertile, well-irrigated soils.",
        "coffee": "Thrives in cool, humid mountain climates. Requires well-drained, acidic soils with shade.",
        "tea": "Prefers cool, humid conditions with acidic soils. Needs consistent rainfall and good drainage.",
        "banana": "Requires warm, humid climate with rich, well-drained soil. Needs consistent moisture.",
        "apple": "Prefers cool temperatures and moderate humidity. Grows well in well-drained, loamy soils.",
        "grapes": "Adaptable to warm, dry climates. Prefers well-drained soils with moderate fertility.",
        "orange": "Needs warm temperatures and moderate humidity. Prefers slightly acidic, well-drained soils.",
        "mango": "Thrives in hot, dry to moderately humid conditions. Adaptable to various soil types.",
        "coconut": "Requires hot, humid coastal climate. Grows in sandy to loamy soils with good drainage.",
        "papaya": "Prefers warm, humid conditions with well-drained soil. Fast-growing in rich soils.",
        "pomegranate": "Adaptable to dry, warm climates. Prefers well-drained soils with moderate fertility.",
        "tomato": "Requires warm temperatures and moderate humidity. Grows best in rich, well-drained soils.",
        "potato": "Prefers cool temperatures and moderate humidity. Needs well-drained, loose soils.",
        "onion": "Adaptable to various climates but prefers moderate temperatures. Needs well-drained soils.",
        "garlic": "Requires cool to moderate temperatures with low humidity. Prefers well-drained, fertile soils.",
        "beans": "Adaptable to various climates. Prefers well-drained soils with moderate fertility."
    }
    
    base_explanation = explanations.get(crop_name, "Suitable for current soil and climate conditions based on analysis.")
    return f"{base_explanation} (Confidence: {confidence:.1%})"

def ask_farmer_questions():
    """Ask farmer-friendly questions and return their answers."""
    print("=== Crop Recommendation System ===")
    print("Please answer the following questions about your farm conditions:\n")
    
    # Soil type
    print("1. What type of soil do you have?")
    print("   Options: sandy, loamy, clay, red, black")
    soil_type = input("Your answer: ").strip().lower()
    
    # Fertilizer use
    print("\n2. How much fertilizer do you typically use?")
    print("   Options: none, low, medium, high")
    fertilizer_use = input("Your answer: ").strip().lower()
    
    # Temperature feel
    print("\n3. How would you describe your farm's temperature?")
    print("   Options: cool, warm, hot")
    temperature_feel = input("Your answer: ").strip().lower()
    
    # Humidity feel
    print("\n4. How would you describe the humidity level?")
    print("   Options: dry, moderate, humid")
    humidity_feel = input("Your answer: ").strip().lower()
    
    # pH feel
    print("\n5. How would you describe your soil's acidity?")
    print("   Options: acidic, neutral, alkaline")
    ph_feel = input("Your answer: ").strip().lower()
    
    # Rainfall season
    print("\n6. How would you describe your rainfall pattern?")
    print("   Options: low, medium, high, very_high")
    rainfall_season = input("Your answer: ").strip().lower()
    
    return soil_type, fertilizer_use, temperature_feel, humidity_feel, ph_feel, rainfall_season

def load_model_and_encoder():
    """Load the trained model and label encoder."""
    try:
        model_path = "rf_crop_model.pkl"
        encoder_path = "label_encoder.pkl"

        if not os.path.exists(model_path):
            print("Error: 'rf_crop_model.pkl' not found. Please keep the trained model in this folder.")
            return None, None

        if not os.path.exists(encoder_path):
            print("Error: 'label_encoder.pkl' not found. Please keep the label encoder in this folder.")
            return None, None

        model = joblib.load(model_path)
        label_encoder = joblib.load(encoder_path)

        return model, label_encoder
        
    except Exception as e:
        print(f"Error loading model or encoder: {e}")
        return None, None

def main():
    """Main application workflow."""
    # Load model and encoder
    model, label_encoder = load_model_and_encoder()
    if model is None or label_encoder is None:
        return
    
    # Ask farmer questions
    answers = ask_farmer_questions()
    
    # Convert answers to numeric features
    features = map_farmer_answers_to_features(*answers)
    
    print(f"\nConverted features: N={features[0]}, P={features[1]}, K={features[2]}, "
          f"Temperature={features[3]}°C, Humidity={features[4]}%, pH={features[5]}, Rainfall={features[6]}mm")
    
    # Get predictions with probabilities
    try:
        probabilities = model.predict_proba([features])[0]
        
        # Get crop names from label encoder
        crop_names = label_encoder.classes_
        
        # Create list of (crop, probability) pairs and sort by probability
        crop_probabilities = list(zip(crop_names, probabilities))
        crop_probabilities.sort(key=lambda x: x[1], reverse=True)
        
        # Display top 3 recommendations
        print("\n=== TOP 3 CROP RECOMMENDATIONS ===")
        for i, (crop, prob) in enumerate(crop_probabilities[:3], 1):
            print(f"\n{i}. {crop.upper()}")
            print(f"   Confidence: {prob:.1%}")
            print(f"   Recommendation: {get_crop_explanation(crop, prob)}")
        
    except Exception as e:
        print(f"Error making predictions: {e}")
        print("Please ensure your model supports predict_proba() method.")

if __name__ == "__main__":
    main()
