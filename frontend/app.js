const state = {
  currentStep: 0,
  answers: {},
  features: null,
  results: [],
  loading: false,
  error: null
};

const questions = [
  {
    id: "soilType",
    en: "What type of soil do you have?",
    hi: "आपकी मिट्टी का प्रकार क्या है?",
    options: [
      { value: "sandy", en: "Sandy", hi: "रेतीली" },
      { value: "loamy", en: "Loamy", hi: "दोमट" },
      { value: "clay", en: "Clay", hi: "चिकनी" },
      { value: "red", en: "Red", hi: "लाल" },
      { value: "black", en: "Black", hi: "काली" }
    ]
  },
  {
    id: "fertilizer",
    en: "How much fertilizer do you use?",
    hi: "आप कितनी खाद का उपयोग करते हैं?",
    options: [
      { value: "none", en: "None", hi: "कोई नहीं" },
      { value: "low", en: "Low", hi: "कम" },
      { value: "medium", en: "Medium", hi: "मध्यम" },
      { value: "high", en: "High", hi: "अधिक" }
    ]
  },
  {
    id: "temperature",
    en: "How is the temperature in your area?",
    hi: "आपके क्षेत्र का तापमान कैसा है?",
    options: [
      { value: "cool", en: "Cool", hi: "ठंडा" },
      { value: "warm", en: "Warm", hi: "मध्यम" },
      { value: "hot", en: "Hot", hi: "गर्म" }
    ]
  },
  {
    id: "humidity",
    en: "How is the humidity level?",
    hi: "नमी का स्तर कैसा है?",
    options: [
      { value: "dry", en: "Dry", hi: "शुष्क" },
      { value: "moderate", en: "Moderate", hi: "मध्यम" },
      { value: "humid", en: "Humid", hi: "अधिक नमी" }
    ]
  },
  {
    id: "ph",
    en: "How is your soil type?",
    hi: "आपकी मिट्टी की प्रकृति कैसी है?",
    options: [
      { value: "acidic", en: "Acidic", hi: "अम्लीय" },
      { value: "neutral", en: "Neutral", hi: "तटस्थ" },
      { value: "alkaline", en: "Alkaline", hi: "क्षारीय" }
    ]
  },
  {
    id: "rainfall",
    en: "How much rainfall do you receive?",
    hi: "वर्षा कितनी होती है?",
    options: [
      { value: "low", en: "Low", hi: "कम" },
      { value: "medium", en: "Medium", hi: "मध्यम" },
      { value: "high", en: "High", hi: "अधिक" },
      { value: "very_high", en: "Very High", hi: "बहुत अधिक" }
    ]
  }
];

const cropMeta = {
  Rice: {
    hi: "चावल",
    explanationEn: "Prefers warm weather, standing water and heavier soils.",
    explanationHi: "गरम मौसम, अधिक नमी और पानी रोकने वाली मिट्टी में अच्छा रहता है।"
  },
  Wheat: {
    hi: "गेहूँ",
    explanationEn: "Good for cool to warm climates with medium fertility.",
    explanationHi: "ठंडे से मध्यम तापमान और मध्यम खाद वाली मिट्टी के लिए उपयुक्त।"
  },
  Maize: {
    hi: "मक्का",
    explanationEn: "Does well in warm areas with moderate rainfall.",
    explanationHi: "मध्यम वर्षा और गर्म क्षेत्रों में अच्छी पैदावार देता है।"
  },
  Cotton: {
    hi: "कपास",
    explanationEn: "Likes hot climates, well-drained soil and medium rainfall.",
    explanationHi: "गर्म मौसम, पानी आसानी से निकलने वाली मिट्टी और मध्यम वर्षा पसंद करता है।"
  },
  Sugarcane: {
    hi: "गन्ना",
    explanationEn: "Needs high water, warm temperature and fertile soil.",
    explanationHi: "अधिक पानी, गर्म तापमान और उपजाऊ मिट्टी की आवश्यकता होती है।"
  },
  Pulses: {
    hi: "दालें",
    explanationEn: "Fit for low fertilizer use and lighter soils.",
    explanationHi: "कम खाद और हल्की मिट्टी में अच्छी तरह उगती हैं।"
  }
};

