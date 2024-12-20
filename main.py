import logging
from log import debug, info, warn, error
from log import llm as log_llm
import boto3
from bedrock_tools import BedrockTools
import tools

bedrock = boto3.client("bedrock-runtime")
model_id = "us.anthropic.claude-3-haiku-20240307-v1:0"

# The maximum number of recursive calls allowed
# This helps prevent infinite loops and potential performance issues.
MAX_RECURSIONS = 50
TEMPERATURE = 0.0
TOP_P = 0.999

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)

# initialize Bedrock tools
tool_manager = BedrockTools()
tool_manager.add_function(tools.get_current_date_time)
tool_manager.add_function(tools.get_aws_news_articles)
tool_manager.add_function(tools.lookup_aws_news_article_details)
info(tool_manager.get_tool_config())

system_prompt = """
You are an AWS news assistant. You help your users understand what new
services and features that AWS is launching. Be sure to include dates
when sharing news.
"""


def process_model_response(model_response, messages, max_recursion=5):

    if max_recursion <= 0:
        logging.warning(
            "Warning: Maximum number of recursions reached. Please try again.")
        raise Exception("Maximum number of recursions reached.")

    # Append the model's response to the ongoing conversation
    message = model_response["output"]["message"]
    messages.append(message)

    stop_reason = model_response["stopReason"]
    logging.info(f"ITERATION {max_recursion}, STOP_REASON: {stop_reason}")

    if stop_reason == "tool_use":
        return handle_tool_use(message, messages, max_recursion)

    if stop_reason == "end_turn":
        print(model_response["output"]["message"]["content"][0]["text"] + "\n")
        return model_response["output"]["message"]["content"][0]["text"]


def handle_tool_use(model_response, messages, max_recursion=5):

    # Initialize an empty list of tool results
    tool_results = []

    # The model's response can consist of multiple content blocks
    for content_block in model_response["content"]:

        # optionally print any text to the console
        if "text" in content_block:
            print(content_block["text"] + "\n")

        # invoke the tool and add it to the list of results
        if "toolUse" in content_block:
            tool_response = tool_manager.invoke(content_block["toolUse"])
            tool_results.append(tool_response)

    # Embed the tool results in a new user message
    message = {"role": "user", "content": tool_results}

    # Append the new message to the ongoing conversation
    messages.append(message)

    request = {
        "modelId": model_id,
        "messages": messages,
        "inferenceConfig": {
            "temperature": TEMPERATURE,
            "topP": TOP_P,
        },
    }

    # Send the conversation to Amazon Bedrock
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        system=[{"text": system_prompt}],
        inferenceConfig={
            "temperature": TEMPERATURE,
            "topP": TOP_P,
        },
        toolConfig=tool_manager.get_tool_config(),
    )

    log_llm(request, response)

    # Recursively handle the model's response until the model has returned
    # its final response or the recursion counter has reached 0
    return process_model_response(response, messages, max_recursion - 1)


def get_user_input():
    user_input = input("AWS News Assistant (x to exit):  ")
    if user_input.lower() == "x":
        return None
    return user_input


def main():

    # Start with an emtpy conversation
    messages = []

    # Get the first user input
    user_input = get_user_input()

    # repl loop
    while user_input is not None:

        # Create a new message with the user input and append it to the conversation
        message = {"role": "user", "content": [{"text": user_input}]}
        messages.append(message)

        request = {
            "modelId": model_id,
            "messages": messages,
            "inferenceConfig": {
                "temperature": TEMPERATURE,
                "topP": TOP_P,
            },
        }

        # Send the conversation to Amazon Bedrock
        response = bedrock.converse(
            modelId=model_id,
            messages=messages,
            system=[{"text": system_prompt}],
            inferenceConfig={
                "temperature": TEMPERATURE,
                "topP": TOP_P,
            },
            toolConfig=tool_manager.get_tool_config(),
        )

        log_llm(request, response)

        # agentic loop
        # Recursively handle the model's response until the model has returned
        # its final response or the recursion counter has reached 0
        process_model_response(
            response, messages, max_recursion=MAX_RECURSIONS)

        # Repeat the repl loop until the user decides to exit the application
        user_input = get_user_input()


if __name__ == "__main__":
    main()
