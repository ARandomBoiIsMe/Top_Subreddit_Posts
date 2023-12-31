from utilities import config_util, reddit_util
import prawcore
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import time

config = config_util.load_config()
reddit = reddit_util.initialize_reddit(config)
number_of_posts = int(config['VARS']['NUMBER_OF_POSTS'])
timeframe = config['VARS']['TIMEFRAME'].lower()
timerange = int(config['VARS']['TIMERANGE'])

def main():
    subreddit_name = config['VARS']['SUBREDDIT']
    subreddit = validate_subreddit(subreddit_name)
    if not subreddit_name:
        print(f"This subreddit does not exist: r/{subreddit_name}.")
        exit()

    if not subreddit.user_is_moderator:
        print(f"You must be a mod in this sub: r/{subreddit_name}.")
        exit()

    delete_previous_stickied_post(subreddit)

    posts = get_previous_posts(subreddit)

    create_stickied_post(posts, subreddit)

def validate_subreddit(subreddit_name):
    if subreddit_name.strip() == '' or subreddit_name is None:
        return None
    
    try:
        return reddit.subreddits.search_by_name(subreddit_name, exact=True)[0]
    except prawcore.exceptions.NotFound:
        return None

def delete_previous_stickied_post(subreddit):
    print("Deleting previous generated post...")

    try:
        # Cycles through sticky posts until it finds the one
        # generated by the program
        sticky_post = None
        for i in range(1, 3):
            if "Most Upvoted Posts" in subreddit.sticky(number=i).title:
                sticky_post = subreddit.sticky(number=i)
                break

        if sticky_post == None:
            return
    
        sticky_post.delete()

        print("Post deleted.")

    except prawcore.NotFound:
        return

def get_previous_posts(subreddit):
    print("Getting previous posts...")

    posts = subreddit.new()

    # Generates time range to search for posts
    time_range = None
    if timeframe == 'd':
        time_range = timedelta(days=timerange)
    elif timeframe == 'w':
        time_range = timedelta(weeks=timerange)
    elif timeframe == 'm':
        time_range = relativedelta(months=timerange)
    else:
        print("The inputted timeframe is not supported. Please use either weeks or months.")
        exit()
    
    # Filters out posts not in that range
    filtered_posts = []
    for post in posts:
        post_creation_date = datetime.fromtimestamp(post.created_utc)
        if (post_creation_date > (datetime.today() - time_range)):
            filtered_posts.append(post)
        else:
            break
    
    print("Posts retrieved.")

    # Sorts from most upvoted to least upvoted
    return sorted(filtered_posts, key=lambda x: x.score, reverse=True)

def create_stickied_post(posts, subreddit):
    global number_of_posts

    # Ensures that the actual number of posters is used, to avoid errors
    if (number_of_posts > len(posts)):
        number_of_posts = len(posts)

    # Creates appropriate title
    title = None
    if timeframe == 'd':
        if timerange == 1:
            title = f"Most Upvoted Posts of the past day."
        else:
            title = f"Most Upvoted Posts of the past {timerange} days."
    elif timeframe == 'w':
        if timerange == 1:
            title = f"Most Upvoted Posts of the past week."
        else:
            title = f"Most Upvoted Posts of the past {timerange} weeks."
    elif timeframe == 'm':
        if timerange == 1:
            title = f"Most Upvoted Posts of the past month."
        else:
            title = f"Most Upvoted Posts of the past {timerange} months."

    # Builds the post body table
    body = """&#x200B;

|Rank|Post Link|Upvotes|Post Author|
|:-|:-|:-|:-|\n"""

    i = 1
    for post in posts:
        if i > number_of_posts:
            break

        body += f"|{i}|https://www.reddit.com/{post.permalink}|{post.score}|u/{post.author}|\n"
        i += 1

    body += "\n&#x200B;"

    print("Making post...")

    submission = subreddit.submit(
        title=title,
        selftext=body
    )

    time.sleep(3)

    # Stickies post
    submission.mod.sticky()

    print("Post submitted and stickied.")

if __name__ == '__main__':
    main()