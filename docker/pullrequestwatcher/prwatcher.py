import sys
import os
import logging
import traceback
from time import sleep
from datetime import datetime, timedelta
from slack import WebClient
from slack.errors import SlackApiError
from github import Github

def parse_env():
    """Read os env var and return it"""
    os_env = {}
    try:
        os_env["github_token"] = os.environ["GITHUB_TOKEN"]
        os_env["github_repository"] = os.environ["GITHUB_REPOSITORY"]
        os_env["threshold"] = int(os.environ["THRESHOLD"])
        os_env["slack_channel"] = os.environ["SLACK_CHANNEL"]
        os_env["slack_token"] = os.environ["SLACK_TOKEN"]
        os_env["sleep_interval"] = int(os.environ["SLEEP_INTERVAL"])
        return os_env
    except KeyError as e:
        logging.error(f"failed to retrieve variable from env: {e}")
        return {}

def notify_slack_message(token, channel, message):
    """Send text message to slack channel """
    client = WebClient(token=token)
    try:
        response = client.chat_postMessage(
        channel=channel,
        text=message)
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")

def notify_slack_blocks(token, channel, blocks):
    """Send blocks message to slack channel """
    client = WebClient(token=token)
    try:
        response = client.chat_postMessage(
        channel=channel,
        blocks=blocks)
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")

def main():
    logging.basicConfig(format='[%(asctime)s]%(message)s', level=logging.INFO, stream=sys.stdout)
    # parse os env to retrieve data
    os_env = parse_env()
    if not os_env:
        logging.error("Failed to retrieve variables from environment, aborting")
        sys.exit(1)
    while True:
        try:
            # open connection to github using pygithub
            g = Github(login_or_token=os_env["github_token"])
            #retrieve repository to watch
            repo = g.get_repo(os_env["github_repository"])
            # get all opened pull requests in the repository
            open_pull_requests = repo.get_pulls(state="open")
            current_date = datetime.utcnow()
            # init first part of the block for the message to send
            blocks = [{"type": "section","text": {"type": "mrkdwn","text": f'*Pull requests older than {os_env["threshold"]} days not reviewed yet:*'}}]
            for pr in open_pull_requests:
                # get reviews for each opened pull requests
                reviews = pr.get_reviews()
                #if pr has no review and is older than threshold
                if reviews.totalCount == 0 and current_date - pr.created_at > timedelta(days=os_env["threshold"]):
                    #we can either notify the channel each time of build a one time message ( less spammy)
                    blocks.append({"type": "divider"})
                    blocks.append({"type": "section","text": {"type": "mrkdwn","text": f'<{pr.html_url}|pr {pr.id}:{pr.title}>'}})
            if len(blocks) > 1:
                logging.info(blocks)
                notify_slack_blocks(os_env["slack_token"], os_env["slack_channel"], blocks)
            else:
                # could send the message to slack with notify_slack_message
                logging.info("nothing to report :)")

        except KeyboardInterrupt:
            sys.exit(1)
        except:
            #SIGHUP, SIGINT and SIGTERM could be intercepted with signal module
            # as the app is not writing anything of value, not really required
            logging.error(f"error :{traceback.print_exc()}")
        sleep(os_env["sleep_interval"])
if __name__ == '__main__':
    main()
