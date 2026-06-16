# 🪙 Gold Price Intelligence
### AI-Powered Financial Market Forecasting with LSTM & Azure AI Foundry

> An end-to-end machine learning platform for financial market forecasting — using gold as the primary use case. Built with LSTM deep learning, real-time news sentiment analysis, and an Azure AI Foundry chatbot assistant.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-orange.svg)](https://tensorflow.org)
[![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4.svg)](https://azure.microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**GitHub:** [github.com/idsaturn07/gold-price-intelligence](https://github.com/idsaturn07/gold-price-intelligence)

---

## 🎯 Key Achievements

- Built an end-to-end machine learning pipeline using **TensorFlow LSTM** trained on 5 years of market data
- Automated **daily model retraining** using Azure Functions Timer Trigger with artifact upload to Azure Blob Storage
- Integrated **Azure AI Foundry Agents** with live contextual market data for intelligent Q&A
- Implemented **real-time sentiment analysis** from live financial news via NewsAPI + TextBlob
- Deployed an interactive **multi-currency analytics dashboard** using Streamlit with live FX rates
- Architected a full **MLOps pipeline** — data ingestion → training → evaluation → storage → serving

---

## 📌 What It Does

- 🔮 Predicts **tomorrow's gold price** using a deep learning LSTM model trained on 5 years of data
- 📈 Shows **interactive price history chart** with live currency conversion
- 📊 Displays **price range** (Low / Predicted / High) based on model MAE error margin
- 💱 Supports **5 currencies** — USD, INR, EUR, GBP, JPY with live exchange rates
- 🌍 Filters news by **region** — Global, India, USA, UK, Japan
- 📰 Fetches **live financial news** and scores sentiment (Positive / Negative / Neutral)
- 🤖 **AI chatbot** powered by Azure AI Foundry Agents with live web search grounding
- 🔄 **Automated daily retraining** via Azure Functions Timer Trigger
- ☁️ **Model artifacts** stored and synced via Azure Blob Storage

---

## 📸 Screenshots

### Dashboard — Header, Disclaimer & Currency Selector
![Dashboard](docs/dashboard.png)

### Price Cards, Predicted Range & Chart
![Price Cards and Chart](docs/price-cards.png)

### 5-Year Price Trend & Live News Sentiment
![Chart and News](docs/chart-news.png)

### Overall Market Sentiment & AI Assistant
![Sentiment and Chatbot](docs/sentiment-chatbot.png)

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| MAE | 101.17 |
| RMSE | 135.38 |
| Training Samples | 926 |
| Training Data | 5 Years (2021–2026, GC=F Futures) |
| Features | Open, High, Low, Close |
| Architecture | 2-Layer LSTM + Dropout (0.3) |
| Optimizer | Adam |
| Loss Function | MSE |
| Train / Test Split | 80% / 20% |
| Next Day Prediction | $4,214.07 (as of June 15, 2026) |

> Run `python model.py` to retrain and see updated values for your own run.

---

## 🗂️ Project Structure

```
gold-price-intelligence/
│
├── app/                              # Streamlit web app
│   ├── app.py                        # Main UI — entry point
│   ├── chatbot.py                    # Azure AI Foundry Agent integration
│   ├── model.py                      # LSTM model, gold data fetch, news sentiment
│   ├── requirements.txt              # Python dependencies
│   ├── startup.sh                    # Azure App Service startup command
│   ├── .env.example                  # Environment variable template
│   └── .gitignore
│
├── retrain-function/                 # Azure Functions — daily model retraining
│   ├── function_app.py               # Timer trigger — retrains and uploads to Blob
│   ├── model.py                      # Training logic
│   ├── host.json                     # Azure Functions config
│   ├── requirements.txt              # Python dependencies
│   ├── local.settings.example.json   # Settings template
│   └── .gitignore
│
├── docs/                             # Screenshots
│   ├── dashboard.png
│   ├── price-cards.png
│   ├── chart-news.png
│   └── sentiment-chatbot.png
│
├── LICENSE
└── README.md
```

---

## 🧠 Architecture

```
                    ┌──────────────────────┐
                    │   Azure App Service   │
                    │    (Streamlit UI)     │
                    └─────────┬────────────┘
                              │
               ┌──────────────┼──────────────┐
               │              │              │
      ┌────────▼──────┐  ┌────▼───┐  ┌──────▼──────────┐
      │  LSTM Model   │  │  News  │  │  Azure AI        │
      │  (.keras file)│  │  API   │  │  Foundry Agent   │
      └────────┬──────┘  └────┬───┘  │  (gold-bot)      │
               │              │      └──────▲────────────┘
      ┌────────▼──────────────▼──────┐      │
      │      Azure Blob Storage      │      │
      │    (models container)        │      │
      └────────▲─────────────────────┘      │
               │                            │
      ┌────────┴───────────┐                │
      │   Azure Functions  │────────────────┘
      │   Timer Trigger    │  (runs daily at 1AM)
      └────────────────────┘
```

---

## ✅ Prerequisites

Before starting, make sure you have:

- [ ] Python 3.9+ → [python.org](https://python.org)
- [ ] Azure subscription → [azure.microsoft.com/free](https://azure.microsoft.com/free)
- [ ] Azure CLI → [aka.ms/installazurecli](https://aka.ms/installazurecli)
- [ ] Azure Functions Core Tools → [aka.ms/azfunc-tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local)
- [ ] NewsAPI key → [newsapi.org](https://newsapi.org) (free, no card needed)
- [ ] Git → [git-scm.com](https://git-scm.com)

---

## ⚙️ Step-by-Step Setup

### Step 1 — Clone the Repository

```bash
git clone https://github.com/idsaturn07/gold-price-intelligence.git
cd gold-price-intelligence
```

---

### Step 2 — Create Azure Resources

#### 2A. Azure AI Foundry Project + Agent

1. Go to [ai.azure.com](https://ai.azure.com) and sign in
2. Click **New Project** → give it any name → click **Create**
3. Go to **Settings** → copy the **Project Endpoint URL**
   - Format: `https://your-resource.services.ai.azure.com/api/projects/your-project`
4. In the left sidebar click **Agents** → **New Agent**
5. Set agent name to exactly: `gold-bot`
6. Under **Tools**, enable **Web Search** grounding
7. Click **Deploy** → note the version number
8. Go to **Settings → Keys** → copy the **API Key**

#### 2B. Azure Storage Account + Blob Container

1. In [portal.azure.com](https://portal.azure.com) search **Storage Accounts** → **Create**
2. Fill in name, region, redundancy (LRS is fine) → **Create**
3. Once deployed → **Containers** → **+ Container** → name it exactly: `models` → **Create**
4. Go to **Access Keys** → **Show** → copy the **Connection string**

#### 2C. Azure App Service

1. Search **App Services** → **Create**
2. Set **Runtime**: Python 3.9, **OS**: Linux
3. Once deployed → **Configuration → Application Settings** → add:

| Name | Value |
|---|---|
| `AZURE_PROJECT_ENDPOINT` | Your Foundry project endpoint URL |
| `AZURE_OPENAI_ENDPOINT` | `https://your-resource.services.ai.azure.com/openai/v1` |
| `AZURE_OPENAI_KEY` | Your Foundry API key |
| `AZURE_DEPLOYMENT_NAME` | Your model deployment name in Foundry |
| `AZURE_AGENT_NAME` | `gold-bot` |
| `AZURE_AGENT_VERSION` | `2` |
| `NEWS_API_KEY` | Your NewsAPI key |

4. **General Settings → Startup Command**: `bash startup.sh` → **Save**

#### 2D. Azure Function App

1. Search **Function App** → **Create**
2. Set **Runtime**: Python 3.9, **Hosting**: Consumption (free)
3. Once deployed → **Configuration → Application Settings** → add:

| Name | Value |
|---|---|
| `AzureWebJobsStorage` | Storage account connection string |
| `BLOB_CONNECTION_STRING` | Storage account connection string |
| `NEWS_API_KEY` | Your NewsAPI key |

4. Click **Save**

---

### Step 3 — Set Up the Web App Locally

```bash
cd app
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and fill in your values:

```env
AZURE_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_OPENAI_ENDPOINT=https://your-resource.services.ai.azure.com/openai/v1
AZURE_OPENAI_KEY=your_azure_openai_key_here
AZURE_DEPLOYMENT_NAME=your_deployment_name
AZURE_AGENT_NAME=gold-bot
AZURE_AGENT_VERSION=2
NEWS_API_KEY=your_newsapi_key_here
```

> Rename `.env.example` to `.env` after filling in your values.

---

### Step 4 — Train the LSTM Model

```bash
cd app
python model.py
```

This downloads 5 years of gold futures data, trains the LSTM (~5–15 min), and saves 4 model artifact files locally. Expected output:

```
Fetching gold data...
Data loaded: 1258 rows | 2021-06-15 to 2026-06-15
Training model on 926 samples...
Epoch 1/50 ...
...
MODEL PERFORMANCE
   MAE  : 101.17
   RMSE : 135.38
   Predicted Tomorrow : $4214.07
Model Saved
```

> ⚠️ You must run this once before launching the app. The app will show an error on startup if model files are missing.

---

### Step 5 — Run Locally

```bash
cd app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

### Step 6 — Set Up Retraining Function Locally

```bash
cd retrain-function
pip install -r requirements.txt
cp local.settings.example.json local.settings.json
```

Fill in `local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "your_storage_connection_string_here",
    "BLOB_CONNECTION_STRING": "your_storage_connection_string_here",
    "NEWS_API_KEY": "your_newsapi_key_here"
  }
}
```

> Rename `local.settings.example.json` to `local.settings.json` after filling in your values.

Test locally (requires Azure Functions Core Tools):

```bash
func start
```

---

## 🚀 Deployment

### Web App → Azure App Service

```bash
cd app
zip -r app.zip . -x "*.pkl" -x "*.keras" -x ".env" -x "__pycache__/*"
az webapp deployment source config-zip \
  --resource-group YOUR_RESOURCE_GROUP \
  --name YOUR_APP_SERVICE_NAME \
  --src app.zip
```

Upload model artifacts via Azure Portal → App Service → **Advanced Tools (Kudu)** → Debug Console → `site/wwwroot/` → drag and drop:
- `gold_model.keras`
- `gold_scaler.pkl`
- `gold_data.pkl`
- `gold_metrics.pkl`

Your app will be live at: `https://YOUR_APP_SERVICE_NAME.azurewebsites.net`

### Retraining Function → Azure Functions

```bash
cd retrain-function
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

Once deployed, the function runs automatically every day at **1:00 AM**, retrains the model, and uploads fresh artifacts to Blob Storage.

---

## 🔐 Environment Variables Reference

### `app/.env.example`

| Variable | Where to Find It |
|---|---|
| `AZURE_PROJECT_ENDPOINT` | AI Foundry → Project → Settings |
| `AZURE_OPENAI_ENDPOINT` | AI Foundry → Project → Settings |
| `AZURE_OPENAI_KEY` | AI Foundry → Project → Keys |
| `AZURE_DEPLOYMENT_NAME` | AI Foundry → Deployments |
| `AZURE_AGENT_NAME` | The agent you created (`gold-bot`) |
| `AZURE_AGENT_VERSION` | Agent version in Foundry |
| `NEWS_API_KEY` | newsapi.org → Account |

### `retrain-function/local.settings.example.json`

| Variable | Where to Find It |
|---|---|
| `AzureWebJobsStorage` | Storage Account → Access Keys → Connection string |
| `BLOB_CONNECTION_STRING` | Storage Account → Access Keys → Connection string |
| `NEWS_API_KEY` | newsapi.org → Account |

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| ML Model | TensorFlow / Keras — 2-Layer LSTM |
| Market Data | yfinance (Yahoo Finance GC=F futures) |
| News & Sentiment | NewsAPI + TextBlob |
| AI Chatbot | Azure AI Foundry Agents (web search grounded) |
| Currency Rates | exchangerate-api.com (live, 1hr cache) |
| MLOps / Automation | Azure Functions Timer Trigger |
| Model Storage | Azure Blob Storage |
| Hosting | Azure App Service |

---

## 🚧 Future Enhancements

- [ ] Transformer-based forecasting models (replacing LSTM)
- [ ] Model versioning with MLflow
- [ ] Real-time WebSocket market data feeds
- [ ] Multi-asset forecasting — Silver, Crude Oil, Stocks
- [ ] CI/CD deployment pipeline with GitHub Actions
- [ ] Backtesting framework for model evaluation over historical periods

---

## ❓ Troubleshooting

**"No trained model found" on startup**
→ Run `python model.py` inside the `app/` folder first

**Chatbot returns "AI Assistant Error"**
→ Check `AZURE_PROJECT_ENDPOINT` and `AZURE_OPENAI_KEY` in `.env`
→ Ensure `gold-bot` agent exists in your Foundry project

**News shows "No news available"**
→ Verify `NEWS_API_KEY` at newsapi.org — free tier has rate limits

**Currency values look wrong**
→ Live rates fetch from exchangerate-api.com — falls back to hardcoded rates if API is down

**Azure Function not uploading models**
→ Check `BLOB_CONNECTION_STRING` in Function App Configuration
→ Confirm the `models` container exists in your Storage Account
→ Check logs: Azure Portal → Function App → Functions → Monitor

---

## ⚠️ Disclaimer

This application is for **informational and educational purposes only**. Predictions are generated by a machine learning model trained on historical data and do not account for real-world events, geopolitical factors, or market anomalies. This is **not financial advice**. Always consult a qualified financial advisor before making investment decisions.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
