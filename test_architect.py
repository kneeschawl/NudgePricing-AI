# test_architect.py
from core.architect import generate_pricing_package
from core.simulator import generate_consumer_agents, run_choice_simulation
from agents.llm_client import generate_pricing_copy

# 1. Run the deterministic math architectures
product = "Premium Organic Coffee Beans"
pricing_strategy = generate_pricing_package(cogs=3.00, target_margin=0.50, alpha=0.15)

# 2. Execute multi-agent simulation sandbox
agents = generate_consumer_agents(num_agents=1000)
results = run_choice_simulation(pricing_strategy, agents)

print("\nRunning local Llama 3.1 model optimization...")
# 3. Request semantic copy overlay from local LLM
copywriting_strategy = generate_pricing_copy(
    product_context=product, 
    pricing_tiers=pricing_strategy, 
    simulation_data=results
)

print("\n=== AI CONSULTANT PERSUASIVE COPY PROPOSAL ===")
print(copywriting_strategy)
print("==============================================")