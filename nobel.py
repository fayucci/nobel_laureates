import pandas as pd
import numpy as np
from bokeh.io import output_file, show, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select, RadioButtonGroup, Legend, Paragraph, Div
from bokeh.models.ranges import FactorRange, DataRange1d
from bokeh.plotting import figure
from bokeh.sampledata.commits import data
from bokeh.transform import factor_cmap
from bokeh.colors import HSL
from bokeh.layouts import row, column
from bokeh.themes import built_in_themes
import math 
from hexagonal_clusters import hex_y, hex_x, delta_x, delta_y, scale_factor
from nobel_data import nobel
from bokeh.models.tools import  BoxZoomTool, PanTool, WheelZoomTool, ResetTool, HoverTool

output_file('nobel.html')

cmap = {
    "Chemistry"  : HSL(0, 0.5, 0.5).to_rgb().to_hex(),
    "Medicine"   : HSL(120, 0.5, 0.5).to_rgb().to_hex(),
    "Physics"    : HSL(180, 0.5, 0.5).to_rgb().to_hex(),
    "Peace"      : HSL(240, 0.5, 0.5).to_rgb().to_hex(),
    "Economics"  : HSL(300, 0.5, 0.5).to_rgb().to_hex(),
    "Literature" : HSL(60, 0.5, 0.5).to_rgb().to_hex()
}

source = ColumnDataSource(data={
    "x" : [],
    "y" : [],
    "Category" : nobel['Category']
})

aspect_ratio= 2.4
p = figure(
    title="Nobel Laureates",
    x_axis_label='Categories',
    y_axis_label='Countries',
    aspect_ratio=aspect_ratio,
    match_aspect=True,
    tooltips=[("Country", "@birth_country"), ("Name", "@Name"), ('Year', '@Year'), ('Motive', '@Motive'), ('Category', '@Category')],
    tools=[],
    margin=0,
    toolbar_location=None
)


legend = Legend(
    orientation="horizontal",
    margin=0,
    location="top_center",
    border_line_width=0,
)
p.add_layout(legend, 'above')
circles = p.circle(
    x='x',
    y='y',
    source=source,
    alpha=1,
    line_width = 0, 
    color=factor_cmap('Category', palette=list(cmap.values()), factors=list(cmap.keys())),
    legend_field='Category'
)
p.x_range.range_padding = 0.1
p.y_range.range_padding = 0.1

p.title.text_font_size = "50px"
p.title.align = "center"

p.xaxis.axis_label_text_font_size = "25px"
p.yaxis.axis_label_text_font_size = "25px"


def create_mask(active, df):
    if active == 1:
        return df['sex'] == 'Female'
    elif active == 2:
        return df['death_date'] == 'Alive'
    elif active == 3:
        return df['prize_share'].astype('int') >= 2
    else:
        return [True for i in df.iterrows()]

def pre_filter(x_name, y_name):
    if x_name == 'Affiliations':
        return nobel[nobel['Affiliations'] != 'others'].copy()
    return nobel.copy()
    
def config_plot(active, x_name, y_name):
    df = pre_filter(x_name, y_name)
    mask = create_mask(active, df)
    X = df[x_name].unique().tolist()
    Y = df[y_name].unique().tolist()
    x_scale = 1.5*len(Y)*aspect_ratio / len(X)
    clusters = df.groupby([x_name, y_name])
    largest_cluster = clusters.count()['laureate_id'].max()
    scale = scale_factor(largest_cluster)
    circles.glyph.radius =  scale*delta_x

    for cols, rows in clusters.groups.items():
        x_col, y_col = cols
        x_offset = X.index(x_col) * x_scale
        y_offset = Y.index(y_col)
        df.loc[rows, "y"] = [y_offset + scale*delta_y * hex_y(k) for k in range(len(rows))]
        df.loc[rows, "x"] = [x_offset + scale*delta_x * hex_x(k) for k in range(len(rows))]

    source.data = { 
        'x': df.loc[(mask), 'x'],
        'y' : df.loc[(mask), 'y'],
        'Category' : df.loc[(mask), 'Category'],
        'Affiliations' : df.loc[(mask), "Affiliations"],
        'Decade' : df.loc[(mask), 'Decade'],
        'sex' : df.loc[(mask), 'sex'],
        'Name' : df.loc[(mask), 'full_name'],
        'Year' : df.loc[(mask), 'Year'],
        'Country' : df.loc[(mask), 'Country'],
        'Motive' : df.loc[(mask), 'motivation'],
        'death_date' : df.loc[(mask), 'death_date'],
        'Prize_share' : df.loc[(mask), 'prize_share'],
        'birth_country' : df.loc[(mask), 'birth_country']
    }

    p.xaxis.ticker = [i * x_scale for i in range(len(X))]
    p.yaxis.ticker = [i for i in range(len(Y))]
    p.xaxis.major_label_overrides = { int(v) if v % 1 == 0 else v: X[i] for i, v in enumerate(p.xaxis.ticker.ticks) }
    p.yaxis.major_label_overrides = { v: Y[i] for i, v in enumerate(p.yaxis.ticker.ticks) }


def update_plot(attr, old, new):
    x = x_select.labels[x_select.active]
    y = y_select.labels[y_select.active]
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    config_plot(filter_group.active, x, y)



config_plot(0, 'Country', 'Category')

filter_group = RadioButtonGroup(labels=["All", "Female", "Alive", "Shared"], active=0)

filter_group.on_change('active', update_plot)

x_select = RadioButtonGroup(labels=['Country', 'Affiliations'], active=0)
x_select.on_change('active', update_plot)

y_select = RadioButtonGroup(labels=['Category', 'Decade'], active=0)
y_select.on_change('active', update_plot)

x_label = Paragraph(text="X:", align="center")
y_label = Paragraph(text="Y:", align="center")
filter_label = Paragraph(text="Filter:", align="center")
caption = Div(text=""" <em> By <strong> Fatima Yucci </strong>. Find me in : <a href="https://github.com/fayucci/nobel_laureates"> Github </a> or <a href="https://www.linkedin.com/in/fatima-yucci/?locale=en_US"> LinkedIn </a> </em>
""")
data_source = Div(text= """Data Source : <a href="https://learn.datacamp.com/projects/441"> DataCamp </a>""")

layout = column(p, row(filter_label, filter_group, x_label, x_select, y_label, y_select, align="center"), caption, data_source, align="center", sizing_mode="scale_both")

curdoc().add_root(layout)
