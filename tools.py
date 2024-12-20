import datetime
import requests


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

    page_size = 20
    url = f"https://api.aws-news.com/articles?page_size={page_size}&article_type=news&search={
        topic}"
    response = requests.get(url)
    data = response.json()
    return data["articles"]


def lookup_aws_news_article_details(url: str) -> str:
    """
    Fetches the details of an AWS news article from the specified url.

    Returns the article HTML
    """
    response = requests.get(url)
    return response.text