function computeFeatures(answers) {
  const fertilizerMap = {
    none: { N: 10, P: 10, K: 10 },
    low: { N: 30, P: 25, K: 25 },
    medium: { N: 60, P: 45, K: 45 },
    high: { N: 90, P: 70, K: 70 }
  };

  const temperatureMap = {
    cool: 18,
    warm: 26,
    hot: 34
  };

  const humidityMap = {
    dry: 35,
    moderate: 60,
    humid: 85
  };

  const phMap = {
    acidic: 5.5,
    neutral: 7,
    alkaline: 8.3
  };

  const rainfallMap = {
    low: 500,
    medium: 800,
    high: 1200,
    very_high: 1800
  };

  const fert = fertilizerMap[answers.fertilizer] || fertilizerMap.medium;
  const temperature = temperatureMap[answers.temperature] || temperatureMap.warm;
  const humidity = humidityMap[answers.humidity] || humidityMap.moderate;
  const ph = phMap[answers.ph] || phMap.neutral;
  const rainfall = rainfallMap[answers.rainfall] || rainfallMap.medium;

  let soilBoost = 0;
  if (answers.soilType === "black" || answers.soilType === "clay") {
    soilBoost = 5;
  } else if (answers.soilType === "sandy") {
    soilBoost = -5;
  }

  const N = Math.max(0, Math.min(100, fert.N + soilBoost));
  const P = Math.max(0, Math.min(100, fert.P + soilBoost));
  const K = Math.max(0, Math.min(100, fert.K + soilBoost));

  return {
    N,
    P,
    K,
    temperature,
    humidity,
    ph,
    rainfall
  };
}

function mockPredict(features) {
  const predictions = [
    { crop: "Rice", probability: 0.0 },
    { crop: "Wheat", probability: 0.0 },
    { crop: "Maize", probability: 0.0 },
    { crop: "Cotton", probability: 0.0 },
    { crop: "Sugarcane", probability: 0.0 },
    { crop: "Pulses", probability: 0.0 }
  ];

  const t = features.temperature;
  const h = features.humidity;
  const r = features.rainfall;
  const n = features.N;

  predictions.forEach(p => {
    if (p.crop === "Rice") {
      p.probability =
        (t >= 24 && t <= 34 ? 0.3 : 0) +
        (h >= 75 ? 0.3 : 0) +
        (r >= 1000 ? 0.3 : 0);
    } else if (p.crop === "Wheat") {
      p.probability =
        (t >= 15 && t <= 24 ? 0.4 : 0) +
        (h >= 40 && h <= 65 ? 0.2 : 0) +
        (r >= 500 && r <= 800 ? 0.2 : 0);
    } else if (p.crop === "Maize") {
      p.probability =
        (t >= 20 && t <= 30 ? 0.4 : 0) +
        (r >= 600 && r <= 900 ? 0.2 : 0);
    } else if (p.crop === "Cotton") {
      p.probability =
        (t >= 25 && t <= 35 ? 0.4 : 0) +
        (r >= 600 && r <= 1100 ? 0.2 : 0);
    } else if (p.crop === "Sugarcane") {
      p.probability =
        (t >= 22 && t <= 32 ? 0.3 : 0) +
        (r >= 1000 ? 0.3 : 0) +
        (n >= 60 ? 0.2 : 0);
    } else if (p.crop === "Pulses") {
      p.probability =
        (t >= 20 && t <= 30 ? 0.3 : 0) +
        (n <= 40 ? 0.3 : 0) +
        (r >= 400 && r <= 800 ? 0.2 : 0);
    }
  });

  let sum = predictions.reduce((acc, p) => acc + p.probability, 0);
  if (sum === 0) {
    predictions.forEach(p => {
      p.probability = 1 / predictions.length;
    });
    sum = 1;
  } else {
    predictions.forEach(p => {
      p.probability = p.probability / sum;
    });
  }

  predictions.sort((a, b) => b.probability - a.probability);
  return predictions.slice(0, 3);
}

function toPercent(prob) {
  return Math.round(prob * 100);
}

