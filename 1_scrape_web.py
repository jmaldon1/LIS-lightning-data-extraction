import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def is_nc_file(url):
    ext = [".nc"]
    return any([url.lower().endswith(e.lower()) for e in ext])


def getLinks(session, url):
    print("Getting links from: " + url)
    page = session.get(url)
    html = page.content.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tr = soup.find_all("tr")
    tr = tr[2:]
    links = [row.find_all("a") for row in tr]
    res = [link[0].get("href") for link in links]
    return res


def main():
    data_dir = "./data"
    creds = {
        "username": os.environ["EARTH_DATA_USERNAME"],
        "password":  os.environ["EARTH_DATA_PASSWORD"],
    }
    base_url = "https://ghrc.nsstc.nasa.gov/pub/lis/iss/data/science/final/nc/"
    login_url = "https://urs.earthdata.nasa.gov/login"

    with requests.Session() as session:
        post_data = session.get(login_url)
        html = BeautifulSoup(post_data.text, "html.parser")
        csrf_token = (
            html.find(id="login")
            .find("input", {"name": "authenticity_token"})
            .get("value")
        )
        creds["authenticity_token"] = csrf_token
        session.post(login_url, data=creds)

        def dfs(url):
            for link in getLinks(session, url):
                next_url = urljoin(url, link)
                if is_nc_file(link):
                    print("Downloading: " + next_url)
                    with open(os.path.join(data_dir, link), "wb") as f:
                        f.write(session.get(next_url).content)
                    break  # Only download 1 file per day
                else:
                    dfs(next_url)

        dfs(base_url)


if "__main__" == __name__:
    load_dotenv()
    main()
