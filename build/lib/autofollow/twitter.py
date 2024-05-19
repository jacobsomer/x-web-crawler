from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def is_ad(tweet):
    try:
        tweet.find_element(By.XPATH, ".//span[text()='Ad']")
        return True
    except Exception:
        return False

def like_tweet(tweet, liked_tweets):
    try:
        tweet_id = tweet.find_element(By.XPATH, ".//a[contains(@href, '/status/')]").get_attribute("href").split("/")[-1]
        if tweet_id and tweet_id not in liked_tweets:
            like_button = tweet.find_element(By.XPATH, ".//div[@data-testid='like']")
            if like_button.is_enabled() and like_button.is_displayed():
                like_button.click()
                liked_tweets.add(tweet_id)
                time.sleep(1)
                return True
        return False
    except Exception as e:
        print(f"Failed to like tweet: {e}")
        return False

def like_tweets_on_feed(driver, run_time=300):
    start_time = time.time()
    while time.time() - start_time < run_time:
        time.sleep(2)
        try:
            tweets = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
            )

            non_ad_tweets = [tweet for tweet in tweets if not is_ad(tweet)]

            for tweet in non_ad_tweets:
                like_tweet(tweet, like_tweet)

        except Exception as e:
            print(f"Error during tweet processing: {e}")

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print(f"Failed to scroll: {e}")
        time.sleep(3)
        

def follow_users(driver, users):
    for user in users:
        driver.get(f"https://x.com/{user}")
        try:
            follow_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Follow')]"))
            )
            follow_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error following user {user}: {e}")
    