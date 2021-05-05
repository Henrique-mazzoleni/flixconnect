import os
import time

from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from flixconnect import settings  

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def home(request):
    return render(request, 'user/home.html')

def signupuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('myhome')          
    else:
        return render(request, 'user/signupuser.html', {'form':UserCreationForm()})
            
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'user/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(
                request,
                'user/loginuser.html',
                {
                    'form': AuthenticationForm(), 
                    'error': 'Incorrect Username or Password.'
                }
            )
        else:
            login(request, user)
            return render(request, 'user/myhome.html', {'user':request.user})

def myhome(request):
    return render(request, 'user/myhome.html', {'user':request.user})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def login_net(driver, url, ACCOUNT, PASSWORD, USER_NAME):
    # login
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="id_userLoginId"]').send_keys(ACCOUNT)
    driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(PASSWORD + Keys.ENTER)
    time.sleep(settings.LOAD_PAGE_PAUSE_TIME)

    # select User
    users = driver.find_elements_by_class_name('profile')
    for user in users:
        if USER_NAME == user.find_element_by_class_name('profile-name').text:
            user.click()
    time.sleep(settings.LOAD_PAGE_PAUSE_TIME)

def access_mylist(driver):
    #Go to My List
    nav_items = driver.find_elements_by_class_name('navigation-tab')
    for item in nav_items:
        if item.find_element_by_tag_name('a').get_attribute('href') == settings.MY_LIST_URL:
            item.click()
    time.sleep(settings.LOAD_PAGE_PAUSE_TIME)

def scroll_to_end_of_page(driver):
    done = False
    while not done:
        last_element = driver.execute_script(
            'return document.querySelector(".galleryLockups").lastElementChild'
        )
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(settings.SCROLL_PAUSE_TIME)
        if last_element == driver.execute_script(
            'return document.querySelector(".galleryLockups").lastElementChild'
        ):
            done = True

def get_shows(driver):
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
    
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--deny-permission-prompts')
    driver = webdriver.Chrome(options=options)

    login_net(
        driver,
        settings.NETFLIX_URL,
        request.user.netflix_login,
        request.user.netflix_password,
        request.user.netflix_username
    )

    access_mylist(driver)
    scroll_to_end_of_page(driver)
    shows = get_shows(driver)