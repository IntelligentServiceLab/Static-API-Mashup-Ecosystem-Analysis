import numpy as np
import matplotlib.pyplot as plt


label = ['API name ', 'Primary category', 'Secondary category', 'URL', 'API provider ']

text = [['Facebook', 'Social', 'Webhooks', 'https://developers.facebook.com/', 'Facebook'],
        ['YouTube', 'Video', 'Webhooks', 'https://developers.google.com/youtube/', 'Google']]

table = plt.table(cellText=text, colLabels=label, loc='center', cellLoc='center',rowLoc='center')
table.scale(1,2)
plt.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Table 1 Web API examples")
plt.show()

