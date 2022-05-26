# coding: utf-8

from bs4 import BeautifulSoup
import requests
# html = requests.get("http://www.example.com").text
html = requests.get("http://www.dicts.cn").text
soup = BeautifulSoup(html, 'html5lib')

# 找到你能用的第一个 <p> 标签（及其内容）：
first_paragraph = soup.find('p') # 或仅仅soup.p

# 可以对 Tag 使用它的 text 属性来得到文本内容：
first_paragraph_text = soup.p.text
first_paragraph_words = soup.p.text.split()
print("first_paragraph_words : ", first_paragraph_words);

# 另外可以把标签当作字典来提取其属性：
# first_paragraph_id = soup.p['id'] # 如果没有'id'则报出KeyError 
# first_paragraph_id2 = soup.p.get('id') # 如果没有'id'则返回None

# 可以一次得到多个标签：
all_paragraphs = soup.find_all('p') # 或仅仅soup('p')
paragraphs_with_ids = [p for p in soup('p') if p.get('id')]

# 通常你会想通过一个类（class）来找到标签：
important_paragraphs = soup('p', {'class' : 'important'})
important_paragraphs2 = soup('p', 'important')
important_paragraphs3 = [p for p in soup('p')
						if 'important' in p.get('class', [])]
# 此外，可以把这些方法组合起来运用更复杂的逻辑。比如，如果想找出包含在一个<div>
# 元素中的每一个 <span> 元素，可以这么做：
# 警告，将多次返回同一个span元素
# 如果它位于多个div元素里
# 如果是这种情况，要更谨慎一些
spans_inside_divs = [span
		for div in soup('div') # 对页面上的每个<div> 
		for span in div('span')] # 找到其中的每一个<span>


