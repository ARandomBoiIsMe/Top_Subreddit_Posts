# Top Subreddit Posts
A script that locates the most upvoted posts in a subreddit within a specified timeframe and makes a stickied post listing them in order.

## Installation
- Install Python. You can download it here https://www.python.org/downloads/ (Add to PATH during the installation).  
- Download the ZIP file of this repo (Click on ```Code``` -> ```Download ZIP```).
- Unzip the ZIP file.
- Open your command prompt and change your directory to that of the unzipped files.  
- Install the required packages:
  ```
  pip install -U praw python-dateutil
  ```
## Configuration
- Create a Reddit App (script) at https://www.reddit.com/prefs/apps/ and get your ```client_id``` and ```client_secret```.  
- Edit the ```config.ini``` file with your details and save:
  ```
  [REDDIT]
  CLIENT_ID = your_client_id
  CLIENT_SECRET = your_client_secret
  PASSWORD = your_reddit_password
  USERNAME = your_reddit_username
  
  [VARS]
  SUBREDDIT = target_subreddit_name
  NUMBER_OF_POSTS = preferred_number_of_posters_to_track
  TIMEFRAME = preferred_time_period (W for Weeks, M for Months)
  TIMERANGE = preferred_time_range (1 OR 2 OR 3...)
  ```

  ## Running the script
  Set up a task to run the program every week/month.
  
  Replace ```C:\path\to\the\main.py``` with the actual path to the main.py file. Don't remove the quotation marks.    
  Replace ```HH:MM``` with your preferred running time, in 24-hour format. (ie, 15:00 for 3PM).  
  Open your command prompt (Windows) and enter:  
    - Weekly:
      ```
      schtasks /create /tn MostUpvotedPostsWeekly /tr "C:\path\to\the\main.py" /sc weekly /d SUN /st HH:MM
      ```

    - Monthly:
      ```
      schtasks /create /tn MostUpvotedPostsMonthly /tr "C:\path\to\the\main.py" /sc monthly /mo lastday /m * /st HH:MM
      ```

  
