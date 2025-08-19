import sqlite3
import pandas as pd
import os

# Connect to your cricket database
conn = sqlite3.connect("cricket.db")

# Folder to save CSV results
output_folder = "Query_Results"
os.makedirs(output_folder, exist_ok=True)

# Dictionary of query name and SQL
queries = {
    "Top_10_Run_Scorers_All_Formats": """
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
    """,

    "Top_10_Six_Hitters_IPL": """
    SELECT batter, COUNT(*) AS sixes
    FROM t20_matches
    WHERE runs_batter = 6
    GROUP BY batter
    ORDER BY sixes DESC
    LIMIT 10;
    """,

    "Best_Strike_Rate_IPL": """
    SELECT batter,
           ROUND(SUM(runs_batter) * 100.0 / COUNT(*), 2) AS strike_rate,
           COUNT(*) AS balls_faced
    FROM t20_matches
    GROUP BY batter
    HAVING COUNT(*) >= 200
    ORDER BY strike_rate DESC
    LIMIT 10;
    """,

    "Batsmen_With_Most_Centuries_ODI": """
    SELECT batter, COUNT(DISTINCT date) AS centuries
    FROM (
        SELECT batter, date,
               SUM(runs_batter) AS runs_in_match
        FROM odi_matches
        GROUP BY batter, date
        HAVING SUM(runs_batter) >= 100
    )
    GROUP BY batter
    ORDER BY centuries DESC
    LIMIT 10;
    """,

    "Top_Test_Partnerships": """
    SELECT team1 AS batting_team, SUM(runs_batter) AS partnership_runs
    FROM test_matches
    GROUP BY team1
    ORDER BY partnership_runs DESC
    LIMIT 10;
    """,

    "Top_10_Wicket_Takers_IPL": """
    SELECT bowler, COUNT(wicket_kind) AS wickets
    FROM t20_matches
    WHERE wicket_kind IS NOT NULL
    GROUP BY bowler
    ORDER BY wickets DESC
    LIMIT 10;
    """,

    "Best_Economy_ODI": """
    SELECT bowler,
           ROUND(SUM(runs_total) * 6.0 / COUNT(*), 2) AS economy_rate,
           COUNT(*) AS balls_bowled
    FROM odi_matches
    GROUP BY bowler
    HAVING COUNT(*) >= 500
    ORDER BY economy_rate ASC
    LIMIT 10;
    """,

    "Most_Maidens_Test": """
    SELECT bowler, COUNT(*) AS maiden_overs
    FROM (
        SELECT bowler, over, SUM(runs_total) AS runs_in_over
        FROM test_matches
        GROUP BY bowler, over
        HAVING SUM(runs_total) = 0
    )
    GROUP BY bowler
    ORDER BY maiden_overs DESC
    LIMIT 10;
    """,

    "Five_Wicket_Hauls_Test": """
    SELECT bowler, COUNT(DISTINCT date) AS five_wicket_hauls
    FROM (
        SELECT bowler, date,
               COUNT(*) AS wickets_in_match
        FROM test_matches
        WHERE wicket_kind IS NOT NULL
        GROUP BY bowler, date
        HAVING COUNT(*) >= 5
    )
    GROUP BY bowler
    ORDER BY five_wicket_hauls DESC;
    """,

    "Most_Dot_Balls_IPL": """
    SELECT bowler, COUNT(*) AS dot_balls
    FROM t20_matches
    WHERE runs_total = 0
    GROUP BY bowler
    ORDER BY dot_balls DESC
    LIMIT 10;
    """,

    "T20I_Teams_Highest_Win_Percentage": """
    SELECT winner,
           ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM t20_matches), 2) AS win_percentage
    FROM t20_matches
    WHERE winner IS NOT NULL
    GROUP BY winner
    ORDER BY win_percentage DESC;
    """,

    "ODI_Teams_Highest_Avg_Runs": """
    SELECT team1 AS team, ROUND(AVG(runs_total), 2) AS avg_runs
    FROM odi_matches
    GROUP BY team1
    ORDER BY avg_runs DESC;
    """,

    "Test_Teams_Most_Innings_Wins": """
    SELECT winner, COUNT(*) AS innings_wins
    FROM test_matches
    WHERE winner IS NOT NULL
      AND wicket_kind IS NOT NULL
    GROUP BY winner
    ORDER BY innings_wins DESC;
    """,

    "Most_Matches_All_Formats": """
    SELECT team, COUNT(*) AS total_matches
    FROM (
        SELECT team1 AS team FROM t20_matches
        UNION ALL
        SELECT team2 FROM t20_matches
        UNION ALL
        SELECT team1 FROM odi_matches
        UNION ALL
        SELECT team2 FROM odi_matches
        UNION ALL
        SELECT team1 FROM test_matches
        UNION ALL
        SELECT team2 FROM test_matches
    )
    GROUP BY team
    ORDER BY total_matches DESC;
    """,

    "Avg_Runs_Per_Over_IPL_By_Year": """
    SELECT SUBSTR(date, 1, 4) AS year,
           ROUND(AVG(runs_total), 2) AS avg_runs_per_over
    FROM t20_matches
    GROUP BY year
    ORDER BY year;
    """,

    "Highest_Scoring_Test_Matches": """
    SELECT date, venue, team1, team2, SUM(runs_total) AS total_runs
    FROM test_matches
    GROUP BY date, venue, team1, team2
    ORDER BY total_runs DESC
    LIMIT 10;
    """,

    "Lowest_Team_Totals_IPL": """
    SELECT date, batting_team, SUM(runs_total) AS team_total
    FROM t20_matches
    GROUP BY date, batting_team
    ORDER BY team_total ASC
    LIMIT 10;
    """,

    "Century_And_FiveWickets_Same_Match": """
    SELECT batter
    FROM (
        SELECT batter, date, SUM(runs_batter) AS runs_in_match
        FROM (
            SELECT batter, date, runs_batter FROM t20_matches
            UNION ALL
            SELECT batter, date, runs_batter FROM odi_matches
            UNION ALL
            SELECT batter, date, runs_batter FROM test_matches
        )
        GROUP BY batter, date
        HAVING runs_in_match >= 100
    ) AS centuries
    INTERSECT
    SELECT bowler
    FROM (
        SELECT bowler, date, COUNT(*) AS wickets_in_match
        FROM (
            SELECT bowler, date, wicket_kind FROM t20_matches
            UNION ALL
            SELECT bowler, date, wicket_kind FROM odi_matches
            UNION ALL
            SELECT bowler, date, wicket_kind FROM test_matches
        )
        WHERE wicket_kind IS NOT NULL
        GROUP BY bowler, date
        HAVING wickets_in_match >= 5
    );
    """,

    "Fifty_Plus_In_All_Formats": """
    SELECT batter
    FROM (
        SELECT batter FROM t20_matches
        GROUP BY batter, date
        HAVING SUM(runs_batter) >= 50
    )
    INTERSECT
    SELECT batter
    FROM (
        SELECT batter FROM odi_matches
        GROUP BY batter, date
        HAVING SUM(runs_batter) >= 50
    )
    INTERSECT
    SELECT batter
    FROM (
        SELECT batter FROM test_matches
        GROUP BY batter, date
        HAVING SUM(runs_batter) >= 50
    );
    """
}

# Run each query and save results
for name, query in queries.items():
    df = pd.read_sql_query(query, conn)
    output_path = os.path.join(output_folder, f"{name}.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Saved: {output_path}")

# Close connection
conn.close()

print("\n🎉 All queries executed and CSVs saved in 'Query_Results' folder!")
