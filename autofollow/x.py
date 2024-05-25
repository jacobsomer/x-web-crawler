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
    
    def unfollow_users(self, users):
        for user in users:
            user = user.replace("https://x.com/", "")
            user = user.replace("https://twitter.com/", "")
            self.driver.get(f"https://x.com/{user}")
            try:
                unfollow_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Following')]"))
                )
                unfollow_button.click()
                time.sleep(2)
                confirm_unfollow_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@style,'border-color: rgba(0, 0, 0, 0)')]"))
                )
                confirm_unfollow_button.click()
                time.sleep(2)
            except Exception as e:
                print(f"Error unfollowing user {user}: {e}")
                
    def unfollow_users_alternative(self, user, users):
        self.driver.get(f"https://x.com/{user}/following")
        unfollowed = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@data-testid, 'UserCell')]"))
                )
                current_following = {}
                for elem in self.driver.find_elements(By.XPATH, "//button[contains(@data-testid, 'UserCell')]"):
                    try:
                        username = elem.find_element(By.XPATH, ".//span[starts-with(text(), '@')]").text
                        unfollow_button = elem.find_element(By.XPATH, f".//button[contains(@aria-label, 'Following {username}')]")
                        current_following[username] = unfollow_button
                    except Exception as e:
                        print(f"Error getting following: {e}")
                users_to_unfollow = {f: current_following[f] for f in current_following if f in users}
                if not users_to_unfollow:
                    # Scroll down to the bottom of the page
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                else:
                    for key in users_to_unfollow:
                        users_to_unfollow[key].click()
                        time.sleep(2)
                        unfollowed.append(key)
            except StaleElementReferenceException:
                print("Encountered a stale element, retrying...")
                time.sleep(1)
                    
            
    
    def get_followers(self, user):
        time.sleep(2)
        self.driver.get(f"https://x.com/{user}")
        time.sleep(2)
        try:
            number_of_followers = self.driver.find_element(By.XPATH, f"//a[contains(@href, '/{user}/verified_followers')]").text.split()[0]
            print(f"Number of followers: {number_of_followers}")
        except Exception as e:
            print(f"Error retrieving follower count: {e}")
            return {}

        self.driver.get(f"https://x.com/{user}/followers")
        followers = {}
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@data-testid, 'UserCell')]"))
                )

                current_followers = {}
                for elem in self.driver.find_elements(By.XPATH, "//button[contains(@data-testid, 'UserCell')]"):
                    try:
                        username = elem.find_element(By.XPATH, ".//span[starts-with(text(), '@')]").text
                        all_text = elem.text
                        current_followers[username] = all_text
                    except Exception as e:
                        print(f"Error getting follower: {e}")

                new_followers = {f: current_followers[f] for f in current_followers if f not in followers}
                if not new_followers:
                    # Scroll down to the bottom of the page
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                else:
                    for key in new_followers:
                        followers[key] = new_followers[key]
                    if len(followers) >= int(number_of_followers.replace(',', '')):
                        break
            except StaleElementReferenceException:
                print("Encountered a stale element, retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"Error during scrolling/loading: {e}")
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
            return {}

        self.driver.get(f"https://x.com/{user}/following")
        following = {}
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@data-testid, 'UserCell')]"))
                )
                
                current_following = {}
                for elem in self.driver.find_elements(By.XPATH, "//button[contains(@data-testid, 'UserCell')]"):
                    try:
                        username = elem.find_element(By.XPATH, ".//span[starts-with(text(), '@')]").text
                        all_text = elem.text
                        current_following[username] = all_text
                    except Exception as e:
                        print(f"Error getting following: {e}")
                new_following = {f: current_following[f] for f in current_following if f not in following}
                if not new_following:
                    # Scroll down to the bottom of the page
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                else:
                    for key in new_following:
                        following[key] = new_following[key]
                    if len(following) >= int(number_of_following.replace(',', '')):
                        break
            except StaleElementReferenceException:
                print("Encountered a stale element, retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"Error during scrolling/loading: {e}")
                break

        return following
    
#   create a method that gets all the handles for a specific search query
#ex. https://x.com/search?q="@PKU1898"&f=user
    def get_handles(self, query, num_handles=10):
        self.driver.get(f'https://x.com/search?q={query}&f=user')
        time.sleep(2)
        handles = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while len(handles) < num_handles:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//span[starts-with(text(), '@')]"))
                )
                current_handles = [elem.text for elem in self.driver.find_elements(By.XPATH, "//span[starts-with(text(), '@')]")]
                new_handles = [f for f in current_handles if f not in handles]

                if not new_handles:
                    # Scroll down to the bottom of the page
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                else:
                    handles.extend(new_handles)
                    print(f"Added {len(new_handles)} new handles.")
            except StaleElementReferenceException:
                print("Encountered a stale element, retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"Error during scrolling/loading: {e}")
                break

        return handles[:num_handles]