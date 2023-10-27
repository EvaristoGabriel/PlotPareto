import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource

# escrevendo um título na página
st.title('Fronteira de Pareto')

### Pegando os dados do arquivo
data = []
current_group = None

with open('pontos_pareto.txt', 'r') as file:
    for line in file:
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
# st.dataframe(df)

for iteration in iterations:
    st.write(f"Iteração: {iteration}")
    subset = df[df['Iteration'] == iteration]
    print(subset)
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

    # Atualiza os dados no gráfico interativo na página do Streamlit
    scatter.data_source.data = data_dict
    plt.clf()