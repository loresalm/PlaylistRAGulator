import pandas as pd  # type: ignore
import sys
import json


print("load config")
config_file_path = 'data/config.json'
with open(config_file_path, 'r') as json_file:
    config = json.load(json_file)
# Assign the values to variables
dataset_in_path = config.get("dataset_in_path")
songs_path = config.get("songs_path")
features_path = config.get("features_path")
print("config loaded")

print("preprocessing")
songs_df = pd.read_csv(songs_path, delimiter='\t')
features_df = pd.read_csv(features_path, delimiter='\t')
sonivar_df = pd.merge(songs_df,
                      features_df,
                      on="song_id",
                      how="inner").dropna()
sonivar_df.to_csv(dataset_in_path, index=False)
print("preprocessing done")
sys.exit(0)
