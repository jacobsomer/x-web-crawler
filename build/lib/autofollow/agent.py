import random
import time
from selenium import webdriver
from .x import XAgent
from . import github

class AutoFollowAgent:
    def __init__(self, driver_path, profile_path, github_username=None, github_password=None):
        self.driver_path = driver_path
        self.profile_path = profile_path
        self.github_username = github_username
        self.github_password = github_password
        self.driver = self.create_driver()
        self.x_agent = XAgent(self.driver)

    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        if self.profile_path:
            chrome_options.add_argument(f"user-data-dir={self.profile_path}")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        })
        chrome_options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(self.driver_path, options=chrome_options)
        return driver

    
    """
    The like_tweets method will like tweets on the user's feed for a specified amount of time.
    """
    def like_tweets(self, duration=300):
        self.x_agent.like_tweets_on_feed(self.driver, duration)
        self.close()
        
    ""
    def follow_github_users(self, url, page_number=0, duration=300):
        if not self.github_username or not self.github_password:
            raise ValueError("GitHub username and password must be provided to follow users.")
        github.follow_users(self.driver, page_number, url, (self.github_username, self.github_password), duration)
        self.close()
        
    def follow_x_users(self, users, duration=300):
        self.x_agent.follow_users(self.driver, users, duration)
        self.close()
        

    def close(self):
        self.driver.quit()
