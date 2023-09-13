import time
import getpass
import random
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from twilio.rest import Client

account_sid = 'test'
auth_token = 'test'
client = Client(account_sid, auth_token)


def send_message(course):
    for numb in ['+test']:
        message = client.messages.create(
            to=numb,
            from_='+test',
            body=f"{course} secured! Go to VM to confirm",
        )
        print(message.sid)


email = 'jameswoyevodsky@gmail.com'
# email = input('What is the account email? > ').strip()
# password = getpass.getpass(
#     'What is the password? (This is not stored anywhere) > ').strip()
password = 'test'
earliest = int(
    input('What is the earliest hour you want to go? (whole numbers only)>> ').
    strip())
latest = int(input("...and the latest hour? (whole numbers only) >> ").strip())

am_or_pm = input('am or pm? >> ').lower().strip()

course = input('What course? >> ').lower().strip()

newest_date = input(
    'Do you want to scan the newest date? (Y/N) >> ').lower().strip()

courses = {
    'blue': 'Bethpage Blue Course',
    'red': 'Bethpage Red Course',
    'black': 'Bethpage Black Course',
    'green': 'Bethpage Green Course',
    'yellow': 'Bethpage Yellow Course',
    'mid 9': 'Bethpage 9 Holes Midday Blue or Yellow Course',
    'early 9': 'Bethpage Early AM 9 Holes Blue'
}

# initialize browser
chromedriver = '/Users/jameswoyevodsky/Downloads/chromedriver_mac64\ \(1\)/chromedriver'
options = Options()
# options.add_argument('headless')
# options.add_argument('window-size=800x850')
browser = webdriver.Chrome(options=options)
# browser.minimize_window()
browser.set_window_size(800, 850)

# navigate to website
browser.get('https://parks.ny.gov/golf/')
time.sleep(5)
link = 'https://foreupsoftware.com/index.php/booking/19765/2431#welcome'
browser.find_element(By.CSS_SELECTOR, f"a[href = '{link}']").click()
time.sleep(3)

# login to account
button_id = 'btn btn-lg btn-primary login'
browser.find_element(By.CSS_SELECTOR, f"button[class = '{button_id}']").click()
time.sleep(2)
browser.find_element(
    By.CSS_SELECTOR, f"input[name = 'email']").send_keys(email)
print('Email entered.')
time.sleep(1)
browser.find_element(By.CSS_SELECTOR, f"input[name = 'password']").send_keys(
    password)
print('Password entered.')
time.sleep(1)
browser.find_element(By.CSS_SELECTOR,
                     "button[data-loading-text = 'Logging In...']").click()
time.sleep(2)
print('Successfully logged in!')

# navigate to NY resident reservation page
tee_time_url = browser.current_url[:len(browser.current_url) - 7] + 'teetimes'
browser.get(tee_time_url)
time.sleep(.5)
browser.find_elements(By.CSS_SELECTOR, "button")[1].click()

# select course on reservation page
WebDriverWait(browser, 100).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "select[id = 'schedule_select']")))
select_course = Select(
    browser.find_element(By.CSS_SELECTOR, "select[id = 'schedule_select']"))
select_course.select_by_visible_text(courses[course])

# select morning, mid, or evening
time.sleep(1)
if am_or_pm == 'am':
    browser.find_element(By.CSS_SELECTOR, "a[data-value = 'morning']").click()
time.sleep(1)

# select date
dates = browser.find_element(
    By.ID, 'date-menu').find_elements(By.TAG_NAME, 'option')
time.sleep(.2)
print('Reached tee-time page')
if newest_date == 'y':
    dates[len(dates) - 1].click()
    date_selection = dates[len(dates) - 1].text
else:
    for i in range(0, len(dates)):
        print(f"{i}) {dates[i].text}")
    date_choice = int(input('What date do you want (enter #) >> ').strip())
    date_selection = dates[date_choice].text
    dates[date_choice].click()

monitor_delay = float(
    input("Enter monitor delay (.5 recommended if you have fast internet): "))
print(
    f"'{courses[course]}' on {date_selection} selected. Waiting for times to open."
)

time.sleep(2)
print('Searching for times...')
# refresh page by clicking on the "4 people" button until times become available
i = 0
while i == 0:
    if 'will be held' in browser.page_source:
        print(
            f"Success! {courses[course]} has been secured!"
        )
        i = 1
        break
    browser.find_element(By.CSS_SELECTOR, f"a[data-value = '3']").click()
    print('Refreshing...')
    time.sleep(monitor_delay)
    try:
        times = browser.find_elements(
            By.CSS_SELECTOR, "div[class = 'booking-start-time-label']")
        # randomize the order of tee times
        random.shuffle(times)
        for ti in range(0, len(times)):
            t = times[ti]
            print('Comparing time against criteria...')
            check = int(t.text.split(':')[0]) >= earliest and int(
                t.text.split(':')[0]) <= latest and t.text.split(
                    ':')[1][2:] == am_or_pm
            print(check)
            if check:
                print(t)
                t.click()
                lock = input('we locking this bitch down ya feel me >> ').lower().strip()
                print('Time Selected!')
                try:
                    time.sleep(.1)
                    if 'will be held' in browser.page_source:
                        print('secured')
                    # browser.find_element(By.CSS_SELECTOR,
                    #     "button[data-loading-text = 'Booking time...']").click(
                    #     )
                        i = 1
                    try:
                        browser.maximize_window()
                    except:
                        pass
                    time_success = t.text
                    print(
                        f"Success! {time_success} at {courses[course]} has been secured!"
                    )
                    break
                except:
                    print('Does not meet criteria.')
                    pass
            else:
                print('Time does not meet criteria.')
                pass
    except:
        print('Time unavaiable.')
        pass
send_message(courses[course])
input()
# email = 'testtesttest@test.com'
# password = 'testtest123'