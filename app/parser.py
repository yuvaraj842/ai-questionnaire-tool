import pandas as pd

def parse_questionnaire(file_path):
    df = pd.read_csv(file_path)
    questions = df.iloc[:,0].tolist()
    return questions