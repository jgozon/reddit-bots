import praw
import re
import time

## Function Definitions ##

# Returns the post count and the user count 
def searchUserForWord(user, word):
    titleCount = 0
    selfTextCount = 0
    commentCount = 0
    word = ' ' + word + ' '
    
    # Search for word occurances in the user's post titles history
    for post in reddit.redditor(user).submissions.new(limit=None):
        stringToSearch = ' ' + post.title.lower() + ' '
        count = stringToSearch.count(word)
        titleCount += count
    
    # Search for word occurances in the user's self text history
    for post in reddit.redditor(user).submissions.new(limit=None):
        stringToSearch = ' ' + post.selftext.lower() + ' '
        count = stringToSearch.count(word)
        selfTextCount += count

    # Search for word occurances in the user's comment history
    for comment in reddit.redditor(user).comments.new(limit=None):
        stringToSearch = ' ' + comment.body.lower() + ' '
        count = stringToSearch.count(word)
        commentCount += count
    return titleCount, selfTextCount, commentCount

## Driver ##

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

keyphrase = "!searchHistory "

for comment in subreddit.stream.comments():
    if keyphrase in comment.body:
        try:
            print("Called")

            # Extract the username and comment
            tempComment = comment.body.replace(keyphrase, '')
            print(tempComment)
            user = tempComment.split(' ', 1)[0]
            print(user)
            tempComment = tempComment.replace(user + ' ', '')
            print(tempComment)
            searchWord = tempComment
            searchWord = searchWord.lower()

            # Find the occurances
            titleCount, selfTextCount, commentCount = searchUserForWord(user, searchWord)
            print("Finished")

            # Post the results
            comment.reply("Analysis for u/" + user + " completed. \n" + 
                            "Total Occurances: " + str(titleCount + selfTextCount + commentCount) + "\n" +
                            "u/" + user + " has said " + str(searchWord) + " " + str(titleCount) + " times in titles, " +
                            str(selfTextCount) + " times in post texts, and " + commentCount + " times in comments.")
        except:
            print("Error in comment formatting or other")
        


