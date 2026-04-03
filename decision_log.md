# 🧠 Decision Log

## 1. Why Rule-Based Agent?

Chosen for deterministic, reliable outputs within limited assignment scope.

## 2. Why Streamlit?

Fast deployment, clean UI, ideal for data-driven apps.

## 3. API Handling

Added safeguards for:

* Missing fields
* API failures
* Empty responses

## 4. Data Cleaning

Handled:

* Currency formatting
* Missing values
* Inconsistent schema

## 5. Tradeoffs

* Did not use LLM → avoids hallucination
* Limited query flexibility → ensures accuracy

## 6. Future Improvements

* Add LLM for flexible queries
* Add caching for performance
* Add dashboards & charts
