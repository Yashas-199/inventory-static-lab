from __future__ import annotations
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Global variable
stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> None:
    """Add quantity to an item. item must be a non-empty string, qty a non-negative int."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an integer")
    if qty < 0:
        raise ValueError("qty must be non-negative")

    prev = stock_data.get(item, 0)
    stock_data[item] = prev + qty
    entry = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(entry)
    logging.info(entry)


def remove_item(item: str, qty: int) -> None:
    """Remove quantity from an item. Raises KeyError if item missing."""
    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an integer")
    if qty <= 0:
        raise ValueError("qty must be positive")

    if item not in stock_data:
        raise KeyError(f"Item '{item}' not found in stock")

    if stock_data[item] < qty:
        raise ValueError(f"Not enough stock for '{item}' to remove {qty}")

    stock_data[item] -= qty
    if stock_data[item] == 0:
        del stock_data[item]
    logging.info(f"{datetime.now()}: Removed {qty} of {item}")


def get_qty(item: str) -> int:
    """Return current quantity of item, 0 if not present."""
    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load stock_data from a JSON file. If file missing or invalid JSON, start with empty dict."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("inventory file must contain a JSON object")
        # Convert numeric values to ints safely
        cleaned: Dict[str, int] = {}
        for k, v in data.items():
            if not isinstance(k, str):
                logging.warning("Skipping non-string key in inventory file: %r", k)
                continue
            try:
                cleaned[k] = int(v)
            except (TypeError, ValueError):
                logging.warning("Skipping key with non-integer value: %s=%r", k, v)
        stock_data = cleaned
        logging.info("Loaded inventory from %s", file)
    except FileNotFoundError:
        logging.warning("Inventory file %s not found — starting with empty inventory", file)
        stock_data = {}
    except json.JSONDecodeError as exc:
        logging.error("Invalid JSON in %s: %s", file, exc)
        stock_data = {}
    except Exception as exc:  # catch unexpected errors and log them
        logging.exception("Unexpected error while loading data: %s", exc)
        stock_data = {}


def save_data(file: str = "inventory.json") -> None:
    """Save stock_data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        logging.info("Saved inventory to %s", file)
    except OSError as exc:
        logging.error("Failed to write inventory to %s: %s", file, exc)
        raise


def print_data() -> None:
    """Print a human-readable items report."""
    print("Items Report")
    for name, qty in stock_data.items():
        print(name, "->", qty)


def check_low_items(threshold: int = 5) -> List[str]:
    """Return list of items with qty strictly less than threshold."""
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold must be a non-negative integer")
    return [name for name, qty in stock_data.items() if qty < threshold]


def main() -> None:
    
    add_item("apple", 10)
    try:
        # banana negative qty -> should raise
        add_item("banana", 2)
    except Exception as exc:
        logging.error("Error adding banana: %s", exc)

    try:
        # invalid types -> will raise TypeError now
        add_item("orange", 10)
    except Exception as exc:
        logging.error("Type error: %s", exc)

    try:
        remove_item("apple", 3)
    except Exception as exc:
        logging.error("Error removing apple: %s", exc)

    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
