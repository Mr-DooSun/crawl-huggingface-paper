import requests
from bs4 import BeautifulSoup

from datetime import datetime, timedelta

from tqdm import tqdm

def get_paper_uids(date:str):
    url = "https://huggingface.co/papers"
    params = {"date":date}

    response = requests.get(url=url,params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.select('body > div > main > div:nth-child(2) > section > div > div > article > a')

    paper_uids = [ element['href'].split("/")[-1] for element in elements ]

    return paper_uids

def generate_dates(start_date, num_days):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    return [(start - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]


def download_pdf(paper_uids:list) -> int:
    url = "https://arxiv.org/pdf"

    for uid in paper_uids :
        pdf_url=f"{url}/{uid}"
        save_path=f"papers/{uid}.pdf"

        response = requests.get(pdf_url)

        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"PDF downloaded successfully: {save_path}")
        else:
            raise Exception(f"Failed to download PDF: {response.status_code}")

def crawl_huggingface_papers():
    today = datetime.now().strftime("%Y-%m-%d")
    num_days = 50
    dates = generate_dates(start_date=today, num_days=num_days)

    for date in tqdm(dates) :
        paper_uids = get_paper_uids(date=date)
        download_pdf(paper_uids=paper_uids)

if __name__ == "__main__":
    results = crawl_huggingface_papers()