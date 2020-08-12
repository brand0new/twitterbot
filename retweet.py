import logging
import time
from api_config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def quotetweet(usedids, api, user):

    # Local variables needed
    highestTweetCount = 0
    tweetIndex = 0
    bestTweetIndex = 0

    # Get the latest timeline update
    tweets = api.user_timeline(id=user.id, exclude_replies=True, include_rts=False, count=200)

    # Iterate through all the Tweets on the timeline
    # Store highest tweet count
    # Store best tweet index
    for tweet in tweets:
        if tweet.id not in usedids:
            if tweet.favorite_count > 5000:
                if tweet.favorite_count > highestTweetCount:
                    highestTweetCount = tweet.favorite_count
                    bestTweetIndex = tweetIndex
            tweetIndex += 1

    # Get the complete tweet object based by id
    tweet = api.get_status(tweets[bestTweetIndex].id, include_entities=True, include_ext_alt=True)

    # Create a tweet
    try:
        api.update_status(f"\"{tweet.text}\" - Best of @{user.screen_name}")
        logging.info("Tweet created!")
        logging.info(f"Favorites: {tweet.favorite_count} | RT: {tweet.retweet_count} | Posted: {tweet.created_at} | {tweet.text}")

    except Exception as e:
        logging.error("Error when trying to post", exc_info=True)
        raise e

    return tweet.id


# Create API object
api = create_api()

# Set target user object
user = api.get_user("Max33Verstappen")

# Print out logging
logger.info("This Twitter bot is targeting the following user: ")
logger.info(f"{user.name} ({user.id}) | # of Tweets {user.statuses_count} | {user.description} | {user.location}")

usedids = []

while True:
    usedids.append(quotetweet(usedids, api, user))
    time.sleep(1800)
