from bs4 import BeautifulSoup
import requests
from time import sleep
base_url = "http://shop.oreilly.com/category/browse-subjects/" + \
 "data.do?sortby=publicationDate&page="

books = []
# NUM_PAGES = 31 # 这是写作本书时的值，现在有可能更多
NUM_PAGES = 3

for page_num in range(1, NUM_PAGES + 1):
    print("souping page", page_num, ",", len(books), " found so far")
    url = base_url + str(page_num)
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')
    for td in soup('td', 'thumbtext'):
        if not is_video(td):
            books.append(book_info(td))
# 现在做一个好公民，遵守robots.txt！
# sleep(30)
sleep(3)

# 把每一年出版的图书数据绘制出来（如图 9-1）：
def get_year(book):
    """book["date"] looks like 'November 2014' so we need to
    split on the space and then take the second piece"""
    return int(book["date"].split()[1])
# 2014是包含数据的最后一个完整的年份（我运行这段代码的时间）
from collections import Counter # 默认未加载
year_counts = Counter(get_year(book) for book in books
                        if get_year(book) <= 2014)
import matplotlib.pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

years = sorted(year_counts)
book_counts = [year_counts[year] for year in years]
plt.plot(years, book_counts)
plt.ylabel("数据图书的数量")
plt.title("数据大发展！")
plt.show()
