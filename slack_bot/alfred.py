import time

from slackclient import SlackClient

from config import slack_token, slack_scim_token
from slackscimclient import SlackSCIMClient

token = slack_token
scim_token = slack_scim_token
sc = SlackClient(token)
scim = SlackSCIMClient(token=scim_token)

# connect to real time messaging
if sc.rtm_connect():
    while True:
        activity = sc.rtm_read()

        # if we got any activity
        if len(activity) > 0:
            # if it was a text message
            if 'text' in activity[0]:
                message = str(activity[0]['text']).lower()
                # TODO: multiple channels
                channel = activity[0]['channel']

                if 'alfred' in message:
                    if 'find' in message:
                        search = message.replace("alfred", "").replace("find",
                                                                       "").lstrip().rstrip()
                        users = scim.find_user(name=search)
                        # TODO: didn't find anyone
                        photo = users[0]['photos'][0]['value']
                        name = users[0]['nickName']
                        attachments = [{'image_url': photo, 'title': name}]

                        if users:
                            # post message
                            sc.api_call("chat.postMessage",
                                        channel=channel,
                                        text="this one?",
                                        attachments=attachments,
                                        username="Alfred")

        time.sleep(0.5)
else:
    print("Connection Failed, invalid token?")
