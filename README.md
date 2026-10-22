# 🏏 Cricbuzz LiveStats: Real-Time Cricket Telemetry & SQL Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)](https://sqlite.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-purple.svg)](https://plotly.com/)

A comprehensive cricket analytics platform that integrates live match telemetry from the **Cricbuzz REST API** with a normalized **3NF SQL Database**, solving **25 advanced business intelligence queries** and providing administrative **CRUD operations** through a multi-page **Streamlit** dashboard.

---

## 📌 Features & Architecture

- **Multi-Page Web Dashboard:** Built with Streamlit (`Home`, `Live Matches`, `Top Stats`, `SQL Analytics`, `CRUD Operations`).
- **Real-Time API Telemetry:** Real-time match telemetry, live scores, and venue details via Cricbuzz REST client with an offline mock fallback engine.
- **Normalized 3NF Database:** 9 relational tables (`teams`, `venues`, `series`, `matches`, `players`, `batting_stats`, `bowling_stats`, `fielding_stats`, `partnerships`).
- **25 SQL Business Intelligence Queries:** 
  - *Beginner (Q1–Q8):* Nationality filters, recent fixtures, venue capacity, format records.
  - *Intermediate (Q9–Q16):* All-rounders, home vs. away records, 100+ partnerships, close-match performers.
  - *Advanced (Q17–Q25):* Toss advantages, limited-overs economy, multi-factor rating formula, head-to-head predictions, and career trajectory evolution.
- **Administrative CRUD Management:** Interactive form-based interface to Create, Read, Update, and Delete player records with real-time UI updates.

---

## 📁 Repository Structure

```text
cricbuzz_livestats/
├── app.py                     # Main dashboard entry point & KPI overview
├── requirements.txt           # Python dependencies
├── README.md                  # Complete project documentation
├── database/
│   ├── db_manager.py          # Schema DDL and seed data generator
│   └── cricket_stats.db       # Relational SQLite database
├── api/
│   └── cricbuzz_client.py     # Cricbuzz REST client with fallback engine
├── services/
│   ├── analytics_service.py   # Complete 25 SQL queries with execution engine
│   └── crud_service.py        # Validated CRUD database handlers
└── pages/
    ├── 1_Home.py              # Architecture & problem statement
    ├── 2_Live_Matches.py      # Real-time scorecards and venues
    ├── 3_Top_Stats.py         # Batting & bowling leaderboards
    ├── 4_SQL_Analytics.py     # Interactive runner for all 25 queries + charts
    └── 5_CRUD_Operations.py   # Admin portal for database manipulation
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/nishajbabu/Cricbuzz-LiveStats-Analytics.git
cd Cricbuzz-LiveStats-Analytics
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python database/db_manager.py
```

### 4. Launch the Dashboard

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.
