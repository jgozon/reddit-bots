import praw
import re
import time

# Add your own credentials to this program
clientUsername = 'redacted'
clientPassword = 'redacted'
clientID = 'redacted'
clientSecret = 'redacted'

reddit = praw.Reddit(client_id=clientID,
                     client_secret=clientSecret,
                     user_agent='console:tasker_bot:0.0.1 Created by /u/',
                     username=clientUsername,
                     password=clientPassword)

# Place this bot in the testing subreddit
subreddit = reddit.subreddit('testingground4bots')

# Prompt for keyphrase
keyphrase = input("Enter your keyphrase: ")
keyphrase = ' ' + keyphrase + ' '

# Prompt for reply
reply = input("Enter your reply: ")

for comment in subreddit.stream.comments():
    # Alter the comment to ensure that we aren't performing simple substring matching
    actualComment = ' ' + comment.body + ' '

    if keyphrase in actualComment:
        try:
            comment.reply(reply)
        except:
            print("Error in comment formatting or other")
        


