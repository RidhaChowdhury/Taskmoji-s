from todoist_api_python.api import TodoistAPI
from sentence_transformers import SentenceTransformer
import re
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import emoji
import csv

# TODO: check for emojis with analyze
def is_task_emoji(task):
  """Returns True if the task starts with an emoji, False otherwise."""
  emoji_pattern = re.compile(r'^(?:[\U00010000-\U0010ffff])')
  return emoji_pattern.match(task) is not None

def get_embedding_emoji(embedding, df):
    similarities = cosine_similarity([embedding], np.stack(df['Embedding'].to_numpy()))
    max_sim_idx = np.argmax(similarities)
    return df.iloc[max_sim_idx]['Emoji']

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') # use multilingual models for texts with non-english characters
api = TodoistAPI("54d4b9a82bc75523fcce6fee381e7f97aafe9ac1")


print("Loading emoji dataset")
df = pd.read_csv('unicode_emojis_and_names.csv')

print("Encoding emoji names")
df['Embedding'] = df['Name'].apply(model.encode)

try:
    tasks = api.get_tasks()
    for task in tasks:
        if is_task_emoji(task.content):
            continue
        content, content_embedding = task.content, model.encode(task.content)
        new_name = get_embedding_emoji(model.encode(content), df) + content
        try:
            is_success = api.update_task(task_id=task.id, content=new_name)
            if is_success:
                print(f"Success!Changing {content} to {new_name}")
            else:
                print(f"Failed!Changing {content} to {new_name}")

        except Exception as error:
            print(error)

except Exception as error:
    print(error)