import os
import time

from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from flixconnect import settings
from .forms import NetflixUserForm
from .models import NetflixUser, Show

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def home(request):
    return render(request, 'user/home.html')

def signupuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('myhome')
    else:
        return render(request, 'user/signupuser.html', {'form':UserCreationForm()})
            
def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            form.clean()
            user = form.get_user()
            login(request, user)
            return redirect('myhome')
    else:
        return render(request, 'user/loginuser.html', {'form':AuthenticationForm()})

@login_required
def myhome(request):
    return render(request, 'user/myhome.html', {'user':request.user})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def netflix_login(request):
    if request.method == 'POST':
        form = NetflixUserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('myhome')
    else:
        form = NetflixUserForm()
        return render(request, 'user/netflixLogin.html', {'form': form})

def scrape(request):
    
    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument('--deny-permission-prompts')
    driver = webdriver.Chrome(options=options)

    net_data = NetflixUser.objects.get(user=request.user)
    
    enter_netflix(
        driver,
        settings.NETFLIX_URL,
        net_data.login,
        net_data.password,
        net_data.profile
    )

    access_mylist(driver)
    scroll_to_end_of_page(driver)
    shows = get_shows(driver)

    for show in shows:
        print(show)

def enter_netflix(driver, url, ACCOUNT, PASSWORD, USER_NAME):
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
    print(nav_items)
    for item in nav_items:
        print(item.find_element_by_tag_name('a').get_attribute('href'))
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
