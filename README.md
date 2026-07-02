# aws-news-agent

Assists with understanding the latest AWS news using the [aws news api](https://aws-news.com) API.

Ask questions like:

- "What Bedrock models have been launched recently?"
- "What's the latest with AgentCore?"
- "Make me a powerpoint with an overview of the EKS launches over the past 60 days"


## Setup

```bash
# Install the AgentCore CLI
npm install -g @aws/agentcore

# Install CDK dependencies
cd agentcore/awsnews/agentcore/cdk
npm install

# Configure for your AWS account and region
cd ../../../..
./setup.sh

# Deploy
cd agentcore/awsnews
agentcore deploy

# Invoke and wait for response
agentcore invoke "What's the latest with Bedrock?"

# Or invoke with interactive TUI
agentcore invoke
```
