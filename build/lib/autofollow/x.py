from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class XAgent:
    def __init__(self, driver):
        self.driver = driver
        self.likes = set()
        self.followed = set()
        
    def is_ad(self, tweet):
        try:
            tweet.find_element(By.XPATH, ".//span[text()='Ad']")
            return True
        except Exception:
            return False

    def like_tweet(self, tweet):
        
        try:
            tweet_id = tweet.find_element(By.XPATH, ".//a[contains(@href, '/status/')]").get_attribute("href").split("/")[-1]
            print(f"Tweet ID: {tweet_id}")
            if tweet_id and tweet_id not in self.likes:
                like_button = tweet.find_element(By.XPATH, ".//button[contains(@aria-label, 'Likes. Like')]")
                if like_button.is_enabled() and like_button.is_displayed():
                    like_button.click()
                    print(f"Liked tweet: {tweet_id}")
                    self.likes.add(tweet_id)
                    time.sleep(1)  # Short delay after each like action
                    return True
            return False
        except Exception as e:
            print(f"Failed to like tweet: {e}")
            return False

    def like_tweets_on_feed(self, driver, run_time=300):
        driver.get("https://x.com/home")
        start_time = time.time()
        while time.time() - start_time < run_time:
            time.sleep(2)
            try:
                tweets = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
                )

                non_ad_tweets = [tweet for tweet in tweets if not self.is_ad(tweet)]

                for tweet in non_ad_tweets:
                    self.like_tweet(tweet)

            except Exception as e:
                print(f"Error during tweet processing: {e}")

            try:
                driver.execute_script("window.scrollBy(0,1000)")
            except Exception as e:
                print(f"Failed to scroll: {e}")
            time.sleep(3)
            

    def follow_users(self, driver, users, duration=300):
        start_time = time.time()
        for user in users:
            if time.time() - start_time > duration:
                break
            user = user.replace("https://x.com/", "")
            user = user.replace("https://twitter.com/", "")
            driver.get(f"https://x.com/{user}")
            try:
                follow_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Follow')]"))
                )
                follow_button.click()
                time.sleep(2)
            except Exception as e:
                print(f"Error following user {user}: {e}")
        