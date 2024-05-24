from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import StaleElementReferenceException # type: ignore
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

    def like_tweets_on_feed(self, run_time=300):
        self.driver.get("https://x.com/home")
        start_time = time.time()
        while time.time() - start_time < run_time:
            time.sleep(2)
            try:
                tweets = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
                )

                non_ad_tweets = [tweet for tweet in tweets if not self.is_ad(tweet)]

                for tweet in non_ad_tweets:
                    self.like_tweet(tweet)

            except Exception as e:
                print(f"Error during tweet processing: {e}")

            try:
                self.driver.execute_script("window.scrollBy(0,1000)")
            except Exception as e:
                print(f"Failed to scroll: {e}")
            time.sleep(3)
            

    def follow_users(self, users, duration=300):
        start_time = time.time()
        for user in users:
            if time.time() - start_time > duration:
                break
            user = user.replace("https://x.com/", "")
            user = user.replace("https://twitter.com/", "")
            self.driver.get(f"https://x.com/{user}")
            try:
                follow_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Follow')]"))
                )
                follow_button.click()
                time.sleep(2)
            except Exception as e:
                print(f"Error following user {user}: {e}")
    
    def get_followers(self, user):
        self.driver.get(f"https://x.com/{user}")
        time.sleep(2)
        try:
            number_of_followers = self.driver.find_element(By.XPATH, f"//a[contains(@href, '/{user}/verified_followers')]").text.split()[0]
            print(f"Number of followers: {number_of_followers}")
        except Exception as e:
            print(f"Error retrieving following count: {e}")
            return []
        self.driver.get(f"https://x.com/{user}/followers")
        followers = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            try:
                # Wait until follower elements are visible
                current_followers = [elem.text for elem in WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//span[starts-with(text(), '@')]"))
                )]
                new_followers = [f for f in current_followers if f not in followers]

                if not new_followers:
                    # Scroll down the page to load new followers
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        print("Reached the end of the list or no new followers are loading.")
                        break
                    last_height = new_height
                else:
                    followers.extend(new_followers)
                    print(f"Added {len(new_followers)} new followers.")
            except StaleElementReferenceException:
                print("Encountered a stale element, retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"Error getting followers: {e}")
                break

        return followers
    
   
    def get_following(self, user):
        self.driver.get(f"https://x.com/{user}")
        time.sleep(2)
        try:
            number_of_following = self.driver.find_element(By.XPATH, f"//a[contains(@href, '/{user}/following')]").text.split()[0]
            print(f"Number of following: {number_of_following}")
        except Exception as e:
            print(f"Error retrieving following count: {e}")
            return []

        self.driver.get(f"https://x.com/{user}/following")
        following = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//span[starts-with(text(), '@')]"))
                )
                current_following = [elem.text for elem in self.driver.find_elements(By.XPATH, "//span[starts-with(text(), '@')]")]
                new_following = [f for f in current_following if f not in following]

                if not new_following:
                    # Scroll down to the bottom of the page
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                else:
                    following.extend(new_following)
                    print(f"Added {len(new_following)} new following.")
                    if len(following) >= int(number_of_following.replace(',', '')):
                        break
            except StaleElementReferenceException:
                print("Encountered a stale element, retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"Error during scrolling/loading: {e}")
                break

        return following
                