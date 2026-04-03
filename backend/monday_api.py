import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")

URL = "https://api.monday.com/v2"

headers = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json"
}


def fetch_board_items(board_id, retries=3):
    query = f"""
    query {{
        boards(ids: {board_id}) {{
            columns {{
                id
                title
            }}
            items_page(limit: 500) {{
                items {{
                    id
                    name
                    column_values {{
                        id
                        text
                        value
                    }}
                }}
            }}
        }}
    }}
    """

    for attempt in range(retries):
        try:
            response = requests.post(
                URL,
                json={"query": query},
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()

            print(f"⚠️ API Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Network Error (Attempt {attempt+1}): {e}")

        time.sleep(2)

    # Final fallback
    return None