def map_farmer_answers_to_features(soil_type, fertilizer_use, temperature_feel, humidity_feel, ph_feel, rainfall_season):
    """
    Convert farmer-friendly answers to numeric features expected by the model.
    
    Expected inputs:
    - soil_type: str - "sandy", "loamy", "clay", "red", "black"
    - fertilizer_use: str - "none", "low", "medium", "high"
    - temperature_feel: str - "cool", "warm", "hot"
    - humidity_feel: str - "dry", "moderate", "humid"
    - ph_feel: str - "acidic", "neutral", "alkaline"
    - rainfall_season: str - "low", "medium", "high", "very_high"
    
    Returns: tuple of (N, P, K, temperature, humidity, pH, rainfall)
    """
    
    # NPK mapping based on soil type and fertilizer use
    soil_npk = {
        "sandy": {"N": 15, "P": 10, "K": 20},
        "loamy": {"N": 25, "P": 15, "K": 25},
        "clay": {"N": 20, "P": 12, "K": 30},
        "red": {"N": 18, "P": 8, "K": 22},
        "black": {"N": 22, "P": 18, "K": 35}
    }
    
    fertilizer_adjustment = {
        "none": {"N": 0, "P": 0, "K": 0},
        "low": {"N": 5, "P": 3, "K": 5},
        "medium": {"N": 10, "P": 8, "K": 10},
        "high": {"N": 15, "P": 12, "K": 15}
    }
    
    # Get base NPK from soil
    base_npk = soil_npk.get(soil_type, {"N": 20, "P": 12, "K": 25})
    
    # Adjust based on fertilizer use
    fert_adj = fertilizer_adjustment.get(fertilizer_use, {"N": 0, "P": 0, "K": 0})
    
    N = base_npk["N"] + fert_adj["N"]
    P = base_npk["P"] + fert_adj["P"]
    K = base_npk["K"] + fert_adj["K"]
    
    # Temperature mapping (Celsius)
    temperature_map = {
        "cool": 18,
        "warm": 25,
        "hot": 32
    }
    temperature = temperature_map.get(temperature_feel, 25)
    
    # Humidity mapping (%)
    humidity_map = {
        "dry": 40,
        "moderate": 65,
        "humid": 85
    }
    humidity = humidity_map.get(humidity_feel, 65)
    
    # pH mapping
    ph_map = {
        "acidic": 5.5,
        "neutral": 7.0,
        "alkaline": 8.5
    }
    ph = ph_map.get(ph_feel, 7.0)
    
    # Rainfall mapping (mm)
    rainfall_map = {
        "low": 500,
        "medium": 1000,
        "high": 1500,
        "very_high": 2000
    }
    rainfall = rainfall_map.get(rainfall_season, 1000)
    
    return (N, P, K, temperature, humidity, ph, rainfall)