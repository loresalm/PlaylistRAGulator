import chromadb  # type: ignore
import time
import ollama  # type: ignore
import pandas as pd  # type: ignore
import sys
import json

script_start_time = time.time()
print("load config")
config_file_path = 'data/config.json'
with open(config_file_path, 'r') as json_file:
    config = json.load(json_file)
# Assign the values to variables
embedmodel = config.get("embedmodel")
dataset_in_path = config.get("dataset_in_path")
chroma_db_path = config.get("chroma_db_path")
nb_row_embed = config.get("nb_row_embed")
print("config loaded")
######################
#                    #
#   make embeddings  #
#                    #
######################
print("make embeddings")
# load embeddings
chroma_client = chromadb.PersistentClient(path=chroma_db_path)
try:
    chroma_client.delete_collection("mydocs")
    print("Collection 'mydocs' cleared.")
except Exception as e:
    print(f"No existing collection to clear. ({str(e)})")

chroma_collection = chroma_client.get_or_create_collection("mydocs")
sonivar_df = pd.read_csv(dataset_in_path)

nb_row_embed = int(len(sonivar_df))
print(f"embedding {nb_row_embed} songs")

for index, row in sonivar_df[:nb_row_embed].iterrows():
    chunk = f"""
        song_name:{row['song_name']},
        billboard: {row['billboard']},
        artists: {row['artists']},
        popularity: {row['popularity']}
        explicit:{row['explicit']},
        song_type: {row['song_type']},
        duration_ms: {row['duration_ms']},
        acousticness: {row['acousticness']}
        danceability:{row['danceability']},
        energy: {row['energy']},
        instrumentalness: {row['instrumentalness']},
        liveness: {row['liveness']}
        loudness: {row['loudness']}
        speechiness: {row['speechiness']}
        valence: {row['valence']}
        tempo: {row['tempo']}"""
    embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
    chroma_collection.add([str(index)],
                          [embed],
                          documents=[chunk],
                          metadatas={"source": index})
print("embeddings done")
script_stop_time = time.time()
print("Time ellapsed:", script_stop_time-script_start_time)
sys.exit(0)
