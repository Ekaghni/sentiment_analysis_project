import snscrape.modules.instagram as s_instagram
import pandas as pd

def get_instagram_comments(post_url):
    # Get the post object using InstagramPost.from_url
    
    data = pd.DataFrame(s_instagram.InstagramUserScraper('iam.anushka.sen').get_items())
    # d = s_instagram.InstagramPost('https://www.instagram.com/p/CyRBNC2InL_/?igshid=MzRlODBiNWFlZA==').comments()
    # Get the comments for the post
    # comments = list(s_instagram.comments(post))

    for index, row in data.iterrows():
        post_url = row['url']
        comments = row['comments']

        print(f"Comments for post {index + 1} ({post_url}):")
        for comment in comments:
            print(comment['text'])
        print("\n")

# Example usage
post_url = "https://www.instagram.com/p/CyRBNC2InL_/"
get_instagram_comments(post_url)

# Print the comments
# for comment in comments:
#     print(comment.content)
