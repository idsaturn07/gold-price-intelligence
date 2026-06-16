# ☁️ Azure Deployment Guide

Full step-by-step instructions for deploying Gold Price Intelligence to Azure.

---

## Step 1 — Azure AI Foundry Project + Agent

1. Go to [ai.azure.com](https://ai.azure.com) and sign in
2. Click **New Project** → give it any name → click **Create**
3. Go to **Settings** → copy the **Project Endpoint URL**
   - Format: `https://your-resource.services.ai.azure.com/api/projects/your-project`
4. In the left sidebar click **Agents** → **New Agent**
5. Set agent name to exactly: `gold-bot`
6. Under **Tools**, enable **Web Search** grounding
7. Click **Deploy** → note the version number
8. Go to **Settings → Keys** → copy the **API Key**

---

## Step 2 — Azure Storage Account + Blob Container

1. In [portal.azure.com](https://portal.azure.com) search **Storage Accounts** → **Create**
2. Fill in name, region, redundancy (LRS is fine) → **Create**
3. Once deployed → **Containers** → **+ Container** → name it exactly: `models` → **Create**
4. Go to **Access Keys** → **Show** → copy the **Connection string**

---

## Step 3 — Azure App Service

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

---

## Step 4 — Azure Function App

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

## Step 5 — Deploy Web App

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

---

## Step 6 — Deploy Retraining Function

```bash
cd retrain-function
cp local.settings.example.json local.settings.json
# Fill in local.settings.json with your values
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

Once deployed, the function runs automatically every day at **1:00 AM**, retrains the model, and uploads fresh artifacts to Blob Storage.
