import instaloader

def scrape_instagram_comments(username):
    # Create an Instaloader instance
    loader = instaloader.Instaloader()

    try:
        # Retrieve profile information
        profile = instaloader.Profile.from_username(loader.context, username)

        # Iterate over each post and print comments
        for post in profile.get_posts():
            print(f"\nPost URL: {post.url}")
            print("Comments:")
            for comment in post.get_comments():
                print(f"  - {comment.owner.username}: {comment.text}")

    except instaloader.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Enter the Instagram username you want to scrape comments for
    target_username = 'iam.anushka.sen'
    scrape_instagram_comments(target_username)
