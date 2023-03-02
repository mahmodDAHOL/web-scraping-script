import csv
from typing import List
import bs4
import requests
from bs4 import BeautifulSoup


def get_info_from_li(li: bs4.element.Tag):
    try:
        alters = [
            "priceTag hardShadow float-right floatL",
            "priceTag hardShadow float-right floatL yellowBg",
        ]
        span = get_alternate(li, alters, "span").text

        alters = ["col-7 contentBox", "contentBox col-7", "contentBox col-6_5"]
        div = get_alternate(li, alters, "div")
        link = div.find("a").attrs["href"]
        page1 = requests.get(link)
        soup1 = BeautifulSoup(page1.content, "html.parser")
        field1 = soup1.find("h1", "searchTitle").text
        field2 = div.find("h4", "listingH4 floatR").text
        field3 = div.find("h3").text
        return span, field1, field2, field3
    except Exception as e:
        print(str(e))
        return 0


def get_full_page_data(page):
    soup = BeautifulSoup(page.content, "html.parser")

    lis: List[bs4.element.Tag] = soup.find_all("li", "listingBox w100")
    spans, field1s, field2s, field3s = [], [], [], []
    for i, li in enumerate(lis):
        print(f"element :{i}")
        res = get_info_from_li(li)
        if res != 0:
            span, field1, field2, field3 = res
            spans.append(
                span.strip("\n").strip("\t").strip("\n").strip("\t").strip("\n")
            )
            field1s.append(
                field1.strip("\n").strip("\t").strip("\n").strip("\t").strip("\n")
            )
            field2s.append(
                field2.strip("\n").strip("\t").strip("\n").strip("\t").strip("\n")
            )
            field3s.append(
                field3.strip("\n")
                .strip("\t")
                .strip("\n")
                .strip("\t")
                .strip("\n")
                .replace("\n", " ")
                .replace("\t", "")
            )
    return spans, field1s, field2s, field3s


def get_alternate(li: bs4.element.Tag, alters: list, el_name: str) -> bs4.element.Tag:
    for alt in alters:
        if li.find(el_name, alt) is not None:
            return li.find(el_name, alt)
        else:
            continue


def main():
    with open(
        "/content/drive/MyDrive/data.csv",
        "a",
        encoding="utf-8-sig",
        newline="",
    ) as fh:
        writer = csv.writer(fh)
        for i in range(1, 66):
            print(f"{i=}")
            page = requests.get(
                f"https://www.mubawab.ma/fr/ct/tanger/immobilier-a-vendre:p:{i}"
            )
            spans, field1s, field2s, field3s = get_full_page_data(page)
            for span, field1, field2, field3 in zip(spans, field1s, field2s, field3s):
                print(span, field1, field2, field3)
                writer.writerow([span, field1, field2, field3])


if __name__ == "__main__":
    main()
