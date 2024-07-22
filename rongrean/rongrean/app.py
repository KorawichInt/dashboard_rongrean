from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import os
import plotly.graph_objects as go
import json


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
filtered_df.columns = ["จังหวัด", "นักเรียนชาย", "นักเรียนหญิง", "นักเรียนทั้งหมด"]

with open('thailand_provinces.geojson', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

app.layout = html.Div([
    html.H2(
        "จำนวนนักเรียนมัธยมศึกษาปีที่ 6 ที่จบการศึกษา ปีการศึกษา 2566", 
        style={'textAlign': 'center'}
    ),
    dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        page_size=5,
        style_cell={'textAlign': 'center'}
    ),

    html.Div(
        [
            html.Label(
                "จังหวัดที่ต้องการแสดง",
                style={'font-weight':'bold'}
            ),
        ],
        style={'margin-bottom': '10px'}
    ),

    html.Div(
        [
            dcc.Dropdown(
                id='dropdown-selection',
                options=[{'label': province, 'value': province} for province in filtered_df['จังหวัด'].unique()],
                value='กรุงเทพมหานคร'  # default
            ),
        ],
        style={'margin-bottom': '30px'}
    ),

    html.Div(
        [
            html.Label(
                "ตัวเลือกที่ต้องการแสดง",
                style={'font-weight':'bold'}
            ),
        ],
        style={'margin-bottom': '10px'}
    ),

    html.Div(
        [
            dcc.Checklist(
                id='checklist-selection',
                options=[
                    {'label': 'นักเรียนทั้งหมด', 'value': 'นักเรียนทั้งหมด'},
                    {'label': 'นักเรียนชาย', 'value': 'นักเรียนชาย'},
                    {'label': 'นักเรียนหญิง', 'value': 'นักเรียนหญิง'}
                ],
                value=['นักเรียนทั้งหมด'],  # default
                # inline=True
            ),
        ],
        style={'margin-bottom': '20px'}
    ),

    dcc.Graph(id="graph-content", style={'width': '100%'}),
    dcc.Graph(id="map-content", style={'width': '100%'})
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
        labels={'Category': 'ประเภทนักเรียน', 'Count': 'จำนวนนักเรียน (คน)'},
    )
    
    fig.update_layout(
        title={
            'text': f"จำนวนนักเรียนที่เรียนจบในจังหวัด {selected_province}",
            'font': {'size':20, 'weight':'normal'},
            'pad':{'t':-20},
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        # width=800,
        # bargap=0.8
    )

    fig.update_traces(
        width=0.2
    )
    
    return fig

@callback(
    Output('map-content', 'figure'),
    [Input('dropdown-selection', 'value')]
)

def update_map(selected_province):
    fig = px.choropleth(
        filtered_df,
        geojson=geojson,
        locations='จังหวัด',
        featureidkey="properties.name",
        color='นักเรียนทั้งหมด',
        color_continuous_scale="YlOrRd",
        range_color=[filtered_df['นักเรียนทั้งหมด'].min(), filtered_df['นักเรียนทั้งหมด'].max()],
        labels={'นักเรียนทั้งหมด': 'นักเรียนทั้งหมด'},
        # width=2000,
    )
    
    fig.update_geos(fitbounds="locations", visible=True)
    
    fig.update_layout(
        title={
            'text': "จำนวนนักเรียนทั้งหมดที่เรียนจบในแต่ละจังหวัด",
            'font': {'size':20, 'weight':'normal'},
            'pad':{'t':-20},
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        coloraxis_colorbar={
            'title': 'จำนวนนักเรียนทั้งหมด (คน)',
            'x': 1.05,
            'len': 0.8
        }
    )
    
    return fig


if __name__ == "__main__":
    app.run(debug=True)
