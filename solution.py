from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import copy


class InventoryError(Exception):
    """Custom exception for inventory-related errors."""
    pass


def processTransactions(inventory: Dict[str, Any], transactions: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Apply a batch of transactions (purchases, sales, returns).
    Update inventory atomically.
    Validate product IDs and prevent negative stock.
    Return updated inventory and transaction log.
    """
    updated_inventory = copy.deepcopy(inventory)
    transaction_log = []

    for tx in transactions:
        product_id = tx.get("product_id")
        quantity = tx.get("quantity", 0)
        tx_type = tx.get("type", "").lower()  # normalize case

        if product_id not in updated_inventory["products"]:
            raise InventoryError(f"Invalid product ID: {product_id}")

        product = updated_inventory["products"][product_id]

        # Use consistent key name
        current_stock = product.get("quantity", 0)

        # Process transaction
        if tx_type == "purchase":
            current_stock += quantity
        elif tx_type == "sale":
            if current_stock < quantity:
                raise InventoryError(f"Insufficient stock for product {product_id}")
            current_stock -= quantity

            product.setdefault("sales_history", []).append({
                "date": datetime.now().date().isoformat(),
                "quantity": quantity
            })
        elif tx_type == "return":
            current_stock += quantity
        else:
            raise InventoryError(f"Invalid transaction type: {tx_type}")

        # Update product record
        product["quantity"] = current_stock
        product["last_updated"] = datetime.now().isoformat()

        transaction_log.append({
            "timestamp": datetime.now().isoformat(),
            "product_id": product_id,
            "type": tx_type,
            "quantity": quantity,
            "resulting_stock": current_stock
        })

    return updated_inventory, transaction_log


def getStockAlerts(inventory: Dict[str, Any], thresholds: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify products below reorder points and calculate days until stockout.
    Returns prioritized alerts: 'critical', 'warning', 'info'.
    """
    alerts = []

    for pid, product in inventory["products"].items():
        stock = product.get("quantity", 0)
        reorder_point = product.get("reorder_point", thresholds.get("default_reorder", 10))

        avg_daily_sales = _calculate_avg_daily_sales(product)
        days_until_stockout = stock / avg_daily_sales if avg_daily_sales > 0 else float('inf')

        if stock <= reorder_point * 0.25:
            level = "critical"
        elif stock <= reorder_point:
            level = "warning"
        else:
            level = "info"

        alerts.append({
            "product_id": pid,
            "product_name": product["name"],
            "stock": stock,
            "reorder_point": reorder_point,
            "days_until_stockout": round(days_until_stockout, 1),
            "avg_daily_sales": round(avg_daily_sales, 2),
            "priority": level
        })

    priority_order = {"critical": 0, "warning": 1, "info": 2}
    alerts.sort(key=lambda x: (priority_order[x["priority"]], x["days_until_stockout"]))

    return alerts


def _calculate_avg_daily_sales(product: Dict[str, Any], days_window: int = 30) -> float:
    """Calculate average daily sales for a given product based on history."""
    if "sales_history" not in product or not product["sales_history"]:
        return 0.0

    cutoff_date = datetime.now().date() - timedelta(days=days_window)
    sales_in_window = [
        s for s in product["sales_history"]
        if datetime.fromisoformat(s["date"]).date() >= cutoff_date
    ]

    total_sold = sum(s["quantity"] for s in sales_in_window)
    days_count = max((datetime.now().date() - cutoff_date).days, 1)

    return total_sold / days_count


if __name__ == "__main__":
    inventory = {
        "products": {
            "SKU001": {"name": "Product A", "quantity": 150, "reorder_point": 50,  "leadTimeDays": 7, "location": "Zone-A", "safetyStock": 30},
            "SKU002": {"name": "Product B", "quantity": 25, "reorder_point": 40, "leadTimeDays": 5, "location": "Zone-B", "safetyStock": 20},
            "SKU003": {"name": "Product C", "quantity": 200, "reorder_point": 100, "leadTimeDays": 10, "location": "Zone-C", "safetyStock": 50},
            "SKU004": {"name": "Product D", "quantity": 50, "reorder_point": 25,  "leadTimeDays": 3, "location": "Zone-A", "safetyStock": 15},
            "SKU005": {"name": "Product E", "quantity": 75, "reorder_point": 60,  "leadTimeDays": 14, "location": "Zone-B", "safetyStock": 30}
        }
    }

    transactions = [
        {"product_id": "SKU001", "type": "sale", "quantity": 10, "timestamp": "2024-11-01T10:30:00Z"},
        {"product_id": "SKU001", "type": "PURCHASE", "quantity": 100, "timestamp": "2024-11-01T14:00:00Z"},
        {"product_id": "SKU002", "type": "sale", "quantity": 15, "timestamp": "2024-11-01T11:15:00Z"},
        {"product_id": "SKU002", "type": "RETURN", "quantity": 5, "timestamp": "2024-11-01T12:00:00Z"},
        {"product_id": "SKU003", "type": "sale", "quantity": 50, "timestamp": "2024-11-01T09:00:00Z"},
        {"product_id": "SKU004", "type": "sale", "quantity": 12, "timestamp": "2024-11-01T13:30:00Z"},
        {"product_id": "SKU005", "type": "PURCHASE", "quantity": 200,  "timestamp": "2024-11-01T15:00:00Z"},
    ]

    updated_inventory, log = processTransactions(inventory, transactions)
    print("\nTransaction Log:")
    for entry in log:
        print(entry)

    print("\nStock Alerts:")
    alerts = getStockAlerts(updated_inventory, {"default_reorder": 10})
    for alert in alerts:
        print(alert)
