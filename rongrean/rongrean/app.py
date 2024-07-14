from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import os


def read_and_save_json(url, save_path):
    # check if file already exists
    if os.path.exists(save_path):
        print(f"File already exists at {save_path}")
        return
    
    # convert json to dataframe and save json file
    df = pd.read_json(url)
    df.to_json(save_path)
    print(f"Readed and saved to {save_path}")
    


if __name__ == "__main__":
    url = "https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json"
    data_path = "student_data"
    student_data = read_and_save_json(url, data_path)