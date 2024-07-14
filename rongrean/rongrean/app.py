from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import os

app = Dash(__name__)

# colors = {
#     "background": "#111111",
#     "ligh_blue_text": "#7FDBFF",
#     "black_text": "#0D0000"
# }

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
# app.layout = html.Div(style={"backgroundColor": colors["background"], "color": colors["ligh_blue_text"]},
app.layout = html.Div([
    # Header (Content)
    html.H2("จำนวนนักเรียนมัธยมศึกษาปีที่ 6 ที่จบการศึกษา ปีการศึกษา 2566"),

    # Dropdown for selecting province
    html.Label("จังหวัดที่ต้องการแสดง"),
    dcc.Dropdown(filtered_df["schools_province"].unique(), "กรุงเทพมหานคร"),

    # Checkbox for selecting genders to display
    html.Label("ประเภทที่ต้องการแสดง"),
    dcc.Checklist(["ทั้งหมด", "นาย", "นางสาว"], ["ทั้งหมด"]),

    dcc.Graph(id="bar-graph")
])

def update_graph(selected_province, selected_data):
    # Filter data based on selected province
    filtered_province_df = filtered_df[filtered_df["schools_province"] == selected_province]
    
    # Create a bar graph
    fig = px.bar(
        filtered_province_df,
        x="schools_province",
        y=selected_data,
        barmode="group"
    )
    
    return fig



if __name__ == "__main__":
    app.run(debug=True)