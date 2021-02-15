# %%
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import subprocess
import fileinput
import sys

timeout = 15

# %%
# - Methods

# replace specific text inside a file
def modify_file_as_text(text_file_path, text_to_search, replacement_text):
    with fileinput.FileInput(text_file_path, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')


# %%
# - Launch chromedriver
cmd_args_present = False

if len(sys.argv) == 4:
    email_recipient = sys.argv[1]
    email_subject = sys.argv[2]
    if os.path.isfile(sys.argv[3]):
        email_body = open(sys.argv[3],'r', encoding="utf-8").read()
        email_body = '<br>'.join(email_body.split('\n'))
    else:
        email_body = sys.argv[3]
    cmd_args_present = True

load_system_profile = True
profile_directory = 'Profile 1'
try:
    driver_location = os.path.abspath(r"{0}/webdriver/chromedriver.exe".format(os.getcwd()))
    # - Disable images for faster scraping
    chrome_options = webdriver.ChromeOptions()
    
    if load_system_profile:
        user_data_folder = os.path.join(os.getenv('LOCALAPPDATA'),r'Google\Chrome\User Data')
    else:
        user_data_folder = os.path.join(os.path.abspath('.'),'Chrome Local Profile')

    chrome_options.add_argument("user-data-dir={0}".format(user_data_folder))
 
    if profile_directory != '':     
        # - select/creates a specific profile inside user data folder
        chrome_options.add_argument(r'--profile-directory={0}'.format(profile_directory))
        
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # hides top bar notification "Chrome is being controlled by automated test software"
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    # avoid this error: https://stackoverflow.com/questions/45099288/what-is-pythons-equivalent-of-useautomationextension-for-selenium
    chrome_options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(executable_path=driver_location ,options=chrome_options)
except Exception as err:
    subprocess.call("TASKKILL /f /IM CHROME.EXE",stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # remove crashed chrome state to avoid restore pages pop up
    modify_file_as_text(os.path.join(user_data_folder,profile_directory,'Preferences'), 'Crashed', 'none')
    print('Sorry, but there was an error in launching the browser.')
    raise SystemError('Webdriver failed to load.\n\n{0}'.format(err))
    #exit(1)
    
browser.implicitly_wait(timeout)
#print("driver OK")

# %%
try:

    if not cmd_args_present:
        email_recipient = input('Who would you like to send an email to?\n')
        email_subject = input('What is the subject of the email?\n')
        email_body = input('What would you like to say?\n')

    #browser.maximize_window()
    browser.implicitly_wait(timeout)
    browser.get('http://mail.google.com')

    main_window_hdw = browser.window_handles[0]

    try:
        WebDriverWait(browser, timeout=timeout).until(
            EC.presence_of_element_located((By.XPATH, r"//div[@role='button' and @class='T-I T-I-KE L3']"))
        )
    except Exception as err:
        raise SystemError('Gmail not loaded correctly\n\n{0}'.format(err))

    html_elem = browser.find_element_by_tag_name('html')
    html_elem.send_keys('d')

    time.sleep(2.5)

    # open last opened tab
    browser.switch_to.window(browser.window_handles[-1])

    browser.execute_script("document.querySelector('.vO').value = arguments[0]",email_recipient)
    browser.execute_script("document.querySelector('.aoT').value = arguments[0]", email_subject)
    browser.execute_script("document.querySelector('.Am.Al.editable.LW-avf.tS-tW').innerHTML = arguments[0]", email_body)
    browser.execute_script("document.querySelector(\"[role='button'][tabIndex='1'][aria-label*='Ctrl-Enter']\").click()")

    try:
        WebDriverWait(browser, timeout=timeout).until(
            EC.presence_of_element_located((By.XPATH, r"//*[ contains(text(),'Mensagem enviada') or contains(text(),'Message sent')]"))        
        )
    except Exception as err:
        raise SystemError('Error sending messsage\n\n{0}'.format(err))

    browser.switch_to.window(main_window_hdw) 

    try:
        WebDriverWait(browser, timeout=timeout).until(
            EC.presence_of_element_located((By.XPATH, r"//div[@role='button' and @class='T-I T-I-KE L3']"))
        )
    except Exception as err:
        raise SystemError('Gmail not loaded correctly\n\n{0}'.format(err))

    print('Email was sent.')
except Exception as err:
    print('There was an error running the program. Probably you are not logged in Gmail.\nLog in your normal chrome browser, close it and run again this program.')
finally:
    browser.quit()
