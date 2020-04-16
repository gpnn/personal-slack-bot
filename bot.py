import concurrent.futures
import sys

from slack import RTMClient


@RTMClient.run_on(event="message")
def exit_bot(**payload):
    data = payload["data"]
    web_client = payload["web_client"]

    is_human: bool = data.get("user") == config.slack_config.user_id
    bot = get_bot(data, web_client)

    if is_human:
        text_received: str = data.get("text").lower()
        logger.debug(f"Passing: {text_received}")
        concurrent.futures.ThreadPoolExecutor().submit(bot.parse_message, text_received)


@RTMClient.run_on(event="hello")
def start_bot(**payload):
    data = payload["data"]
    web_client = payload["web_client"]

    bot = get_bot(data, web_client)
    concurrent.futures.ThreadPoolExecutor().submit(bot.reddit_watch)
    concurrent.futures.ThreadPoolExecutor().submit(bot.site_watch)


@RTMClient.run_on(event="goodbye")
def reply_bot(**payload):
    sys.exit()


if __name__ == "__main__":
    logger = get_logger()
    config = get_config()
    rtm_client = RTMClient(token=config.slack_config.token)
    rtm_client.start()
