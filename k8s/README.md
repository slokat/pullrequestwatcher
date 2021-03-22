## for kubernetes deployment

Included a sample of a very simple deployment for the application
token are mounted in env through secrets already deployed
kubectl apply -f deployment.yaml could simply deploy the app

helm could be used to template and prepare a chart for deployment.
As per the secrets handling themselves, helm secrets could be used ( not very familiar )

Could also use third party solution (hashicorp vault) to populate the kubernetes secrets

As per the deployment itself, will spawn one replica of the pod that runs the docker image previously used
no readiness/liveliness probe has been provided but we could have a command liveliness probe that would
run a small shell script to check that a given file ( in /tmp for example ) has been modified by the application
in that case we would add a simple open file in the py script to touch it ( that would be with a different sleep interval)

we would change the main script like so for instance

```
def main():
    logging.basicConfig(format='[%(asctime)s]%(message)s', level=logging.INFO, stream=sys.stdout)
    # parse os env to retrieve data
    os_env = parse_env()
    if not os_env:
        logging.error("Failed to retrieve variables from environment, aborting")
        sys.exit(1)

    sleep_count = 0
    while True:
        try:

            logging.info(f'{sleep_count},{os_env["sleep_interval"]}')
            if sleep_count % os_env["sleep_interval"] == 0:

                # open connection to github using pygithub
                g = Github(login_or_token=os_env["github_token"])
                #retrieve repository to watch
                repo = g.get_repo(os_env["github_repository"])
                # get all opened pull requests in the repository
                open_pull_requests = repo.get_pulls(state="open")
                current_date = datetime.utcnow()
                report_to_send = False
                blocks = [{"type": "section","text": {"type": "mrkdwn","text": f'*Pull requests older than {os_env["threshold"]} days not reviewed yet:*'}}]
                for pr in open_pull_requests:
                    # get reviews for each opened pull requests
                    reviews = pr.get_reviews()
                    #if pr has no review and is older than threshold // reversed here for testing
                    if  current_date - pr.created_at < timedelta(days=os_env["threshold"]):
                        #we can either notify the channel each time of build a one time message ( less spammy)
                        report_to_send = True
                        blocks.append({"type": "divider"})
                        blocks.append({"type": "section","text": {"type": "mrkdwn","text": f'<{pr.html_url}|pr {pr.id}:{pr.title}>'}})
                if len(blocks) > 1:
                    logging.info(blocks)
                    not_slack(os_env["slack_token"], os_env["slack_channel"], blocks)
                else:
                    logging.info("nothing to report :)")

            # will write every loop of 30s in a tmp file for liveliness probe
            # that can be checked
            f = open("/tmp/status", "w")
            f.write("ok")
            f.close()

        except KeyboardInterrupt:
            sys.exit()
        except:
            #SIGHUP and SIGTERM could be intercepted with signal
            logging.error(traceback.print_exc())
            logging.error(f"error :{sys.exc_info()}")
        sleep_count += 30
        sleep(30)
```
probe will be running a shell script/command like
```
#!/usr/bin/env bash
if [[ $(( $(date +%s) - $(stat /tmp/status  -c %Y) )) -gt 30 ]]
then
exit 1
else
exit 0
fi
```

container will require internet access to be able to access github website as well as slack api
