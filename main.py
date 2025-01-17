import requests
from bs4 import BeautifulSoup

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

def download_pdf(paper_uids:list):
    
    url = "https://arxiv.org/pdf"
    paper_uids = get_paper_uids(date="2025-01-16")

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
    paper_uids = get_paper_uids(date="2025-01-16")
    download_pdf(paper_uids=paper_uids)

if __name__ == "__main__":
    results = crawl_huggingface_papers()