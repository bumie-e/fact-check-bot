import pandas as pd

def preprocess(file_dir):
   #Open the file
    with open(file_dir, "r", encoding='unicode_escape') as file:
      content = file.read().replace('\n', '')

    sentences = list(map(str.strip, content.split(".")))
    df = pd.DataFrame()
    df["claim"] = pd.Series(sentences)


    return df