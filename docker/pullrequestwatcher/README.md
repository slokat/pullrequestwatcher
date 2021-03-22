## main python script

2 modules were used :
* PyGithub for easy handling of github api
* slackclient offical python library for connection and handling to slack

Used a simple user auth token to access the repository and github api.
In a best case scenario either a robotic user token or an app token should be used

for github setup :
- either use the token of a robotic account ( in this case I use mine)
- or use a github app

for slack setup:
- created free workspace
- had to create an app, get a token for it with just channel:write (nothing else as we don't read anything)
- invite the app user in the channel /invite \@app-user

There seem to be no option for color text in the slack api and couldnt find anything backing up the use of colors
in channel messages
block formatting can be used (divider between PR for instance)

The script does not intercept any kill messages that could be sent to it ( through docker stop / kubectl delete pod for instance)
could be done with the signal module

if we want a liveliness probe we could add a open(file)/write/close(file) to a tmp file that
would be written on in a shorter interval and checked on by probe


possibly forgotten
timedelta check is reversed (for testing purposes)
