import requests
import pprint
# Reddit API endpoint for retrieving new posts from the "python" subreddit
subreddit = "python"
num_post_each_round = 10
num_round = 3

def get_reddit_posts(subreddit, num_post_each_round, last_post_id=None,):
    # Set up the request headers and parameters
    url = f"https://www.reddit.com/r/{subreddit}/new/.json"
    headers = {"User-Agent": "my-app/0.0.1"}
    call_params =dict(limit=num_post_each_round, after=last_post_id)
        
    # Make a request to the Reddit API
    response = requests.get(url, headers=headers, params=call_params)

    rposts = []
    # Check if the request was successful
    if response.status_code == 200:
        # Retrieve the JSON data for the next post

        posts = response.json()["data"]["children"]
        for post in posts:
            data = post["data"]
            
            # Print the text content of the post
            # print(data["selftext"])
            rposts.append(data)

            # Update the ID of the last post retrieved
            last_post_id = f'{post["kind"]}_{data["id"]}'
    else:
        # Handle errors
        print(f"Error: {response.status_code}")
    return rposts, last_post_id
    

# last_post_id = None
# for i in range(num_round):
#     print(f"Round {i+1}:")
#     posts, last_post_id = get_reddit_posts(subreddit, num_post_each_round, last_post_id)
#     pprint.pprint([post["title"] for post in posts])
#     print("")