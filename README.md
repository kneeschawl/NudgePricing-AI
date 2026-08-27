# 📊 NudgePricing AI - Enterprise Core Suite

NudgePricing AI is a high-standard, quantitative behavioral sandbox designed to architect, test, and optimize asymmetric pricing models. By leveraging multi-agent simulations, the application tests pricing tiers against 1,000 synthetic consumer profiles to accurately forecast market share distribution, batch revenue, and price friction before hitting production.
NudgePricing AI is an interactive Streamlit application for testing and refining tiered pricing strategies with behavioral simulation. It models how synthetic consumers choose among base, decoy, and premium options, then surfaces market-share and revenue outcomes before you ship pricing to production.

![Streamlit Version](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat-square&logo=Streamlit)
![Plotly Engine](https://img.shields.io/badge/Graphics-Plotly-3F4F75?style=flat-square&logo=Plotly)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=Python)

---

## 🚀 Key Features
## What this project does

* **Multi-Agent Simulation Engine:** Instantly spins up 1,000 algorithmic consumer agents with varying utility thresholds to test tier pricing strategies.
* **Asymmetric Controls:** Choose between manual tier calibration or an automated AI routine driving structural optimization (Alpha compression ratios).
* **Enterprise-Grade UI:** A sleek, theme-adaptive interface powered by modern typography (*Plus Jakarta Sans* & *Inter*) that translates flawlessly between Native Light and Dark environments.
* **Generative Strategy Briefing:** An integrated LLM analyst layer that evaluates live simulation results to offer deep architectural feedback on pricing friction patterns.
NudgePricing AI combines:

- **Pricing architecture logic** to build and tune 3-tier menus.
- **Agent-based simulation** across 1,000 synthetic consumers with heterogeneous budgets and sensitivities.
- **Outcome analytics** for tier share, abandonment (`No Purchase`), and projected batch revenue.
- **LLM-assisted strategy commentary** that explains pricing friction and optimization directions using current simulation context.

---

## 🛠️ Tech Stack & Architecture
## Core features

- **Manual Price Tester**
  - Enter product context and all three prices directly.
  - Validate tier structure (`Small < Medium < Large`) in the UI.

- **AI Automated Optimization**
  - Set COGS, target baseline margin, and decoy compression factor (`alpha`).
  - Automatically derive:
    - `Small (Base)` from target margin
    - `Large (Premium)` as a premium multiple
    - `Medium (Decoy)` via asymmetric decoy injection

- **Behavioral simulation engine**
  - Generates a reproducible synthetic population.
  - Scores each option with a utility function using value sensitivity, price sensitivity, budget constraints, and stochastic noise.
  - Aggregates conversion distribution and revenue.

- **Executive Strategy Briefing**
  - Chat interface backed by an OpenAI-compatible local LLM endpoint (default: Ollama).
  - Prompting is bounded to the current product/pricing/simulation data.

---

* **UI Layer:** Streamlit (Dynamic layout grid, responsive metric wrappers)
* **Data Visualization:** Plotly Express (Tailored corporate color matrix)
* **Agent Modeling:** Native Python state matrices
* **Generative Backend:** Configurable Open-AI / LLM Clients
## Repository structure

```text
nudgepricing-ai/
├── agents/
│   ├── llm_client.py          # Handles API initialization and LLM pooling
│   └── prompt_templates.py    # System prompts guiding the pricing analyst
NudgePricing-AI/
├── app.py                       # Streamlit app and dashboard workflow
├── core/
│   ├── architect.py           # Handles automated decoy price injection
│   └── simulator.py           # Orchestrates agent behavior matrices
├── .env                       # Local secrets (API Keys) - Ignored by Git
├── .gitignore                 # Workspace cleanup rules
├── app.py                     # Main dashboard entrypoint
│   ├── architect.py             # Pricing tier and decoy generation logic
│   └── simulator.py             # Synthetic agents + choice simulation engine
├── agents/
│   ├── llm_client.py            # OpenAI-compatible local LLM client
│   └── prompt_templates.py      # Context-bounded analyst system prompt
├── requirements.txt             # Python dependencies
└── README.md
```

---

## Technology stack

- **Frontend / App Layer:** Streamlit
- **Data & Numerics:** Pandas, NumPy
- **Visualization:** Plotly Express
- **LLM Client:** `openai` Python SDK against local OpenAI-compatible servers (e.g., Ollama)

---

## How it works

1. Build pricing tiers manually or via automated controls.
2. Run simulation against synthetic agents.
3. Review:
   - Tier selection percentages
   - No-purchase rate (price friction signal)
   - Total projected revenue
4. Ask the LLM analyst for interpretation and optimization suggestions.

---

## Getting started

### 1) Clone and enter the project

```bash
git clone https://github.com/kneeschawl/NudgePricing-AI.git
cd NudgePricing-AI
```

### 2) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

For Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables (optional)

Create a `.env` file in the repository root:

```env
LLM_HOST=http://localhost:11434/v1
LLM_MODEL=llama3.1:8b
```

Defaults are already defined in code, so this step is optional unless you want custom values.

### 5) Run the app

```bash
streamlit run app.py
```

---

## LLM backend notes

- The app expects an **OpenAI-compatible** chat-completions endpoint.
- Default API key is set to `ollama` for local usage.
- If the model server is unavailable, the UI shows an explicit runtime error in the briefing panel.

---

## Practical interpretation tips

- High **No Purchase** usually indicates pricing friction or low perceived value.
- Tune **alpha** to reposition the decoy relative to the premium tier.
- Re-run simulations after each tier adjustment and compare revenue vs abandonment, not revenue alone.

---

## License

This project is distributed under the terms in [LICENSE](./LICENSE).
