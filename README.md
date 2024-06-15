
# x-web-crawler

x-web-crawler is a Python package for automating interactions on social media platforms like Twitter (X) and GitHub.

## Installation

You can install x-web-crawler using [pip](https://pypi.org/project/x-web-crawler/):

```bash
pip install x-web-crawler
```

## Usage

Here’s an example of how to use x-web-crawler to automate actions on Twitter (X) and GitHub:

```python
from xagent import XAgent

def main():
    driver_path = "YOUR_DRIVER_PATH"
    profile_path = "YOUR_PROFILE_PATH"
    twitter_username = "YOUR_TWITTER_USERNAME" # works best with your twitter handle and not email
    twitter_password = "YOUR_TWITTER_PASSWORD"
    url = "https://github.com/orgs/Azure/people"

    agent = XAgent(
        driver_path=driver_path,
        profile_path=profile_path,
        x_username=twitter_username,
        x_password=twitter_password,
    )

    try:
        agent.like_x_posts(duration=300)
        agent.follow_x_users(["https://x.com/jacob_somer_"], duration=300)
    finally:
        agent.close()

if __name__ == "__main__":
    main()
```

### XAgent Methods

#### `__init__(self, driver_path, profile_path, x_username=None, x_password=None, browser="chrome")`

Initializes the XAgent.

- `driver_path`: Path to the ChromeDriver executable. Download ChromeDriver from [here](https://googlechromelabs.github.io/chrome-for-testing/).
- `profile_path`: Path to the user profile directory for Chrome. To find this, type "chrome://version" into your Chrome browser's address bar, and look for the "Profile Path" variable.
- `x_username` (optional): Twitter (X) username for authentication.
- `x_password` (optional): Twitter (X) password for authentication.
- `browser`: The browser to use, either "chrome" or "edge".

#### `like_x_posts(duration=300)`

Likes posts on the user's feed for the specified duration.

#### `follow_x_users(users, duration=300)`

Follows the specified Twitter (X) users for the specified duration.

#### `get_x_followers(username)`

Gets the followers of a specified Twitter (X) user.

#### `get_x_following(username)`

Gets the users that a specified Twitter (X) user is following.

#### `unfollow_x_users(users)`

Unfollows the specified Twitter (X) users.

#### `unfollow_x_users_alternative(user, users)`

Unfollows the specified Twitter (X) users using an alternative method.

#### `get_x_handles(query, num_handles=10)`

Gets the handles of users based on a query.

### Running Tests

To run the tests for this package, use the `unittest` framework:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
