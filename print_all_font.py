from os import path
from matplotlib.font_manager import fontManager
for i in fontManager.ttflist:
    print(i.fname, i.name)
