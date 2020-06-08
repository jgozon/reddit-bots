import praw
import requests
import json

## Function Definitions ##

# Extracts links from comments by parsing the HTML, searching for href="" tags
def extractLinks(comment_html):
    links = []
    currentString = comment_html

    # While there exists a link in the html
    while("href=\"" in currentString):
        linkBegin = currentString.find("href=\"") + 6
        linkEnd = currentString.find('\"', linkBegin)
        links.append(currentString[linkBegin:linkEnd])
        currentString = currentString[linkEnd+1:]
    
    return links

# Returns list of external links
def checkLinks(potentialLinks):
    # If a link begins with '/'  --> INTERNAL/SAFE
    # If a link begins with http --> EXTERNAL/CHECK
    dangerousLinks = []
    
    linkNumber = 0
    for link in potentialLinks:
        linkNumber += 1
        if (link[0] == "/"):
            pass
        elif (link.startswith('http')):
            if (isDangerous(link)):
                dangerousLinks.append(linkNumber)

    if (len(dangerousLinks) == 0):
        return True, dangerousLinks
    else:
        return False, dangerousLinks

# Sends a POST request to Google's API to check if a link is dangerous or not
def isDangerous(link):
    api_key = 'redacted'
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {'client': {'clientId': "mycompany", 'clientVersion': "0.1"},
        'threatInfo': {'threatTypes': ["SOCIAL_ENGINEERING", "MALWARE", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                       'platformTypes': ["ANY_PLATFORM"],
                       'threatEntryTypes': ["URL"],
                       'threatEntries': [{'url': link}]}}
    params = {'key': api_key}
    r = requests.post(url, params=params, json=payload)
    
    # Link is safe if the response from request response is empty
    if (str(r.json()) == "{}"):
        return False
    else:
        return True

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

keyphrase = "!checkLink "

for comment in subreddit.stream.comments():
    if keyphrase in comment.body:
        try:
            print("Bot Called")

            # Find all links in the comment
            potentialLinks = extractLinks(comment.body_html)
            
            # If no links were detected, exit
            if (len(potentialLinks) == 0):
                comment.reply("No links were found in your comment")
                continue
            
            # Check all the external links for malware and phishing
            allSafe, dangerousLinks = checkLinks(potentialLinks)

            # Alert the user based on the safety of the links
            if (allSafe):
                comment.reply("All the links in the comment above are safe (or inactive) according to Google's Safe Browsing API")
            else:
                comment.reply("According to Google's Safe Browsing API, the following links are not safe (listed in the order they appear in the comment) \n \n "
                                + str(dangerousLinks))
        except:
            print("Error in comment formatting or other")
