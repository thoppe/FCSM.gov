import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dspipe import Pipe

local_domain = "fcsm.gov"


def get_html_files(directory):
    """Recursively find all HTML files in the given directory."""
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html") or file.endswith(".htm"):
                html_files.append(os.path.join(root, file))
    return html_files


def extract_external_links(html_file):
    """Extract external links from an HTML file."""
    external_links = set()
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        for link in soup.find_all("a", href=True):
            url = link["href"]
            parsed_url = urlparse(url)

            if parsed_url.scheme in ("http", "https"):
                if local_domain not in parsed_url.netloc:
                    external_links.add(url)

    return external_links


def is_target_document(url: str) -> str:
    """Guess the file type based on the URL extension."""
    file_types = {
        ".pdf": "PDF Document",
        ".docx": "Word Document (DOCX)",
        ".pptx": "PowerPoint Presentation (PPTX)",
        ".doc": "Word Document (DOC)",
        ".ppt": "PowerPoint Presentation (PPT)",
    }

    match = re.search(r"(\.pdf|\.docx|\.pptx|\.doc|\.ppt)(?:\?|$)", url, re.IGNORECASE)

    return match


html_files = get_html_files("../docs/")
links = []
for item in Pipe(html_files)(extract_external_links, -1):
    links.extend(item)

links = sorted(list(set(links)))
document_links = [x for x in links if is_target_document(x)]

print("External document links identified:")
for link in document_links:
    print(f"+ [{link}]({link})")
