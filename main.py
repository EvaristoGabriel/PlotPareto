import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource

st.title('Fronteira de Pareto')

uploaded_file = st.file_uploader("Faça o upload de um arquivo", type=["txt"])

data = []
current_group = None

if uploaded_file is not None:
    uploaded_file = uploaded_file.read().decode("utf-8")
    lines = uploaded_file.split("\n")
    for line in lines:
        line = line.strip()
        parts = line.split("|")
        if len(parts) == 1:
            current_group = {"items": []}
            data.append(current_group)
        elif len(parts) == 3:
            value = float(parts[0].strip())
            content = float(parts[1].strip())  # Avalia a string JSON
            parameters = parts[2]
            current_group["items"].append({"value": value, "content": content, "parameters": parameters})

df = pd.DataFrame({
    'Iteration': [idx for idx, group in enumerate(data) for _ in group['items']],
    'Value': [item['value'] for group in data for item in group['items']],
    'Content': [item['content'] for group in data for item in group['items']],
    'Parameters': [item['parameters'] for group in data for item in group['items']]
})
df['Iteration'] = df['Iteration'] + 1
################################################################
iterations = df['Iteration'].unique()

for iteration in iterations:
    st.write(f"Iteração: {iteration}")
    subset = df[df['Iteration'] == iteration]
    plot = figure(tooltips=[('Value', '@Value{0.0}'), ('Content',
                  '@Content{0.0000000000000000}'), ('Parameters', '@Parameters')])
    scatter = plot.circle('Value', 'Content',
                        source=ColumnDataSource(subset), size=10, color='blue')
    hover = HoverTool(names=[],tooltips=None)
    plot.add_tools(hover)
    plot.line('Value', 'Content', source=ColumnDataSource(subset), line_width=2)
    st.bokeh_chart(plot)
    data_dict = {
        'Value': subset['Value'],
        'Content': subset['Content'],
        'Parameters': subset['Parameters']
    }

    scatter.data_source.data = data_dict
    plt.clf()