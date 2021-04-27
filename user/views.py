import os
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def home(request):
    return render(request, 'user/home.html')

def signupuser(request):
    return render(request, 'user/signupuser.html', {'form':UserCreationForm()})

def login(driver, url, ACCOUNT, PASSWORD, USER_NAME):
    # login
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="id_userLoginId"]').send_keys(ACCOUNT)
    driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(PASSWORD + Keys.ENTER)
    time.sleep(LOAD_PAGE_PAUSE_TIME)

    # select User
    users = driver.find_elements_by_class_name('profile')
    names = []
    for user in users:
        if USER_NAME == user.find_element_by_class_name('profile-name').text:
            user.click()
    time.sleep(LOAD_PAGE_PAUSE_TIME)

def access_mylist():
    #Go to My List
    nav_items = driver.find_elements_by_class_name('navigation-tab')
    for item in nav_items:
        if item.find_element_by_tag_name('a').get_attribute('href') == my_list_url:
            item.click()
    time.sleep(LOAD_PAGE_PAUSE_TIME)

def scroll_to_end_of_page():
    done = False
    while not done:
        last_element = driver.execute_script('return document.querySelector(".galleryLockups").lastElementChild')
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)
        if last_element == driver.execute_script('return document.querySelector(".galleryLockups").lastElementChild'):
            done = True

def get_shows():
    shows = driver.find_elements_by_class_name('slider-refocus')
    shows_list = []
    for show in shows:
        label = show.get_attribute('aria-label')
        link = show.get_attribute('href')
        shows_list.append(
            {
                'label': label,
                'link': link
            }
        )
    return shows_list

def scrap(request):
    
    options = Options()
    options.headless = True
    options.add_argument('--deny-permission-prompts')
    driver = Chrome(options=options)

    login(
        driver,
        url,
        request.user.netflix_login,
        request.user.netflix_password,
        request.user.netflix_username
    )

    access_mylist()
    scroll_to_end_of_page()
    shows = get_shows()