import time
import requests
import csv
from bs4 import BeautifulSoup
import datetime

# 请求头部
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}


# 获取所有药材的链接和信息
def get_med_info(page_num):
    url = f"https://db.yaozh.com/zhongyaocai?p={page_num}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to retrieve {url}: {resp.status_code}")
        return []

    page = BeautifulSoup(resp.text, "html.parser")
    med_list = []

    # 根据实际网页结构提取药材信息
    rows = page.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 6:

            med_name = row.find("th").find("a").text.strip()
            med_category = columns[0].text.strip()
            med_origin = columns[1].text.strip()
            med_alias = columns[2].text.strip()
            med_properties = columns[3].text.strip()
            med_functions = columns[4].text.strip()
            med_list.append([med_name, med_category, med_origin, med_alias, med_properties, med_functions])

    resp.close()
    time.sleep(0.5)
    return med_list


if __name__ == '__main__':
    print(f"==== {datetime.datetime.now()} start executing crawler === \n")
    all_meds = []

    max_pages = 1000

    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        med_info = get_med_info(page)
        if not med_info:
            print("No more data to fetch.")
            break
        all_meds.extend(med_info)

    # 写入 CSV 文件
    with open("yaozhishuzu.csv", mode="w", newline='', encoding='utf-8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["药材名称", "药材类别", "药材基原", "药材别名", "性味归经", "功能主治"])
        csvwriter.writerows(all_meds)

    print(f"Fetched {len(all_meds)} records.")
    print(f"==== {datetime.datetime.now()} end === \n")
