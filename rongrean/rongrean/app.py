from dash import Dash, dcc, html, Input, Output, callback, dash_table
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

# Read json from url and save as a new json file
url = "https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json"
data_path = "student_data"
student_df = read_and_save_json(url, data_path)

filtered_df = student_df.loc[:, ["schools_province", "totalmale", "totalfemale", "totalstd"]]
filtered_df.columns = ["จังหวัด", "จำนวนนักเรียนชาย", "จำนวนนักเรียนหญิง", "จำนวนนักเรียนทั้งหมด"]
# app.layout = html.Div(style={"backgroundColor": colors["background"], "color": colors["ligh_blue_text"]},
app.layout = html.Div([
    # Header (Content)
    html.H2("จำนวนนักเรียนมัธยมศึกษาปีที่ 6 ที่จบการศึกษา ปีการศึกษา 2566"),
    dash_table.DataTable(data=filtered_df.to_dict('records'), page_size=5),

    # Dropdown for selecting province
    html.Label("จังหวัดที่ต้องการแสดง"),
    dcc.Dropdown(
        id='dropdown-selection',
        options=[{'label': province, 'value': province} for province in filtered_df['จังหวัด'].unique()],
        # filtered_df["จังหวัด"].unique(), "กรุงเทพมหานคร"),
        value='กรุงเทพมหานคร' # default
    ),

    # Checkbox for selecting genders to display
    html.Label("ตัวเลือกที่ต้องการแสดง"),
    dcc.Checklist(
        id='checklist-selection',
        options=[
            {'label': 'นักเรียนทั้งหมด', 'value': 'นักเรียนทั้งหมด'},
            {'label': 'นักเรียนชาย', 'value': 'นักเรียนชาย'},
            {'label': 'นักเรียนหญิง', 'value': 'นักเรียนหญิง'}
        ],
        value=['นักเรียนทั้งหมด'] # default
    ),

    # Graph
    dcc.Graph(id="graph-content")
])

@callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'),
     Input('checklist-selection', 'value')]
)

def update_graph(selected_province, selected_display):
    # Filter data based on selected province
    filtered_province_df = filtered_df[filtered_df["จังหวัด"] == selected_province]
    
    # Create a bar graph
    fig = px.bar(
        filtered_province_df,
        x='จังหวัด',
        y=selected_display,
        barmode='group'
        
    )
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)