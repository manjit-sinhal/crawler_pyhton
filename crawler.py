import urllib.parse
from collections import deque
import requests
from bs4 import BeautifulSoup
import sys

# manjit
class WebCrawler:

    def __init__(self, start_url, max_depth=2):
        self.start_url = start_url
        self.max_depth = max_depth
        # Parse target domain to keep the crawler from leaving the site
        self.target_domain = urllib.parse.urlparse(start_url).netloc
        # Use a set for O(1) duplicate lookups
        self.visited = set()
        # Queue stores tuples of (url, current_depth)
        self.queue = deque([(start_url, 0)])

    def get_internal_links(self, html_content, base_url):
        """Extracts and normalizes all internal URLs from a page."""
        soup = BeautifulSoup(html_content, "html.parser")
        links = set()

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            # Convert relative URLs (e.g., /about) to absolute URLs
            absolute_url = urllib.parse.urljoin(base_url, href)
            parsed_url = urllib.parse.urlparse(absolute_url)

            # Ensure the link belongs to the same domain and uses HTTP(S)
            if (
                parsed_url.netloc == self.target_domain
                and parsed_url.scheme in ["http", "https"]
            ):
                # Strip fragments (#section1) to avoid crawling the same page twice
                clean_url = absolute_url.split("#")[0]
                links.add(clean_url)

        return links

    def crawl(self):
        """Executes the crawl loop."""
        print(f"🚀 Starting crawl on: {self.start_url}")

        while self.queue:
            url, depth = self.queue.popleft()

            # Skip if already visited or if it exceeds max depth
            if url in self.visited or depth > self.max_depth:
                continue

            print(f"🌐 [Depth {depth}] Crawling: {url}")
            self.visited.add(url)

            try:
                # Custom User-Agent to avoid generic bot blocks
                headers = {"User-Agent": "MyPythonCrawler/1.0"}
                response = requests.get(url, headers=headers, timeout=5)

                if response.status_code == 200:
                    # Optional: Extract and save page data here (Scraping)
                    # For now, we extract new links to follow
                    new_links = self.get_internal_links(response.text, url)

                    for link in new_links:
                        if link not in self.visited:
                            self.queue.append((link, depth + 1))
                else:
                    print(
                        f"⚠️ Skipped {url} (Status Code: {response.status_code})"
                    )

            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to fetch {url}: {e}")

        print(f"\n✅ Crawl finished. Total unique pages visited: {len(self.visited)}")


if __name__ == "__main__":
    # Test your crawler on a safe sandbox or your own site
    START_URL = "https://www.mysite.com"
    crawler = WebCrawler(start_url=START_URL, max_depth=2)
    crawler.crawl()


#try to copy it in output.txt
def custom_print(message_to_print, log_file='output.txt'):
    print(message_to_print)
    with open(log_file, 'a') as of:
        of.write(message_to_print + '\n')


#use TEE 
#python3 craw.py | tee console.txt 
