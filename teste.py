import pandas as pd

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
            content = eval(parts[1].strip())  # Avalia a string JSON
            parameters = parts[2]
            current_group["items"].append({"value": value, "content": content, "parameters": parameters})
print(data[1])

df = pd.DataFrame({
    'Group': [idx for idx, group in enumerate(data) for _ in group['items']],
    'Value': [item['value'] for group in data for item in group['items']],
    'Content': [item['content'] for group in data for item in group['items']],
    'Parameters': [item['parameters'] for group in data for item in group['items']]
})
df['Group'] = df['Group'] + 1
print(df)