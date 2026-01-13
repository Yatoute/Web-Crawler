import time
from urllib.parse import urljoin, urldefrag

from robots import is_authorized_to_parse
from http_client import get_html_page
from html_parser import parse_html


class Crawler:
    def __init__(
        self,
        seed_urls,
        user_agent="FlexScraper/1.0",
        max_pages=50,
        priority_token="product",
        sleep_seconds=0.0,
        timeout=10,
    ):
        self.seed_urls = seed_urls
        self.user_agent = user_agent
        self.max_pages = max_pages
        self.priority_token = priority_token
        self.sleep_seconds = sleep_seconds
        self.timeout = timeout

        self.visited = set()
        self.queued = set()
        self.priority_queue = []
        self.normal_queue = []
        self.pages_crawled = 0
        self.results = []

        for url in seed_urls:
            self.add_url(url)

    def run(self):
        """Lancer le Crawler"""
        
        while self.pages_crawled < self.max_pages:
            parsed = self.crawl_next()
            if parsed is None:  # plus rien à crawler
                break
        return self.results

    def crawl_next(self):
        """Crawler la prochaine page"""
        
        url = self._pop_next_url()
        if url is None:
            return None

        self.queued.discard(url)

        if url in self.visited:
            return {} 

        # robots
        if not is_authorized_to_parse(url, self.user_agent):
            self.visited.add(url)
            return {}

        # On fait une pause
        self._throttle()

        # fetch
        html = get_html_page(url, user_agent=self.user_agent)  # timeout si tu l'ajoutes dans get_html_page
        if not html:
            self.visited.add(url)
            return {}

        # parse
        data = parse_html(html)
        data["url"] = data.get("url") or url
        self.results.append(data)

        self.visited.add(url)
        self.pages_crawled += 1

        # add links
        for link in data.get("links", []):
            absolute = urljoin(url, link)
            absolute, _ = urldefrag(absolute)  # retire les #ancres
            self.add_url(absolute)

        return data

    def add_url(self, url: str):
        """Ajouter l'url à une des 2 fils d'attente selon sa priorité"""

        url, _ = urldefrag(url)

        # On évite les doublons
        if url in self.visited or url in self.queued:
            return

        self.queued.add(url)

        if self.priority_token in url:
            self.priority_queue.append(url)
        else:
            self.normal_queue.append(url)

    def _pop_next_url(self):
        if self.priority_queue:
            return self.priority_queue.pop(0)
        if self.normal_queue:
            return self.normal_queue.pop(0)
        return None

    def _throttle(self):
        if self.sleep_seconds and self.sleep_seconds > 0:
            time.sleep(self.sleep_seconds)
