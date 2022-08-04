import numpy as np
import matplotlib.pyplot as plt


label = ['Mashup name', 'Tags', 'APIs used by the Mashup']

text = [['EmbedPlus', 'motion, scene, skip, slow, video, youtube', 'Bit.ly, Topsy, YouTube'],
        ['Earth Sandwich ', 'mapping, science', 'Google Maps'],
        ['AuctionPixie ', 'auction, shopping', 'eBay, hostip.info']]

table = plt.table(cellText=text, colLabels=label, loc='center', cellLoc='center',rowLoc='center')
table.scale(1,2)
plt.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Table II. EXAMPLES OF MASHUPS")
plt.show()
