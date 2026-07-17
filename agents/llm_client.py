# agents/llm_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Default local endpoints: Change host URL if you are using LM Studio (typically http://localhost:1234/v1)
OLLAMA_HOST = os.getenv("LLM_HOST", "http://localhost:11434/v1")
MODEL_NAME = os.getenv("LLM_MODEL", "llama3.1:8b")

def get_llm_client():
    """Initializes an OpenAI-compatible client pointing to your local server."""
    return OpenAI(
        base_url=OLLAMA_HOST,
        api_key="ollama"  # Local hosts do not require a real API key
    )

def generate_pricing_copy(product_context: str, pricing_tiers: dict, simulation_data: dict) -> str:
    """
    Sends the localized simulation context to Llama 3.1 to generate 
    psychological marketing copy and value justifications.
    """
    client = get_llm_client()
    
    system_prompt = (
        "You are an expert behavioral economist and conversion copywriter. Your job is to analyze "
        "raw economic simulation data and create persuasive storefront product features that maximize "
        "conversion rate. You must speak directly to the target buyer, using pricing anchoring principles."
    )
    
    user_prompt = f"""
    Product Category: {product_context}
    
    Current Pricing Tiers:
    - Small (Base): ${pricing_tiers['Small (Base)']:.2f}
    - Medium (Decoy): ${pricing_tiers['Medium (Decoy)']:.2f}
    - Large (Premium): ${pricing_tiers['Large (Premium)']:.2f}
    
    Simulation Performance Metrics:
    - Small Selection Rate: {simulation_data.get('Small (Base)')}
    - Medium Selection Rate: {simulation_data.get('Medium (Decoy)')}
    - Large Selection Rate: {simulation_data.get('Large (Premium)')}
    - Market Abandonment (No Purchase): {simulation_data.get('No Purchase')}
    
    CRITICAL CHALLENGE: 
    Our behavioral model shows an 83.3% 'No Purchase' rate because the jump to the decoy is too high. 
    Write compelling feature points for the three tiers. For the Large tier, emphasize massive 
    added value (e.g., free shipping, bonus accessories, or double quantities) to justify the price 
    and salvage the walkaway shoppers. Keep the response concise and formatted in clean Markdown.
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to local LLM server: {str(e)}. Please check if your local server is running."