import requests
from bs4 import BeautifulSoup
import csv
import os
from tqdm import tqdm
import math


def scrapePage(num):
    titles = []
    summaries = []
    prices = []
    numOfBidsEntries = []
    tags = []
    URL = f"https://www.freelancer.com/jobs/{num}?results=100"

    headers = {
        "User-Agent": 'Chrome'
    }

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    for x in soup.findAll("a", {"class": "JobSearchCard-primary-heading-link"}):
        titles.append(x.get_text().strip())

    for x in soup.findAll("p", {"class": "JobSearchCard-primary-description"}):
        summaries.append(x.get_text().strip())

    for x in soup.findAll("div", {"class": "JobSearchCard-primary-tags"}):
        group = []
        for y in x.findAll("a", {"class": "JobSearchCard-primary-tagsLink"}):
            group.append(y.get_text().strip())
        tags.append(group)

    for x in soup.findAll("div", {"class": "JobSearchCard-secondary-price"}):
        prices.append(" ".join(x.get_text().split()))

    for x in soup.findAll("div", {"class": "JobSearchCard-secondary-entry"}):
        numOfBidsEntries.append(x.get_text().strip())

    if(len(titles) == len(summaries) or len(titles) == len(prices)):
        try:
            with open('result.csv', 'a', encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                row = []
                for x in range(len(titles)):
                    row.append(titles[x])
                    row.append(summaries[x])
                    row.append(tags[x])
                    row.append(prices[x])
                    row.append(numOfBidsEntries[x])
                    writer.writerow(row)
                    row = []
        except:
            pass


if os.path.exists("result.csv"):
      os.remove("result.csv")
with open('result.csv', 'a', encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    row = ["Title", "Description", "Tag", "Price/Budget", "Bids/Entries"]
    writer.writerow(row)

URL = f"https://www.freelancer.com/jobs/?results=100"

headers = {
    "User-Agent": 'Chrome'
}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

numOfPage = soup.find("span", {"id": "total-results"}).get_text().strip().replace(',','')

print(f"Total Job Count: {numOfPage}")

numOfPage = int(1+math.ceil(int(numOfPage)/100))

print(f"Total Page Count: {numOfPage-1}")

for x in tqdm(range(1, numOfPage)):
    scrapePage(x)

print("Done")