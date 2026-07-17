# core/architect.py

def calculate_base_tiers(cogs: float, target_margin: float = 0.50) -> tuple[float, float]:
    """
    Calculates the baseline economy (P1) and premium (P3) price boundaries.
    
    Args:
        cogs: Cost of Goods Sold for the product base.
        target_margin: Minimum acceptable profit margin (e.g., 0.50 = 50%).
        
    Returns:
        A tuple containing (Price_Small, Price_Large)
    """
    # Small tier covers the cost and guarantees the bare minimum margin
    price_small = round(cogs / (1 - target_margin), 2)
    
    # Large tier leverages premium framing (typically 2x to 2.5x base price depending on category)
    price_large = round(price_small * 2.2, 2)
    
    return price_small, price_large


def inject_decoy_price(price_small: float, price_large: float, alpha: float = 0.15) -> float:
    """
    Programmatically engineers the decoy price (P2) using asymmetric dominance compression.
    
    Args:
        price_small: The established base price (P1).
        price_large: The established premium price (P3).
        alpha: Value compression factor. Smaller alpha pushes P2 closer to P3, 
               making the premium option look like a massive bargain.
               
    Returns:
        The optimized decoy price (P2).
    """
    if alpha <= 0 or alpha >= 0.5:
        raise ValueError("Alpha should typically stay between 0.05 and 0.30 to create an effective decoy.")
        
    # Asymmetric decoy logic: P2 sits tightly beneath P3
    price_decoy = price_large - ((price_large - price_small) * alpha)
    
    return round(price_decoy, 2)


def generate_pricing_package(cogs: float, target_margin: float = 0.50, alpha: float = 0.15) -> dict:
    """
    Orchestrates the phase 1 engine to yield a complete 3-tier pricing object.
    """
    p1, p3 = calculate_base_tiers(cogs, target_margin)
    p2 = inject_decoy_price(p1, p3, alpha)
    
    return {
        "Small (Base)": p1,
        "Medium (Decoy)": p2,
        "Large (Premium)": p3
    }