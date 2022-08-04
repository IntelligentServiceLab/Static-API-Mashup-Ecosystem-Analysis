import numpy as np
import matplotlib.pyplot as plt


label = ['API name', 'Tags', 'Category', 'URL ', 'Protocol']

text = [['Shiny Ads', 'advertising','Advertising', 'http://ShinyAds.com', 'REST'],
        ['Websnapr', 'imag,security ', 'Security ', 'http://www.Websnapr.com/code/', 'JavaScript']]

table = plt.table(cellText=text, colLabels=label, loc='center', cellLoc='center',rowLoc='center')
table.scale(1,2)
plt.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Table I.  EXAMPLES OF WEB APIS ")
plt.show()
