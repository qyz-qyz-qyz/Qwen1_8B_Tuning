import time
import requests
import csv
from bs4 import BeautifulSoup
import re


class Medicine:
    def __init__(self):
        self.url = 'http://www.zhongyoo.com/name/page_{}.html'

    def parse_url(self, url):
        resp = requests.get(url)
        resp.encoding = 'gb2312'
        return resp.text

    def get_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return [a['href'] for a in soup.select('div.r2-con div.sp strong a')]

    def parse_link(self, link, csv_writer):
        html = self.parse_url(link)
        soup = BeautifulSoup(html, 'html.parser')
        gaishu_div = soup.find('div', class_='gaishu')

        if gaishu_div:
            # 获取 div 中的所有文本内容
            text_content = gaishu_div.get_text(separator='\n', strip=True)
            formatted_content = ''.join([line.strip() for line in text_content.splitlines() if line.strip()])
            medicine_names = re.findall(r'【中药名】([\u4e00-\u9fa5]+)', formatted_content)
            medicine_parts = re.findall(r'(?<=【药用部位】).*?(?=【)', formatted_content)
            medicine_symbol = re.findall(r'(?<=【药材性状】).*?(?=【)', formatted_content)
            medicine_taste = re.findall(r'(?<=【性味归经】).*?(?=【)', formatted_content)
            medicine_importance = re.findall(r'(?<=【功效与作用】).*?(?=【)', formatted_content)
            medicine_apply = re.findall(r'(?<=【临床应用】).*?(?=【)', formatted_content)
            medicine_rearch = re.findall(r'(?<=【药理研究】).*?(?=【)', formatted_content)
            medicine_indregient = re.findall(r'(?<=【主要成分|化学成分】).*?(?=【)', formatted_content)
            medicine_taboo = re.findall(r'(?<=【使用禁忌】).*?(?=【)', formatted_content)
            medicine_precription = re.findall(r'(?<=药方】).*?(?=【|$)', formatted_content)

            csv_writer.writerow([medicine_names, medicine_parts, medicine_symbol, medicine_taste, medicine_importance,
                                 medicine_apply, medicine_rearch, medicine_indregient, medicine_taboo, medicine_precription])




    def run(self):
        f = open('medicine_data_detiles.csv', 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(f)
        csv_writer.writerow(['中药名', '药用部位', '药材性状', '性味归经', '功效与作用', '临床应用', '药理研究', '主要成分|化学成分', '使用禁忌', '药方'])  # 写入表头
        for num in range(1, 45):
            start_url = self.url.format(num)
            html = self.parse_url(start_url)
            if html:
                links = self.get_links(html)
                for link in links:
                    self.parse_link(link, csv_writer)
                time.sleep(1)

        f.close()


if __name__ == "__main__":
    medicine = Medicine()
    medicine.run()
