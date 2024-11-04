import time
import requests
import csv
from bs4 import BeautifulSoup


class Medicine:
    def __init__(self):
        self.url = 'http://www.cnkang.com/yaopin/'

    def parse_url(self, url):
        resp = requests.get(url)
        resp.encoding = 'gb2312'
        return resp.text

    def get_classify(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        classify = []
        divs = soup.select('div.list-lum-tt1')
        for div in divs:
            a_tag = div.select_one('span a')
            if a_tag:
                classify.append(a_tag['href'])
        return classify

    def get_page(self, classify, writer):
        html = self.parse_url(classify)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            pages = [div.select_one('span a')['href'] for div in soup.select('div.list-lum-tt1') if div.select_one('span a')]
            if pages:
                return pages
            else:
                links = [a['href'] for a in soup.find_all('a', class_='link')]
                for link in links:
                    self.parse_link(link, writer)
        else:
            print(f"无法获取页面: {classify}")

    def get_links(self, page):
        html = self.parse_url(page)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            return [a['href'] for a in soup.select('div.f14 a.link')]
        else:
            print(f"无法获取链接页面: {page}")
            return []

    def parse_link(self, link, writer):
        html = self.parse_url(link)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            context = soup.find('div', id='wleft')
            if context:
                text_content = context.get_text(separator='\n', strip=True)
                writer.writerow([link, text_content])

    def run(self):
        html = self.parse_url(self.url)
        if html:
            with open('xiyao_medicine_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['链接', '文本内容'])
                classes = self.get_classify(html)
                for classify in classes:
                    pages = self.get_page(classify, writer)
                    if pages:
                        for page in pages:
                            links = self.get_links(page)
                            for link in links:
                                self.parse_link(link, writer)
                            time.sleep(2)
        else:
            print("无法获取分类页面。")

if __name__ == "__main__":
    medicine = Medicine()
    medicine.run()
