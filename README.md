# AutoFollow

AutoFollow is a Python package for automating interactions on social media platforms like Twitter (X) and GitHub.

## Installation

You can install AutoFollow using pip:

```bash
pip install autofollow
```

## Usage

Here’s an example of how to use AutoFollow to automate actions on Twitter (X) and GitHub:

```python
from autofollow.agent import AutoFollowAgent

def main():
    driver_path = "YOUR_DRIVER_PATH"
    twitter_username = "YOUR_TWITTER_USERNAME"
    twitter_password = "YOUR_TWITTER_PASSWORD"
    github_username = "YOUR_GITHUB_USERNAME"
    github_password = "YOUR_GITHUB_PASSWORD"
    url = "https://github.com/orgs/Azure/people"

    agent = AutoFollowAgent(
        driver_path=driver_path,
        twitter_username=twitter_username,
        twitter_password=twitter_password,
        github_username=github_username,
        github_password=github_password
    )

    try:
        agent.like_tweets(duration=300)
        agent.follow_twitter_users(["https://x.com/minimario1729"], duration=300)
        agent.follow_github_users(url, page_number=0, duration=300)
    finally:
        agent.close()

if __name__ == "__main__":
    main()
```

### AutoFollowAgent Methods

#### `like_tweets(duration=300)`

Likes tweets on the user's feed for the specified duration.

#### `follow_twitter_users(users, duration=300)`

Follows the specified Twitter (X) users for the specified duration.

#### `follow_github_users(url, page_number=0, duration=300)`

Follows users on GitHub starting from the specified page number for the specified duration.

### Running Tests

To run the tests for this package, use the `unittest` framework:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
