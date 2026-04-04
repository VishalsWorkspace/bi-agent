# 🚀 AI Business Intelligence Agent (Monday.com)

An AI-powered Business Intelligence Agent that converts natural language queries into actionable insights using Monday.com data.

---

## 🔥 Features

* 📊 Total Pipeline Value
* 📂 Deals by Stage (Value + Count)
* 🏢 Revenue by Sector
* 🎯 Conversion Summary
* 🔍 Open Deals Analysis
* 🧠 Reasoning Trace (Explainability)

---

## 🧠 Example Queries

* What is total pipeline?
* Show deals by stage
* How many deals in each stage?
* Revenue by sector
* Conversion summary

---

## ⚙️ Tech Stack

* Python
* Streamlit (UI)
* Monday.com GraphQL API
* Custom Rule-based Agent

---

## 🏗️ Architecture

* `monday_api.py` → Fetch data
* `tools.py` → Data processing
* `main.py` → Agent logic
* `app.py` → UI (Streamlit)

---

## 🔐 Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add `.env`:

```
MONDAY_API_KEY=your_key_here
```

---

## 🌐 Live Demo

👉 https://bi-agent-assignment.streamlit.app/

---

## 🧠 Design Decisions

* Rule-based intent parsing for reliability
* Safe API handling with fallbacks
* Modular architecture for scalability
* Explainable reasoning trace

---

## ⚠️ Notes

* Data is fetched live from Monday.com
* Results depend on API data quality
