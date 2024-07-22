from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import os

app = Dash(__name__)

def read_and_save_json(url, save_path):
    if os.path.exists(save_path):
        print(f"File already exists at {save_path}")
        df = pd.read_json(save_path)
        return df
    
    df = pd.read_json(url)
    df.to_json(save_path)
    print(f"Read and saved to {save_path}")
    return df

url = "https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json"
data_path = "student_data"
student_df = read_and_save_json(url, data_path)

filtered_df = student_df.loc[:, ["schools_province", "totalmale", "totalfemale", "totalstd"]]
filtered_df.columns = ["จังหวัด", "จำนวนนักเรียนชาย", "จำนวนนักเรียนหญิง", "จำนวนนักเรียนทั้งหมด"]

app.layout = html.Div([
    html.H2("จำนวนนักเรียนมัธยมศึกษาปีที่ 6 ที่จบการศึกษา ปีการศึกษา 2566"),
    dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        page_size=5,
        style_cell={'textAlign': 'center'}
    ),

    html.Div(
        [
            html.Label("จังหวัดที่ต้องการแสดง"),
            dcc.Dropdown(
                id='dropdown-selection',
                options=[{'label': province, 'value': province} for province in filtered_df['จังหวัด'].unique()],
                value='กรุงเทพมหานคร'  # default
            ),
        ],
        style={'margin-bottom': '30px'}
    ),

    html.Label("ตัวเลือกที่ต้องการแสดง"),
    dcc.Checklist(
        id='checklist-selection',
        options=[
            {'label': 'นักเรียนทั้งหมด', 'value': 'จำนวนนักเรียนทั้งหมด'},
            {'label': 'นักเรียนชาย', 'value': 'จำนวนนักเรียนชาย'},
            {'label': 'นักเรียนหญิง', 'value': 'จำนวนนักเรียนหญิง'}
        ],
        value=['จำนวนนักเรียนทั้งหมด']  # default
    ),

    dcc.Graph(id="graph-content", style={'width': '100%'})
])

@callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'),
     Input('checklist-selection', 'value')]
)
def update_graph(selected_province, selected_display):
    filtered_province_df = filtered_df[filtered_df["จังหวัด"] == selected_province]

    melted_df = filtered_province_df.melt(id_vars=["จังหวัด"], value_vars=selected_display,
                                          var_name='Category', value_name='Count')

    fig = px.bar(
        melted_df,
        x='Category',
        y='Count',
        labels={'Category': 'ประเภทนักเรียน', 'Count': 'จำนวนนักเรียน'},
    )
    
    fig.update_layout(
        title={
            'text': f"จำนวนนักเรียนที่เรียนจบในจังหวัด {selected_province}",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        width=800
    )
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)
