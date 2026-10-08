import requests

URL = "https://www.cnn.com"


def fetch_headlines():
    resp = requests.get(URL)
    # Placeholder: only fetches homepage HTML
    return resp.text[:500]


if __name__ == "__main__":
    print(fetch_headlines())
