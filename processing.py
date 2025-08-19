import os
import json
import pandas as pd

def process_matches(folder_path, match_type, output_csv):
    all_rows = []

    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            with open(os.path.join(folder_path, file), encoding="utf-8") as f:
                data = json.load(f)

            # Extract match metadata
            info = data.get("info", {})
            date = info.get("dates", [""])[0]
            venue = info.get("venue", "")
            teams = info.get("teams", ["", ""])
            winner = info.get("outcome", {}).get("winner", "")

            # Loop over innings
            for innings in data.get("innings", []):
                team = innings.get("team", "")
                for over_info in innings.get("overs", []):
                    over_num = over_info.get("over", None)
                    for delivery in over_info.get("deliveries", []):
                        row = {
                            "match_type": match_type,
                            "date": date,
                            "venue": venue,
                            "team1": teams[0],
                            "team2": teams[1],
                            "batting_team": team,
                            "over": over_num,
                            "batter": delivery.get("batter", ""),
                            "bowler": delivery.get("bowler", ""),
                            "runs_batter": delivery.get("runs", {}).get("batter", 0),
                            "runs_extras": delivery.get("runs", {}).get("extras", 0),
                            "runs_total": delivery.get("runs", {}).get("total", 0),
                            "extras_type": list(delivery.get("extras", {}).keys())[0] if "extras" in delivery else None,
                            "wicket_kind": delivery["wickets"][0]["kind"] if "wickets" in delivery else None,
                            "player_out": delivery["wickets"][0]["player_out"] if "wickets" in delivery else None,
                            "winner": winner
                        }
                        all_rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(all_rows)

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved {match_type} data to {output_csv}")


# ---- PROCESS ALL ----
process_matches("IPL", "IPL", "ipl_matches.csv")
process_matches("ODIs", "ODIs", "odi_matches.csv")
process_matches("T20", "T20", "t20_international_matches.csv")
process_matches("Test", "Test", "test_matches.csv")
