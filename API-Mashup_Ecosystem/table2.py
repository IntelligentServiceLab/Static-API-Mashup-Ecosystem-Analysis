import numpy as np
import matplotlib.pyplot as plt


label = ['Mashup name', 'Categories', 'Component APIs', 'URL']

text = [['Standuply', 'Project management','Slack bot, Slack conversations', 'https://standuply.com'],
        ['Nostalgia', 'Music, charts', 'Spotify Web, YouTube ', 'http://www.nostalgilistan.se ']]
plt.figure(figsize=(20,8))
table = plt.table(cellText=text, colLabels=label, loc='center', cellLoc='center',rowLoc='center')
table.scale(1,2)
plt.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Table 2 Mashup examples")
plt.show()

