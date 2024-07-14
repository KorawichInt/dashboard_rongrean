from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import os

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def read_and_save_json(url, save_path):
    # check if file already exists
    if os.path.exists(save_path):
        print(f"File already exists at {save_path}")
        df = pd.read_json(save_path)
        return df
    
    # convert json to dataframe and save json file
    df = pd.read_json(url)
    df.to_json(save_path)
    print(f"Readed and saved to {save_path}")
    return df

url = "https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json"
data_path = "student_data"
student_df = read_and_save_json(url, data_path)

filtered_df = student_df.loc[:, ["schools_province", "totalmale", "totalfemale", "totalstd"]]
# app.layout = html.Div(style={"backgroundColor": colors["background"]}, 
app.layout = html.Div(style={"backgroundColor": colors["background"]},
    children = [
        # Header (Content)
        html.H1(
            # children = "Mor.6 student (Graduated year 2566)"),
            children = "จำนวนนักเรียนมัธยมศึกษาปีที่ 6 ที่จบการศึกษา ปีการศึกษา 2566",
            style = {
                "textAlign": "center",
                "color": colors["text"]
            }
        ),

        # Province dropdown
        html.Label(
            "จังหวัด", style = {"color": colors["text"]}
        ),
        dcc.Dropdown(filtered_df["schools_province"]),


    ],
)
# ])



if __name__ == "__main__":
    app.run(debug=True)