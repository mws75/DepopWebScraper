from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import os
from random import uniform
from EmailHelper import EmailHelper
import random
from MouseMover import MouseMover

''' 
    DEBUG TIPS - If it stops working things to check are 
        1. is chromedriver up-to-date?
        2. are the list of user_agents up-to-date?

    Set up vitual env here: /Users/michaelspencer/OneDrive/SaniroStore/pythonTools/env
    To activate vitual environment - $ souce env/bin/activate
    You will know because it will show (env) infront of each line in the terminal. 

    #Update 8.23.2020 - Change some of the sleep times in order to make the process 
    faster, but I have not tested yet. 

    #Update 6.11.2021 - Set sleep time to sleep for 15-18 min every 102 posts, also added 
    an email helper to send me emails when depop has started. 
'''

#Global Variables 
my_binary_location = '//Applications//Google Chrome.app//Contents//MacOS//Google Chrome'
my_executable_path = "//Users//michaelspencer//OneDrive//SaniroStore//pythonTools//env//bin//chromedriver"
#my_executable_path = "env//bin//chromedriver.exe"
depop_url = "https://www.depop.com/login/"    
user_name = "ahnagrace"
depop_user_url = "https://www.depop.com/"+ user_name + "/"
login_password = "password"
login_button_id = "login__cta"
login_button_xpath = "//button[@data-testid='login__cta']"

def main():
    print("we shall begin the process of updating... Updating sleep time...")
    # TODO - Sleep 1 to 15 mintues before beginning so that the job does not start at an exact time. 
    #GetSoup()
    driver = SetUpHeadlessDriver()
    driver = LoginIntoDePop(driver, depop_url)
    time.sleep(2.42)
    driver.get(depop_user_url)
    time.sleep(5.3)
    # figure out how to press covid button
    try:
        covid_button = driver.find_element_by_class_name("CovidBannerstyles__CloseButton-sc-1mwsgry-3")
        time.sleep(3.23)
        covid_button.click()   
    except:
        print("no Covid Button")        
    numberOfRefreshes = RefreshListings(driver)
    subject = f"Depop Refresh for {user_name}"
    message = ""
    if numberOfRefreshes == 0:
        message = "Depop was not fully refreshed"
    else: 
        message = f"Depop was correctly refreshed.  {str(numberOfRefreshes)} posts were refreshed."
    driver.close()
    emailHelper = EmailHelper(subject, message, "mwspencer75@gmail.com")
    emailHelper.send_message()


def LoginIntoDePop(driver, url):        
    driver.get(url)

    mouse_mover = MouseMover(driver)
    mouse_mover.move_mouse_bezier_curve()

    # enter username id = username
    username = driver.find_element_by_id("username")
    
    # sleep after a random number of posts - like a person taking a break. 
    for letter in user_name:
        username.send_keys(letter)
        sleep_time = uniform(0, 0.1)
        time.sleep(sleep_time)
    
    time.sleep(1.28)
    
    #enter password id = password
    password = driver.find_element_by_id("password")
    
    time.sleep(2.23)
    password.click()
    for letter in login_password:
        password.send_keys(letter)
        sleep_time = uniform(0, 0.1)
        time.sleep(sleep_time)
    
    time.sleep(1.45)

    #press login button data-testid = login__cta
    login_button = driver.find_element_by_xpath(login_button_xpath)
    webdriver.ActionChains(driver).move_to_element(login_button).perform
    #login_button = driver.find_element_by_xpath(login_button_xpath)
    login_button.click()
    return(driver)


def DriveToUrl(url = "https://www.depop.com//littlebrickhouse"):
    driver = SetUpHeadlessDriver()
    driver.get(url)    
    return(driver)

def RefreshListings(driver):
    #scroll to the bottom of the page
    emailHelper = EmailHelper("Depop Crawler Started", "Depop Automator has started", "mwspencer75@gmail.com")
    emailHelper.send_message()
    try:
        for i in range(30):
            time.sleep(.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        soup = BeautifulSoup(driver.page_source, 'html')
        all_posts = soup.find_all("a", {"data-testid": "product__item"})   #{"class": "styles__ProductImage-sc-5cfswk-5 gPcWvA LazyLoadImage__Image-sc-1732jps-1 cSwkPp"})
        
        posts = FilterOutSoldItems(all_posts)        
        posts.reverse()

        postNum = 1
        random_interval = int(uniform(50, 100))
        for post in posts: 
            
            #
            if postNum % random_interval == 0:
                time.sleep(uniform(1200, 1400))
                random_interval = int(uniform(50, 100))

            time.sleep(uniform(1.5, 2.5))
            print("posts: " + str(postNum))   
            href = post.get('href')
            product_page = href.split("/")[-2] #get the product page identifier
            edit_page = "https://www.depop.com/products/edit/" + product_page + "/"

            time.sleep(uniform(1.25, 2.02))      
            driver.get(edit_page)
            time.sleep(uniform(1.75, 2.05))
            try:      
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(uniform(0.001, 0.9))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(uniform(0.001, 0.9))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.001, 0.9)          
                save_changes_button = driver.find_element_by_xpath("//button[@data-testid='editProductFormButtons__save']")
                time.sleep(uniform(1.24, 2.45))                       
                save_changes_button.click()
                time.sleep(uniform(1.01, 2.11))                   
            except:
                print("post has already been sold")
            
            print(href + " - has been updated at {}".format(datetime.now()))
            postNum = 1 + postNum
        return postNum
    except:
        return 0

            
def SetUpHeadlessDriver():
    user_agent_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                ]  
    user_agent = random.choice(user_agent_list)

    chrome_options = Options()
    chrome_options.add_argument("--headless--")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("window-size=1280,800")
    chrome_options.add_argument(user_agent)
    chrome_options.binary_location = my_binary_location
    
    #absolute_path = str(os.path.abspath(my_executable_path)).replace("/", "//")
    driver = webdriver.Chrome(executable_path= my_executable_path,
                              options=chrome_options)    
    return(driver)


def FilterOutSoldItems(all_posts):
    posts = []
    for post in all_posts:
        itemsold = post.find_all("div", {"data-testid": "product__sold"}) 
        if len(itemsold) > 0:
            continue
        else:
            posts.append(post)
    return posts


main()    




