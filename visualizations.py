import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('similarity_results.csv')

mutation_options = [
    'bd', 'bf', 'bi', 'br', 'bp', 'bei', 'bed', 'ber', 'sr', 'sd', 'lr2',
    'li', 'ls', 'lp', 'lis', 'lrs', 'td', 'tr2', 'ts1', 'ts2', 'tr', 'uw',
    'num', 'ft', 'fn', 'fo'
]

plt.figure(figsize=(14, 8))
ax = plt.gca()
colors = plt.cm.tab20.colors

for i, mutation_option in enumerate(mutation_options, start=1):
    data = df[df['Mutation Option'] == mutation_option]['CodeBERT Score']
    data = data.dropna()
    if not data.empty:
        color = colors[i % len(colors)] 
        ax.boxplot(data, positions=[i], widths=0.5, patch_artist=True, boxprops=dict(facecolor=color), medianprops=dict(color='black', linewidth=2))

plt.xlabel('Mutation Option', fontsize=16)
plt.ylabel('CodeBERT Score', fontsize=16)
plt.title('CodeBERT Scores by Mutation Option', fontsize=16)

plt.xticks(range(1, len(mutation_options) + 1), mutation_options, rotation=45, ha='right', fontsize=12)
plt.tight_layout()

plt.savefig('similarity_boxplot.png')
plt.show()
