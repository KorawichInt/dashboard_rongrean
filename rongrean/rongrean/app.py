from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import os


def read_and_save_json(url, save_path):
    # if os.path.exists(save_path):
    #     print(f"File already exists at {save_path}")
    #     return
    
    df = pd.read_json(url)
    print(df)
    # df.to_json(save_path)
    pass


if __name__ == "__main__":
    url = "https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json"
    data_path = "student_data"
    student_data = read_and_save_json(url, data_path)