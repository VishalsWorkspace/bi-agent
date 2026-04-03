from monday_api import fetch_board_items
from utils import clean_number, clean_date


# 🔹 DEALS
def get_clean_deals(board_id):
    data = fetch_board_items(board_id)

    # 🛡️ SAFEGUARD (API failure)
    if not data or "data" not in data or not data["data"].get("boards"):
        print("⚠️ API Error (Deals):", data)
        return []

    board = data["data"]["boards"][0]

    columns = board.get("columns", [])
    if not columns:
        print("⚠️ Columns missing in API response")
        return []

    items = board.get("items_page", {}).get("items", [])

    col_map = {col["id"]: col["title"].lower() for col in columns}

    cleaned = []

    for item in items:
        record = {
            "id": item.get("id"),  # ✅ IMPORTANT FOR DEDUP
            "name": item.get("name"),
            "value": 0,
            "status": None,
            "stage": None,
            "probability": None,
            "sector": None,
            "close_date": None
        }

        for col in item.get("column_values", []):
            col_id = col.get("id")
            text = col.get("text")

            if not text:
                continue

            title = col_map.get(col_id, "")

            if "value" in title:
                record["value"] = clean_number(text)
            elif "status" in title:
                record["status"] = text
            elif "stage" in title:
                record["stage"] = text
            elif "probability" in title:
                record["probability"] = text
            elif "sector" in title:
                record["sector"] = text
            elif "date" in title:
                record["close_date"] = clean_date(text)

        cleaned.append(record)

    # 🔥 PERFECT DEDUP (USING ID)
    seen = set()
    unique_deals = []

    for d in cleaned:
        if d["id"] not in seen:
            seen.add(d["id"])
            unique_deals.append(d)

    return unique_deals


# 🔹 WORK ORDERS
def get_clean_work_orders(board_id):
    data = fetch_board_items(board_id)

    # 🛡️ SAFEGUARD
    if not data or "data" not in data or not data["data"].get("boards"):
        print("⚠️ API Error (Work Orders):", data)
        return []

    board = data["data"]["boards"][0]

    columns = board.get("columns", [])
    items = board.get("items_page", {}).get("items", [])

    col_map = {col["id"]: col["title"].lower() for col in columns}

    cleaned = []

    for item in items:
        record = {
            "name": item.get("name"),
            "sector": None,
            "status": None,
            "execution_status": None,
            "amount_total": 0,
            "amount_collected": 0,
            "amount_receivable": 0
        }

        for col in item.get("column_values", []):
            col_id = col.get("id")
            text = col.get("text")

            if not text:
                continue

            title = col_map.get(col_id, "")

            if "sector" in title:
                record["sector"] = text
            elif "execution" in title:
                record["execution_status"] = text
            elif "status" in title:
                record["status"] = text
            elif "collected" in title:
                record["amount_collected"] = clean_number(text)
            elif "receivable" in title:
                record["amount_receivable"] = clean_number(text)
            elif "amount" in title:
                record["amount_total"] = clean_number(text)

        cleaned.append(record)

    return cleaned


# 🔥 BUSINESS LOGIC

def total_pipeline_value(deals):
    return sum(d.get("value", 0) for d in deals)


def deals_by_stage(deals):
    result = {}

    for d in deals:
        stage = d.get("stage")

        if not stage or stage.lower() == "deal stage":
            continue

        value = d.get("value", 0)

        if value == 0:
            continue

        result[stage] = result.get(stage, 0) + value

    return result


def revenue_by_sector(work_orders):
    result = {}

    for w in work_orders:
        sector = w.get("sector")
        value = w.get("amount_total", 0)

        if not sector or value == 0:
            continue

        result[sector] = result.get(sector, 0) + value

    return result


def conversion_summary(deals):
    total = len(deals)

    high = len([d for d in deals if d.get("probability") == "High"])
    medium = len([d for d in deals if d.get("probability") == "Medium"])
    low = len([d for d in deals if d.get("probability") == "Low"])

    return {
        "total_deals": total,
        "high": high,
        "medium": medium,
        "low": low
    }