function handleOptionSelect(questionId, value) {
  state.answers[questionId] = value;
  if (state.currentStep < questions.length - 1) {
    state.currentStep += 1;
    render();
  } else {
    submitAnswers();
  }
}

function handlePrev() {
  if (state.loading) return;
  if (state.currentStep > 0) {
    state.currentStep -= 1;
    render();
  }
}

function handleRestart() {
  state.currentStep = 0;
  state.answers = {};
  state.features = null;
  state.results = [];
  state.loading = false;
  state.error = null;
  render();
}

function submitAnswers() {
  const features = computeFeatures(state.answers);
  state.features = features;
  state.currentStep = questions.length;
  state.loading = true;
  state.error = null;
  state.results = [];
  render();

  fetch("/api/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      N: features.N,
      P: features.P,
      K: features.K,
      temperature: features.temperature,
      humidity: features.humidity,
      ph: features.ph,
      rainfall: features.rainfall
    })
  })
    .then(res => {
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    })
    .then(data => {
      const serverPredictions = Array.isArray(data.predictions)
        ? data.predictions
        : [];
      let predictions;
      if (serverPredictions.length > 0) {
        predictions = serverPredictions
          .map(p => ({
            crop: p.crop || p.name || "",
            probability:
              typeof p.probability === "number"
                ? p.probability
                : typeof p.confidence === "number"
                ? p.confidence
                : 0
          }))
          .filter(p => p.crop);
        predictions.sort((a, b) => b.probability - a.probability);
        predictions = predictions.slice(0, 3);
      } else {
        predictions = mockPredict(features);
      }
      state.results = predictions;
      state.loading = false;
      state.error = null;
      render();
    })
    .catch(() => {
      const predictions = mockPredict(features);
      state.results = predictions;
      state.loading = false;
      state.error = null;
      render();
    });
}

function renderQuestion() {
  const q = questions[state.currentStep];
  const total = questions.length;
  const step = state.currentStep + 1;
  const selectedValue = state.answers[q.id];
  const percent = (step / total) * 100;

  return `
    <div class="card">
      <div class="wizard-header">
        <div class="step-label">
          Step ${step} / ${total}
        </div>
        <div class="badge-soft">
          Crop Helper
        </div>
      </div>
      <div class="progress-bar">
        <div class="progress-bar-fill" style="width: ${percent}%;"></div>
      </div>
      <div class="question-text">
        <div class="question-en">${q.en}</div>
        <div class="question-hi">(${q.hi})</div>
      </div>
      <div class="options-grid">
        ${q.options
          .map(option => {
            const isSelected = option.value === selectedValue;
            return `
              <button 
                class="option-button ${isSelected ? "selected" : ""}" 
                data-option-value="${option.value}" 
                data-question-id="${q.id}"
                type="button"
              >
                <div class="option-main">
                  <span class="option-en">${option.en}</span>
                  <span class="option-hi">${option.hi}</span>
                </div>
                <div class="option-indicator">
                  ${isSelected ? "✓" : ""}
                </div>
              </button>
            `;
          })
          .join("")}
      </div>
      <div class="nav-row">
        <div class="nav-left">
          <button 
            class="nav-button secondary" 
            data-action="prev" 
            type="button"
            ${state.currentStep === 0 ? "disabled" : ""}
          >
            ◀ Back
          </button>
        </div>
        <div class="nav-right">
          <span class="nav-hint">
            Tap an option to continue
          </span>
        </div>
      </div>
    </div>
  `;
}

