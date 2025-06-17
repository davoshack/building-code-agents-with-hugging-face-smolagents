# Add your utilities or helper functions to this file.

import os
import numpy as np
import pandas as pd


def calculate_transport_cost(distance_km: float, order_volume: float) -> float:
    """
    Calculate transportation cost based on distance and order size.
    Assumes refrigerated transport costs $2.5 per mile and has a capacity of 300 liters.

    Args:
        distance_km: the distance in kilometers
        order_volume: the order volume in liters
    """
    trucks_needed = np.ceil(order_volume / 300)
    cost_per_km = 1.20
    return distance_km * cost_per_km * trucks_needed


def calculate_tariff(base_cost: float, is_canadian: bool) -> float:
    """
    Calculates tariff for Canadian imports. Returns the tariff only, not the total cost.
    Assumes 7.5% tariff on dairy products from Canada.

    Args:
        base_cost: the base cost.
        is_canadian: wether the import is from Canada.
    """
    if is_canadian:
        return base_cost * 0.075
    return 0

def analyze_supplier_costs(suppliers_df, daily_need_liters=30):
    """
    Analyze total costs for each supplier based on daily needs.
    """
    results = []

    for _, supplier in suppliers_df.iterrows():
        # Ensure order size meets minimum requirement
        order_size = 30  # Daily order

        # Calculate base cost
        base_cost = order_size * supplier["base_price_per_liter"]

        # Calculate transport cost
        transport_cost = calculate_transport_cost(supplier["distance_km"], order_size)

        # Calculate tariff if applicable
        tariff = calculate_tariff(base_cost, supplier["is_canadian"])

        # Calculate total cost and daily cost
        daily_cost = base_cost + transport_cost + tariff

        results.append(
            {
                "supplier": supplier["name"],
                "order_size_liters": order_size,
                "base_cost": base_cost,
                "transport_cost": transport_cost,
                "tariff": tariff,
                "daily_cost": daily_cost,
            }
        )

    return pd.DataFrame(results)
