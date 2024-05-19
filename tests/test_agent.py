import unittest
from unittest.mock import patch, MagicMock
from autofollow.agent import AutoFollowAgent
from selenium import webdriver

class TestAutoFollowAgent(unittest.TestCase):
    def setUp(self):
        self.driver_path = "/Users/jacobsomer/Documents/side_prod/salesBook/chromedriver-mac-arm64/chromedriver"
        self.github_username = "jacobsomer"
        self.github_password = "BorderCollie5*"
        self.agent = AutoFollowAgent(
            driver_path=self.driver_path,
            github_username=self.github_username,
            github_password=self.github_password
        )

    def tearDown(self):
        self.agent.close()

    def test_create_driver(self):
        driver = self.agent.create_driver()
        self.assertIsInstance(driver, webdriver.Chrome)
        driver.quit()

    @patch('autofollow.x.like_tweets_on_feed')
    def test_like_tweets(self, mock_like_tweets_on_feed):
        self.agent.like_tweets(duration=300)
        mock_like_tweets_on_feed.assert_called_once_with(self.agent.driver, 300)

    @patch('autofollow.github.follow_users')
    def test_follow_github_users(self, mock_follow_users):
        url = "https://github.com/orgs/Azure/people"
        self.agent.follow_github_users(url, page_number=0, duration=300)
        mock_follow_users.assert_called_once_with(
            self.agent.driver,
            0,
            url,
            (self.github_username, self.github_password),
            300
        )

    @patch('autofollow.x.follow_users')
    def test_follow_x_users(self, mock_follow_users):
        users = ["user1", "user2"]
        self.agent.follow_x_users(users, duration=300)
        mock_follow_users.assert_called_once_with(self.agent.driver, users, 300)

    @patch('autofollow.agent.AutoFollowAgent.close')
    def test_close(self, mock_close):
        self.agent.close()
        mock_close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
