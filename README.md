# reddit-bots
This repository consists of the source code for the small reddit bots that I created. Anyone is free to use these bots as they wish.

## How can I use these bots?
Currently, these bots only work on r/testingground4bots. You will need to add all of the subreddits that you want the bot to respond in
by manually adding the desired subreddits to the subreddit list in the source code. You will also need to manually fill out the
clientUsername, clientPassword, clientID, and clientSecret variables which can be created with a reddit account. Finally, you will need to
install PRAW, the Python Reddit API Wrapper.

## Will these bots respond to every reddit comment?
To prevent spam, all the bots in this repository are triggered by a certain keyword. This can easily be changed by removing the if statement which checks whether or not the keyword exists in the comment.

## Are these bots currently running?
I am currently not running any of these bots as I do not have a server or extra computer that I can use to run these programs 24/7. If they are working, someone else is probably running them.