function renderResults() {
  const hasResults = state.results && state.results.length > 0;

  if (state.loading) {
    return `
      <div class="card">
        <div class="results-header">
          <div>
            <div class="results-title">Finding best crops</div>
            <div class="results-subtitle">
              कृपया प्रतीक्षा करें...
            </div>
          </div>
        </div>
        <div class="loading-state">
          <div class="spinner"></div>
          <div class="small-note">
            Analysing soil, मौसम और वर्षा की जानकारी
          </div>
        </div>
        <div class="footer-row">
          <button 
            class="nav-button secondary" 
            data-action="prev" 
            type="button"
          >
            ◀ Back
          </button>
          <button 
            class="nav-button primary" 
            data-action="restart" 
            type="button"
          >
            Start again / फिर से शुरू करें
          </button>
        </div>
      </div>
    `;
  }

  if (!hasResults) {
    return `
      <div class="card">
        <div class="results-header">
          <div>
            <div class="results-title">No results</div>
            <div class="results-subtitle">
              कृपया विकल्प चुनकर फिर से प्रयास करें।
            </div>
          </div>
        </div>
        <div class="footer-row">
          <button 
            class="nav-button primary" 
            data-action="restart" 
            type="button"
          >
            Start again / फिर से शुरू करें
          </button>
        </div>
      </div>
    `;
  }

  const featureTags = [
    `N: ${state.features.N}`,
    `P: ${state.features.P}`,
    `K: ${state.features.K}`,
    `Temp: ${state.features.temperature}°C`,
    `Humidity: ${state.features.humidity}%`,
    `pH: ${state.features.ph}`,
    `Rain: ${state.features.rainfall} mm`
  ];

  const suitabilityMessages = [
    { en: "Best suited crop for your field", hi: "(आपके खेत के लिए सबसे उपयुक्त फसल)" },
    { en: "Good alternative crop", hi: "(अच्छा वैकल्पिक विकल्प)" },
    { en: "Possible crop option", hi: "(संभावित विकल्प)" }
  ];

  const resultsHtml = state.results
    .map((item, index) => {
      const cropName = item.crop;
      const meta = cropMeta[cropName] || {};
      const hiName = meta.hi || "";
      const explanationEn =
        meta.explanationEn ||
        "Good match for your soil, मौसम and rainfall pattern.";
      const explanationHi =
        meta.explanationHi ||
        "आपकी मिट्टी, मौसम और वर्षा के अनुसार यह फसल उपयुक्त है।";
      const suit = suitabilityMessages[index];
      return `
        <div class="result-card">
          <div class="result-row">
            <div>
              <div class="crop-name">
                ${index + 1}. ${cropName} ${hiName ? `(${hiName})` : ""}
              </div>
            </div>
            <div class="suitability-pill">
              ${suit.en} <span class="suit-hi">${suit.hi}</span>
            </div>
          </div>
          <div class="explanation">
            <div class="explanation-line">
              ${explanationEn}
            </div>
            <div class="explanation-line">
              ${explanationHi}
            </div>
          </div>
        </div>
      `;
    })
    .join("");

  return `
    <div class="card">
      <div class="results-header">
        <div>
          <div class="results-title">
            Top 3 crops for you
          </div>
          <div class="results-subtitle">
            आपके खेत के लिए सुझाई गई शीर्ष 3 फसलें
          </div>
        </div>
        <div class="badge-soft">
          Guidance / मार्गदर्शन
        </div>
      </div>
      <div class="results-list">
        ${resultsHtml}
      </div>
      <div class="pill-row">
        ${featureTags
          .map(tag => `<span class="pill-tag">${tag}</span>`)
          .join("")}
      </div>
      <div class="footer-row">
        <div class="small-note">
          Final crop निर्णय के लिए स्थानीय सलाह भी लें।
        </div>
        <button 
          class="nav-button primary" 
          data-action="restart" 
          type="button"
        >
          New field / नया खेत
        </button>
      </div>
    </div>
  `;
}

function render() {
  const root = document.getElementById("app");
  if (!root) return;
  if (state.currentStep < questions.length) {
    root.innerHTML = renderQuestion();
  } else {
    root.innerHTML = renderResults();
  }
}

function setupEvents() {
  const root = document.getElementById("app");
  if (!root) return;

  root.addEventListener("click", event => {
    const optionEl = event.target.closest("[data-option-value]");
    if (optionEl) {
      const questionId = optionEl.getAttribute("data-question-id");
      const value = optionEl.getAttribute("data-option-value");
      if (questionId && value) {
        handleOptionSelect(questionId, value);
        return;
      }
    }

    const actionEl = event.target.closest("[data-action]");
    if (actionEl) {
      const action = actionEl.getAttribute("data-action");
      if (action === "prev") {
        handlePrev();
      } else if (action === "restart") {
        handleRestart();
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupEvents();
  render();
});

