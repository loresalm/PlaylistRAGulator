import chromadb  # type: ignore
import time
import ollama  # type: ignore
import pandas as pd  # type: ignore
import sys
import json

print("load config")
config_file_path = 'data/user_inputs/config.json'
with open(config_file_path, 'r') as json_file:
    config = json.load(json_file)
# Assign the values to variables
embedmodel = config.get("embedmodel")
nb_songs = config.get("nb_songs")
adj_path = config.get("adj_path")
img_desc_path = config.get("img_desc_path")
chroma_db_path = config.get("chroma_db_path")
output_csv_path = config.get("output_path")
dataset_in_path = config.get("dataset_in_path")
output_path = config.get("output_path")
use_img = config.get("use_img")
use_adj = config.get("use_adj")
print("config loaded")


######################
#                    #
#  load user inputs  #
#                    #
######################
start_time = time.time()
if use_img:
    with open(img_desc_path, 'r') as file:
        desc = file.read().strip()
    prompt_img = f"fit the vibe of following description: {desc}"
else:
    prompt_img = ""
if use_adj:
    adj_df = pd.read_csv(adj_path)
    adj = ", ".join(adj_df["adjective"].values)
    prompt_adj = f"fit this adjectives: {adj}"
else:
    prompt_adj = ""
print("user inputs loaded")

######################
#                    #
#  load embeddings   #
#                    #
######################
chroma_client = chromadb.PersistentClient(path=chroma_db_path)
chroma_collection = chroma_client.get_or_create_collection("mydocs")
print("embeddings loaded")
######################
#                    #
#  query the vect db #
#                    #
######################
query = f"""
    I'm looking for a set of songs that: {prompt_adj}, {prompt_img}."""
queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']
relevantdocs = chroma_collection.query(query_embeddings=[queryembed],
                                       n_results=nb_songs)
print("query done")
######################
#                    #
#   select songs     #
#                    #
######################
slect_ids = relevantdocs["ids"][0]
sonivar_df = pd.read_csv(dataset_in_path)
output_data = {
        "Id": [],
        "song_name": [],
        "billboard": []
    }
for i, idx in enumerate(slect_ids):
    song = sonivar_df["song_name"].values[int(idx)]
    billboard = sonivar_df["billboard"].values[int(idx)]
    output_data["Id"].append(idx)
    output_data["song_name"].append(song)
    output_data["billboard"].append(billboard)

# Create a DataFrame
output_df = pd.DataFrame(output_data)
# Save DataFrame to CSV
output_df.to_csv(output_path, index=False)
end_time = time.time()
print(f"playlist done in {round((end_time - start_time)/60, 2)} min")
sys.exit(0)
