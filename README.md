# 📊 NudgePricing AI - Enterprise Core Suite

NudgePricing AI is a high-standard, quantitative behavioral sandbox designed to architect, test, and optimize asymmetric pricing models. By leveraging multi-agent simulations, the application tests pricing tiers against 1,000 synthetic consumer profiles to accurately forecast market share distribution, batch revenue, and price friction before hitting production.

![Streamlit Version](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat-square&logo=Streamlit)
![Plotly Engine](https://img.shields.io/badge/Graphics-Plotly-3F4F75?style=flat-square&logo=Plotly)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=Python)

---

## 🚀 Key Features

* **Multi-Agent Simulation Engine:** Instantly spins up 1,000 algorithmic consumer agents with varying utility thresholds to test tier pricing strategies.
* **Asymmetric Controls:** Choose between manual tier calibration or an automated AI routine driving structural optimization (Alpha compression ratios).
* **Enterprise-Grade UI:** A sleek, theme-adaptive interface powered by modern typography (*Plus Jakarta Sans* & *Inter*) that translates flawlessly between Native Light and Dark environments.
* **Generative Strategy Briefing:** An integrated LLM analyst layer that evaluates live simulation results to offer deep architectural feedback on pricing friction patterns.

---

## 🛠️ Tech Stack & Architecture

* **UI Layer:** Streamlit (Dynamic layout grid, responsive metric wrappers)
* **Data Visualization:** Plotly Express (Tailored corporate color matrix)
* **Agent Modeling:** Native Python state matrices
* **Generative Backend:** Configurable Open-AI / LLM Clients

```text
nudgepricing-ai/
├── agents/
│   ├── llm_client.py          # Handles API initialization and LLM pooling
│   └── prompt_templates.py    # System prompts guiding the pricing analyst
├── core/
│   ├── architect.py           # Handles automated decoy price injection
│   └── simulator.py           # Orchestrates agent behavior matrices
├── .env                       # Local secrets (API Keys) - Ignored by Git
├── .gitignore                 # Workspace cleanup rules
├── app.py                     # Main dashboard entrypoint

