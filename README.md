# Cricket Match Analysis

This project analyses cricket data (IPL, ODI, T20I, Test) from **Cricsheet JSON datasets** and builds an interactive **Power BI dashboard**.

## 📂 Project Structure

```
Cricket match Analysis/
│── IPL/                  # Raw IPL JSON files
│── ODI/                  # Raw ODI JSON files
│── T20/                  # Raw T20 JSON files
│── Test/                 # Raw Test JSON files
│── CSVs/                 # Converted CSVs from JSON files
│── cricket.db            # SQLite database storing all formats
│── db.py                 # Script to load CSVs into SQLite DB
│── run_queries.py        # Script to run 20 queries and save results to CSVs
│── Query_Results/        # Folder containing query output CSVs
│── Cricket_Analysis.pbix # Power BI dashboard file (built manually)
│── README.md             # Documentation
```

---

## ⚙️ Step 1: Convert JSON to CSV
The Cricsheet JSON files are parsed and converted into CSV format using Python.

```python
import pandas as pd
import json, os

# Example for IPL
input_folder = "IPL"
output_csv = "CSVs/t20_matches.csv"

data = []
for file in os.listdir(input_folder):
    if file.endswith(".json"):
        with open(os.path.join(input_folder, file)) as f:
            match = json.load(f)
            # Flatten JSON into rows (batter, bowler, runs, etc.)
            # Append to data list...

df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)
```

Repeat for ODI, T20I, and Test.

---

## ⚙️ Step 2: Load CSVs into SQLite DB
`db.py` creates a SQLite database (`cricket.db`) and loads all CSVs.

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("cricket.db")
t20_df = pd.read_csv("CSVs/t20_matches.csv")
odi_df = pd.read_csv("CSVs/odi_matches.csv")
test_df = pd.read_csv("CSVs/test_matches.csv")

t20_df.to_sql("t20_matches", conn, if_exists="replace", index=False)
odi_df.to_sql("odi_matches", conn, if_exists="replace", index=False)
test_df.to_sql("test_matches", conn, if_exists="replace", index=False)

conn.close()
```

---

## ⚙️ Step 3: Run SQL Queries
`run_queries.py` executes **20 advanced queries** (batting, bowling, team, records) and saves results as CSVs inside `Query_Results/`.

Example:
```sql
-- Top 10 Run Scorers (All Formats)
SELECT batter, SUM(runs_batter) AS total_runs
FROM (
    SELECT batter, runs_batter FROM t20_matches
    UNION ALL
    SELECT batter, runs_batter FROM odi_matches
    UNION ALL
    SELECT batter, runs_batter FROM test_matches
)
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;
```

---

## 📊 Step 4: Power BI Dashboard
1. Open **Power BI Desktop**
2. Load all CSVs from `Query_Results/`
3. Create 5 dashboard pages:
   - **Overview**
   - **Batting Analysis**
   - **Bowling Analysis**
   - **Team Analysis**
   - **Records & Specials**
4. Style using **dark theme** + slicers for **Year / Player / Team**.

---

## 🚀 How to Run
1. Clone this repo / copy files
2. Install requirements:
   ```bash
   pip install pandas
   ```
3. Run scripts:
   ```bash
   python db.py
   python run_queries.py
   ```
4. Open `Cricket_Analysis.pbix` in Power BI Desktop.

---

## 📌 Deliverables
- **SQLite Database:** `cricket.db`
- **20 SQL Query Outputs:** `Query_Results/*.csv`
- **Interactive Dashboard:** `Cricket_Analysis.pbix`
- **Documentation:** `README.md`

---

## 📖 Author
👤 Thiyagarajan 
📌 Role: Data Analyst / Data Scientist  
