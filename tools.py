import datetime
import requests
from html2text import HTML2Text
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_current_date_time() -> str:
    """
    Returns the current date and time in the format "YYYY-MM-DD HH:MM:SS".
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_aws_news_articles(topic: str) -> list:
    """
    Returns a list of AWS news articles with announcements
    of new products, services, and capabilities for the specified aws topic/service.

    For example: If asked for the "latest bedrock announcements", you would call
    `get_aws_news_articles("load balancer")`

    This tool returns data in the following format:
    [
        {
            "id": "0193bd2d-09d5-4e40-1631-b4cdcf141344",
            "url": "https://aws.amazon.com/about-aws/whats-new/2024/12/amazon-bedrock-guardrails-languages-spanish-french/",
            "title": "Amazon Bedrock Guardrails now supports additional languages - Spanish and French",
            "external_id": "whats-new-v2#p175378537",
            "created_date": "2024-12-09T20:09:19Z",
            "updated_date": "2024-12-12T23:17:04Z",
            "published_date": "2024-12-12T23:21:05.749000Z",
            "type": "News",
            "popular": null,
            "main_category": null
        },
        {
            "id": "0193b1df-0de1-738c-9e3a-25a870d29f42",
            "url": "https://aws.amazon.com/about-aws/whats-new/2024/12/amazon-bedrock-guardrails-reduces-pricing-85-percent",
            "title": "Amazon Bedrock Guardrails reduces pricing by up to 85%",
            "external_id": "whats-new-v2#p173175971",
            "created_date": "2024-12-05T17:22:25Z",
            "updated_date": "2024-12-10T18:36:08Z",
            "published_date": "2024-12-10T18:40:05.601000Z",
            "type": "News",
            "popular": null,
            "main_category": null
        }
    ]
    """

    page_size = 40
    url = f"https://api.aws-news.com/articles?page_size={page_size}&article_type=news&search={
        topic}"
    response = requests.get(url)
    data = response.json()
    return data["articles"]


# def lookup_aws_news_article_details(url: str) -> str:
#     """
#     Fetches the details of an AWS news article from the specified url.

#     Returns the article HTML
#     """
#     response = requests.get(url)
#     return response.text

def fetch_webpage(url: str) -> str:
    """
    Fetches a webpage and converts it to markdown format.

    Args:
        url (str): The URL of the webpage to fetch

    Returns:
        str: The webpage content in markdown format
    """

    print()
    print(f"Reading URL: {url}")
    print()
    try:
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Create HTML2Text instance with custom settings
        h2t = HTML2Text()
        h2t.ignore_links = False
        h2t.ignore_images = True
        h2t.ignore_tables = False
        h2t.ignore_emphasis = False
        h2t.body_width = 0  # Disable line wrapping

        # Parse with BeautifulSoup first to clean the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'iframe']):
            element.decompose()

        # Convert relative URLs to absolute URLs
        for tag in soup.find_all(['a', 'img']):
            if tag.get('href'):
                tag['href'] = urljoin(url, tag['href'])
            if tag.get('src'):
                tag['src'] = urljoin(url, tag['src'])

        # Convert to markdown
        markdown = h2t.handle(str(soup))

        # Clean up the markdown
        markdown = '\n'.join(
            line for line in markdown.splitlines() if line.strip())

        # # Truncate if max_length is specified
        # if max_length and len(markdown) > max_length:
        #     markdown = markdown[:max_length] + "..."

        return markdown

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch webpage: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing webpage: {str(e)}")
