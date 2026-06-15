from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT      = os.getenv("AZURE_PROJECT_ENDPOINT")
AGENT_NAME    = os.getenv("AZURE_AGENT_NAME", "gold-bot")
AGENT_VERSION = os.getenv("AZURE_AGENT_VERSION", "2")

# Initialize once at module level
project_client = AIProjectClient(
    endpoint=ENDPOINT,
    credential=DefaultAzureCredential()
)
openai_client = project_client.get_openai_client()


def ask_ai(price_per_gram, price_per_ounce, sentiment, question, country="Global", currency="USD", history=None):
    messages = []

    # Cap history to last 20 messages (10 exchanges) to avoid huge API calls
    if history:
        history = history[-20:]
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # Natural context injection
    messages.append({
        "role": "user",
        "content": f"[Market context: predicted gold price for tomorrow is {price_per_gram:.2f}/gram, sentiment is {sentiment}, region is {country}]\n\n{question}"
    })

    try:
        response = openai_client.responses.create(
            input=messages,
            extra_body={
                "agent_reference": {
                    "name"   : AGENT_NAME,
                    "version": AGENT_VERSION,
                    "type"   : "agent_reference"
                }
            }
        )
        return response.output_text or "⚠️ No response received. Please try again."

    except Exception as e:
        return f"❌ AI Assistant Error: {str(e)}"
