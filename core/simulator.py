# core/simulator.py
import numpy as np
import pandas as pd

def generate_consumer_agents(num_agents: int = 1000) -> pd.DataFrame:
    """
    Generates a synthetic population of consumer agents with diverse behavioral traits.
    Optimized for standard premium retail items (e.g., Organic Coffee, Popcorn).
    """
    np.random.seed(42)  # Set seed for reproducible simulations
    
    # 1. Budget: What is the absolute max they will spend? (Mean $15, StdDev $4)
    budgets = np.random.normal(loc=15.0, scale=4.0, size=num_agents)
    budgets = np.clip(budgets, 4.0, 30.0)  # Keep within realistic boundaries
    
    # 2. Price Sensitivity (beta): Higher means they hate spending money more
    price_sensitivity = np.random.beta(a=2, b=5, size=num_agents) * 2.5
    
    # 3. Value/Feature Sensitivity (gamma): Higher means they highly value getting the premium size
    value_sensitivity = np.random.normal(loc=1.5, scale=0.5, size=num_agents)
    value_sensitivity = np.clip(value_sensitivity, 0.1, 3.0)
    
    return pd.DataFrame({
        "agent_id": range(num_agents),
        "budget": budgets,
        "price_sensitivity": price_sensitivity,
        "value_sensitivity": value_sensitivity
    })

def run_choice_simulation(pricing_strategy: dict, agent_df: pd.DataFrame) -> dict:
    """
    Simulates the purchasing decision for every agent based on a Utility function.
    """
    # Define perceived relative value/utility scores for the sizes
    tier_values = {"Small (Base)": 1.0, "Medium (Decoy)": 2.2, "Large (Premium)": 3.0}
    choices = []
    
    for _, agent in agent_df.iterrows():
        utilities = {}
        
        # Calculate utility for each available pricing tier
        for tier, price in pricing_strategy.items():
            # Hard constraint: If it exceeds their budget, they cannot buy it
            if price > agent["budget"]:
                utilities[tier] = -np.inf
            else:
                # Utility = (Value * Weight) - (Price * Weight) + Gumbel Random Noise
                gumbel_noise = np.random.gumbel(0, 0.1)
                u = (tier_values[tier] * agent["value_sensitivity"]) - (price * agent["price_sensitivity"]) + gumbel_noise
                utilities[tier] = u
                
        # The No-Purchase Option (Walking away entirely has a base utility of 0)
        utilities["No Purchase"] = 0.0
        
        # Agent picks the option that yields the highest utility
        chosen_tier = max(utilities, key=utilities.get)
        choices.append(chosen_tier)
        
    # Aggregate data metrics
    agent_df["choice"] = choices
    conversion_counts = agent_df["choice"].value_counts()
    
    total_agents = len(agent_df)
    results = {}
    total_revenue = 0.0
    
    for option in ["Small (Base)", "Medium (Decoy)", "Large (Premium)", "No Purchase"]:
        count = conversion_counts.get(option, 0)
        percentage = (count / total_agents) * 100
        results[option] = f"{percentage:.1f}%"
        
        if option in pricing_strategy:
            total_revenue += count * pricing_strategy[option]
            
    results["Total Revenue Generated"] = f"${total_revenue:.2f}"
    
    return results