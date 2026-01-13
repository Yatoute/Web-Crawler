import urllib.request
import urllib.error

def get_html_page(page_url: str, user_agent: str = "FlexScraper/1.0"):
    """Get html page"""

    headers = {
        "User-Agent": user_agent
    }

    request = urllib.request.Request(page_url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8")

    except urllib.error.URLError as e:
        print(f"Erreur lors de l'accès à {page_url} : {e}")
        return None