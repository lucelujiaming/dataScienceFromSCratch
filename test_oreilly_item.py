# coding: utf-8

from bs4 import BeautifulSoup
import requests
# 除非是写进书里，否则你没必要这样拆分一个url
# url = "http://shop.oreilly.com/category/browse-subjects/" + \
#	 "data.do?sortby=publicationDate&page=1"
url = "https://www.oreilly.com/search/?query=data&extended_publisher_data=true"

soup = BeautifulSoup(requests.get(url).text, 'html5lib')

tds = soup('td', 'thumbtext')
print(len(tds))

def is_video(td):
	"""it's a video if it has exactly one pricelabel, and if
	the stripped text inside that pricelabel starts with 'Video'"""
	pricelabels = td('span', 'pricelabel')
	return (len(pricelabels) == 1 and
			pricelabels[0].text.strip().startswith("Video"))
print(len([td for td in tds if not is_video(td)]))
# 对我来说结果是21，你得到的结果可能会不同

#	# 从td元素中提取数据
#	title = td.find("div", "thumbheader").a.text
#
#	# 作者（们）的名字在 AuthorName <div> 的文本里
#	author_name = td.find('div', 'AuthorName').text
#	authors = [x.strip() for x in re.sub("^By ", "", author_name).split(",")]
#
#	# ISBN 看起来是包含在 thumbheader <div> 中的链接里：
#	isbn_link = td.find("div", "thumbheader").a.get("href")
#	# re.match捕捉了括号中的正则表达式部分
#	isbn = re.match("/product/(.*)\.do", isbn_link).group(1)
#
#	# 日期就是 <span class="directorydate"> 的内容：
#	date = td.find("span", "directorydate").text.strip()

# 我们把所有这些都放到一个函数里边：
def book_info(td):
	"""given a BeautifulSoup <td> Tag representing a book,
	extract the book's details and return a dict"""

	# 从td元素中提取数据
	title = td.find("div", "thumbheader").a.text
	# 作者（们）的名字在 AuthorName <div> 的文本里
	by_author = td.find('div', 'AuthorName').text
	authors = [x.strip() for x in re.sub("^By ", "", by_author).split(",")]
	# ISBN 看起来是包含在 thumbheader <div> 中的链接里：
	isbn_link = td.find("div", "thumbheader").a.get("href")
	# re.match捕捉了括号中的正则表达式部分
	isbn = re.match("/product/(.*)\.do", isbn_link).groups()[0]
	# 日期就是 <span class="directorydate"> 的内容：
	date = td.find("span", "directorydate").text.strip()
	return {
		"title" : title,
		"authors" : authors,
		"isbn" : isbn,
		"date" : date
	}
