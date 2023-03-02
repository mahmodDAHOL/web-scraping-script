import csv

import requests
from bs4 import BeautifulSoup

feilds = ["اسم المنشأة", "درجة العضوبة", "الحساب",
          "رقم العضويه", "العضوية", "عضو منذ", "حجم المنشأة", "عدد الساعات التدريبية", "رقم الجوال", "المدينة", "المنطقه", "البريد الإلكترونى"]
feilds.sort()


def decode_email(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16) ^ k)

    return de


def get_carts_links_from_page_link(page_link: str) -> list:

    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    my_links = []
    global titles
    titles = []
    links = soup.find_all('a')

    for link in links:
        try:
            if link.find_parent().attrs['class'][0] == "card-title":
                my_links.append(link.attrs['href'])
                titles.append(link.get_text())
        except:
            continue
    return my_links


def get_info_from_links(links: list) -> list:
    i = 0
    info = []
    for i, link in enumerate(links):
        single_info = {}
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.find_all('div')
        single_info['اسم المنشأة'] = titles[i]
        for link in links:
            try:

                if link.attrs['class'][0] == "info-details":
                    single_info[list(link.children)[1].get_text().strip()] = list(
                        link.children)[3].get_text()

                if link.attrs['class'][0] == "badge" and len(link.attrs['class']) == 1:
                    single_info["درجة العضوبة"] = list(link)[-1].strip("\n")
                if link.attrs['class'][0] == "badge" and link.attrs['class'][1] == "transparent":
                    single_info["الحساب"] = list(link)[-1].strip("\n")

                if link.attrs['class'][0] == "info-details":
                    single_info["البريد الإلكترونى"] = decode_email(
                        list(link.children)[3].find("a").attrs['href'].split("#")[1])
            except:
                continue
        if "عنوان" in single_info.keys():
            del single_info["عنوان"]
        for feild in feilds:
            if feild not in single_info.keys():
                single_info[feild] = ""
        single_info = {k: v for k, v in sorted(
            single_info.items(), key=lambda item: item[0])}
        info.append(",".join(list(single_info.values())).replace("\n", " "))

    return info


def main():
    with(open('data2.csv', 'a', encoding='utf-8-sig', newline="")) as fh:
        writer = csv.writer(fh)
        website_name = "muqawil.org"
        for page_number in range(200):
            print(f"{page_number=}")
            my_links = get_carts_links_from_page_link(
                f"https://{website_name}/ar/contractors?page={page_number}")
            info = get_info_from_links(my_links)
            for inf in info:
                writer.writerow(inf.split(","))


if __name__ == "__main__":
    main()
