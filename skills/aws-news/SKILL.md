---
name: aws-news
description: "Fetch the latest AWS announcements, blog posts, and news for specific AWS services using the aws-news.com API. Use when the user asks about recent AWS launches, features, service updates, or wants to stay current on AWS news."
---

# AWS News API Skill

Use the public AWS News API at `https://api.aws-news.com` to fetch recent AWS announcements, blog posts, and service news. This replaces the need for an MCP tool — you can call the API directly via HTTP.

## API Endpoint

```
GET https://api.aws-news.com/articles?{query_params}
```

## Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search` | string | Yes | — | AWS topic or service to search for (e.g., `s3`, `lambda`, `bedrock`, `mcp`) |
| `page_size` | integer | No | 40 | Maximum number of results to return |
| `article_type` | string | No | — | Filter by type: `news` or `blog`. Omit for both. |
| `since` | string | No | — | ISO 8601 date to filter results from (e.g., `2025-01-01T00:00:00Z`) |
| `hide_regional_expansions` | boolean | No | `true` | Set to `false` to include regional expansion announcements |

## Example Requests

```
# News/launches about S3 (default: news only)
https://api.aws-news.com/articles?search=s3&article_type=news&page_size=40&hide_regional_expansions=true

# Only blog posts about EC2
https://api.aws-news.com/articles?search=ec2&article_type=blog&page_size=20&hide_regional_expansions=true

# Lambda launches since January 2025
https://api.aws-news.com/articles?search=lambda&article_type=news&since=2025-01-01T00:00:00Z&page_size=40&hide_regional_expansions=true

# All DynamoDB content (news + blogs) including regional expansions
https://api.aws-news.com/articles?search=dynamodb&page_size=40&hide_regional_expansions=false
```

## Response Format

The API returns a JSON array of article objects. Each article contains fields like title, description, date, URL, and article type.

## How to Use This Skill

When the user asks about AWS news, announcements, or recent launches:

1. **Identify the topic** — Extract the AWS service or topic from the user's question (e.g., "bedrock", "lambda", "eks", "mcp", "agents").

2. **Determine filters** — Based on the question:
   - **Default to `article_type=news`** — Unless the user explicitly asks for "blogs" or "blog posts", always set `article_type=news`. Launches, announcements, "what's new", and "what's the latest" all mean news articles only.
   - If they explicitly ask about "blogs" or "blog posts" → set `article_type=blog`
   - If they ask for "everything" or "news and blogs" → omit `article_type` to get both
   - If they mention a timeframe (e.g., "past 30 days", "since March") → calculate the `since` date in ISO 8601
   - If they ask about regional availability → set `hide_regional_expansions=false`

3. **Make the HTTP GET request** — Call the API with the constructed URL.

4. **Summarize the results** — Present the news in a clear, organized format:
   - Group by relevance or date
   - Include the article title, date, and a brief description
   - Link to the original article URL when available
   - Call out the most significant launches or features

## Tips for Effective Use

- **Use short service names** for the search term: `s3`, `lambda`, `ec2`, `bedrock`, `eks`, `ecs`, `mcp` — not the full "Amazon Simple Storage Service".
- **Default to hiding regional expansions** unless the user specifically asks about availability in new regions. Regional expansion news is high-volume and usually low-signal.
- **Default page_size of 40** is good for most queries. Use a smaller value (10-20) for focused questions, or larger (100) for comprehensive overviews.
- **Calculate "since" dates** relative to today. If the user says "past 30 days", compute the date 30 days ago in ISO 8601 format.
- **Multiple topics**: If the user asks about multiple services, make separate API calls for each topic and combine the results.
- **Presentation**: When summarizing results, lead with the most impactful launches. Users typically care most about new capabilities, not minor updates.

## Common User Queries → API Calls

| User asks... | search | article_type | since | hide_regional_expansions |
|---|---|---|---|---|
| "What's new with Bedrock?" | `bedrock` | `news` | last 30 days | `true` |
| "Latest Lambda blog posts" | `lambda` | `blog` | (omit) | `true` |
| "EKS launches in the past 60 days" | `eks` | `news` | 60 days ago | `true` |
| "Is DynamoDB available in new regions?" | `dynamodb` | `news` | (omit) | `false` |
| "What's the latest with AgentCore?" | `agentcore` | `news` | last 90 days | `true` |
| "Recent announcements about MCP" | `mcp` | `news` | last 90 days | `true` |
| "All Bedrock news and blogs" | `bedrock` | (omit) | last 30 days | `true` |
