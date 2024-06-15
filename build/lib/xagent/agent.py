from selenium import webdriver
from .x import X

class XAgent:
    def __init__(self, driver_path, profile_path, x_username=None, x_password=None, browser="chrome"):
        self.driver_path = driver_path
        self.profile_path = profile_path
        self.browser = browser
        self.driver = self.create_driver()
        self.x_agent = X(self.driver)
        self.x_username = x_username
        self.x_password = x_password
        self.login_to_x()
        
    def set_common_options(self, options):
        if self.profile_path:
            options.add_argument(f"user-data-dir={self.profile_path}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--remote-debugging-port=9222")
        
        options.add_argument("--disable-dev-shm-using") 
        options.add_argument("--disable-extensions") 
        options.add_argument("--disable-gpu") 
        options.add_argument("start-maximized") 
        options.add_argument("disable-infobars")
        options.add_argument(f"window-size={1920//2},1080")
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        })
        return options

    def create_driver(self):
        if self.browser == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options = self.set_common_options(chrome_options)
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        elif self.browser == "edge":
            edge_options = webdriver.EdgeOptions()
            edge_options = self.set_common_options(edge_options)
            edge_service = webdriver.EdgeService(executable_path=self.driver_path) 
            driver = webdriver.Edge(service=edge_service, options=edge_options)
            return driver
        
    """
    The like_x_posts method will like x posts on the user's feed for a specified amount of time.
    """
    def like_x_posts(self, duration=300):
        self.x_agent.like_x_posts_on_feed(duration)
        
    """
    Gets the followers of a user.
    """
    def get_x_followers(self, username):
        ret = self.x_agent.get_followers(username)
        return ret
    
    """
    Gets the following of a user.
    """
    def get_x_following(self, username):
        ret = self.x_agent.get_following(username)
        return ret
    
    """
    Given a list of users, unfollows them.
    """
    def unfollow_x_users(self, users):
        self.x_agent.unfollow_users(users)
        
    """
    Given a list of users and the current user, unfollows them. Uses an alternative method.
    """
    def unfollow_x_users_alternative(self, user, users):
        self.x_agent.unfollow_users_alternative(user, users)
        
    """
    Given a list of users, follows them.
    """    
    def follow_x_users(self, users, duration=300):
        self.x_agent.follow_users(users, duration)
        
    """
    Given a query, gets the handles of the users.
    """    
    def get_x_handles(self, query, num_handles=10):
        ret = self.x_agent.get_handles(query, num_handles)
        return ret
    
    def login_to_x(self):
        self.x_agent.login(self.x_username, self.x_password)
    
    def close(self):
        self.driver.quit()
