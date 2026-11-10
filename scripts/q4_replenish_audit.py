"""Q4 replenishment audit helper.

Reads the store catalogue and produces replenishment decisions for items that
carry a reorder point in their product metadata.

A product is due for replenishment when its on-hand stock is *strictly* below
its reorder point. The restock target is three times the reorder point, and the
suggested order is the smallest multiple of the item's case pack that reaches it.

Output columns: SKU | Item | On Hand | Reorder Point | Shortfall | Suggested Order
"""

from math import ceil


def restock_target(reorder_point: int) -> int:
    return 3 * int(reorder_point)


def suggested_order(on_hand: int, reorder_point: int, case_pack: int) -> int:
    target = restock_target(reorder_point)
    if on_hand >= target:
        return 0
    gap = target - on_hand
    return int(ceil(gap / max(1, case_pack))) * max(1, case_pack)


def is_due(on_hand: int, reorder_point: int) -> bool:
    return on_hand < reorder_point


def build_row(product, metadata):
    on_hand = int(product["stock_quantity"])
    reorder = int(metadata["reorder_point"])
    pack = int(metadata.get("case_pack", 1))
    return {
        "SKU": product["sku"],
        "Item": product["name"],
        "On Hand": on_hand,
        "Reorder Point": reorder,
        "Shortfall": reorder - on_hand,
        "Suggested Order": suggested_order(on_hand, reorder, pack),
    }
