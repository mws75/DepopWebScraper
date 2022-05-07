from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import os

''' 
    Set up vitual env here: /Users/michaelspencer/OneDrive/SaniroStore/pythonTools/env
    To activate vitual environment - $ souce env/bin/activate
    You will know because it will show (env) infront of each line in the terminal. 

    #Update 8.23.2020 - Change some of the sleep times in order to make the process 
    faster, but I have not tested yet. 
'''

#Global Variables 
my_binary_location = '//Applications//Google Chrome.app//Contents//MacOS//Google Chrome'
my_executable_path = "//Users//michaelspencer//OneDrive//SaniroStore//pythonTools//env//bin//chromedriver"
depop_url = "https://www.depop.com/login/"
user_url =  "https://www.depop.com/ahnagrace/"  
user_name = "ahnagrace"
login_password = "i<<<3mona"
login_button_id = "login__cta"
login_button_xpath = "//button[@data-testid='login__cta']"

def main():
    #GetSoup()
    #TestHeadlessCrawler()
    driver = SetUpHeadlessDriver()
    driver = LoginIntoDePop(driver, depop_url)
    time.sleep(2)
    driver.get(user_url)
    time.sleep(5)
    # figure out how to press covid button
    try:
        covid_button = driver.find_element_by_class_name("CovidBannerstyles__CloseButton-sc-1mwsgry-3")
        time.sleep(3)
        covid_button.click()   
    except:
        print("no Covid Button")        
    GetPosts(driver)
    driver.close()


def LoginIntoDePop(driver, url):    
    driver.get(url)
    #enter username id = username
    username = driver.find_element_by_id("username") 
    time.sleep(1)   
    username.send_keys(user_name)
    time.sleep(1)
    #enter password id = password
    password = driver.find_element_by_id("password")
    time.sleep(2)
    password.click()
    password.send_keys(login_password)
    #press login button data-testid = login__cta
    login_button = driver.find_element_by_xpath(login_button_xpath)
    login_button.click()
    return(driver)


def GetPosts(driver):
    #scroll to the bottom of the page
    
    for i in range(20):
        time.sleep(0.25)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    soup = BeautifulSoup(driver.page_source, 'html')
    all_posts = soup.find_all("a", {"data-testid": "product__item"})   #{"class": "styles__ProductImage-sc-5cfswk-5 gPcWvA LazyLoadImage__Image-sc-1732jps-1 cSwkPp"})
    
    posts = FilterOutSoldItems(all_posts)

    postNum = 0
    posts.reverse()
    for post in posts:  
        # time.sleep(1.25)
        # print("posts: " + str(postNum))   
        # href = post.get('href')
        # product_page = href.split("/")[-2] #get the product page identifier
        # edit_page = "https://www.depop.com/products/edit/" + product_page + "/"

        # time.sleep(1)      
        # driver.get(edit_page)
        # time.sleep(1.5)
        # try:      
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")          
        #     save_changes_button = driver.find_element_by_xpath("//button[@data-testid='editProductFormButtons__save']")
        #     time.sleep(1)
        #     save_changes_button.click() 
                   
        # except:
        #     print("post has already been sold")
        
        # print(href + " - has been updated at {}".format(datetime.now()))
        print(post)
        postNum = 1 + postNum

            
def SetUpHeadlessDriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless--")
    chrome_options.binary_location = my_binary_location
    
    driver = webdriver.Chrome(executable_path= my_executable_path,
                              chrome_options=chrome_options)    
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



