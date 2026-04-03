from tools import (
    get_clean_deals,
    get_clean_work_orders,
    total_pipeline_value,
    deals_by_stage,
    revenue_by_sector,
    conversion_summary
)

DEALS_BOARD = "5027611622"
WORK_BOARD = "5027611621"


# 💰 Formatting helpers
def format_currency(value):
    return f"₹{value:,.2f}"


def format_dict(data):
    lines = []
    for k, v in data.items():
        lines.append(f"{k}: {format_currency(v)}")
    return "\n".join(lines)


# 🤖 AI Agent
def run_agent(user_query):
    deals = get_clean_deals(DEALS_BOARD)
    work_orders = get_clean_work_orders(WORK_BOARD)

    trace = []
    query = user_query.lower()

    # 🛡️ GLOBAL SAFEGUARDS
    if deals is None or work_orders is None:
        return (
            "⚠️ API connection failed. Please check internet or try again."
        ), ["API failure"]

    if len(deals) == 0:
        return (
            "⚠️ No deal data available. Please check board/API."
        ), ["Empty deals"]

    # 🔥 OPEN PIPELINE
    if "open" in query and "pipeline" in query:
        trace.append("Filtered open deals pipeline")

        open_deals = [d for d in deals if d.get("status") == "Open"]
        result = total_pipeline_value(open_deals)

        return (
            f"📊 Open deals pipeline value is {format_currency(result)}"
        ), trace

    # 📊 TOTAL PIPELINE
    elif "pipeline" in query:
        trace.append("Called total_pipeline_value()")

        result = total_pipeline_value(deals)

        return (
            f"📊 Total pipeline value is {format_currency(result)}\n"
            f"👉 This represents the total potential deal value across all stages."
        ), trace

    # 🔢 COUNT BY STAGE
    elif "how many" in query and "stage" in query:
        trace.append("Count deals by stage")

        counts = {}
        for d in deals:
            stage = d.get("stage")
            if not stage:
                continue
            counts[stage] = counts.get(stage, 0) + 1

        return (
            "\n📊 Deal Count by Stage:\n" +
            "\n".join(f"{k}: {v}" for k, v in counts.items())
        ), trace

    # 📈 DEALS BY STAGE
    elif "stage" in query:
        trace.append("Called deals_by_stage()")

        result = deals_by_stage(deals)

        return (
            f"\n📈 Deals by Stage:\n{format_dict(result)}"
        ), trace

    # 🏢 REVENUE
    elif "revenue" in query:
        trace.append("Called revenue_by_sector()")

        result = revenue_by_sector(work_orders)

        return (
            f"\n🏢 Revenue by Sector:\n{format_dict(result)}"
        ), trace

    # 🎯 CONVERSION
    elif "conversion" in query or "probability" in query:
        trace.append("Called conversion_summary()")

        result = conversion_summary(deals)

        return (
            f"\n🎯 Deal Conversion Summary:\n"
            f"Total Deals: {result['total_deals']}\n"
            f"High: {result['high']}\n"
            f"Medium: {result['medium']}\n"
            f"Low: {result['low']}"
        ), trace

    # 🧠 SMART FALLBACK
    else:
        trace.append("Clarification required")

        return (
            "I understood your query, but currently I support:\n\n"
            "- Total pipeline value\n"
            "- Open deals pipeline\n"
            "- Deals by stage (value + count)\n"
            "- Revenue by sector\n"
            "- Conversion summary\n\n"
            "👉 Try asking:\n"
            "'What is total pipeline?'\n"
            "'Show deals by stage'\n"
            "'How many deals in each stage?'\n"
            "'Revenue by sector'\n"
            "'Conversion summary'\n\n"
            "I can be extended to support more advanced queries."
        ), trace


# 🚀 CLI ENTRY POINT
if __name__ == "__main__":
    print("\n🤖 AI BI Agent Ready!")
    print("Ask things like:")
    print("- What is total pipeline?")
    print("- Show deals by stage")
    print("- How many deals in each stage?")
    print("- Revenue by sector")
    print("- Conversion summary\n")

    while True:
        query = input("Ask something: ")

        answer, trace = run_agent(query)

        print("\n🤖 Answer:\n", answer)
        print("🔍 Trace:", trace)