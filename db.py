import pandas as pd
from sqlalchemy import create_engine

# Create SQLite database file
engine = create_engine("sqlite:///cricket.db")

# Read and save each CSV into the database
ipl_df= pd.read_csv(r"E:\Cricket match Analysis\CSVs\ipl_matches.csv")
t20_df = pd.read_csv(r"E:\Cricket match Analysis\CSVs\t20_matches.csv")
odi_df = pd.read_csv(r"E:\Cricket match Analysis\CSVs\odi_matches.csv")
test_df = pd.read_csv(r"E:\Cricket match Analysis\CSVs\test_matches.csv")

ipl_df.to_sql("ipl_matches", engine, if_exists="replace", index=False)
t20_df.to_sql("t20_matches", engine, if_exists="replace", index=False)
odi_df.to_sql("odi_matches", engine, if_exists="replace", index=False)
test_df.to_sql("test_matches", engine, if_exists="replace", index=False)

print("✅ All match data saved to cricket.db")
