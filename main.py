from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
from time import sleep
import getpass
from dotenv import load_dotenv
import os
load_dotenv()

NAME = os.getenv('NAME')

ITEMS_PER_LINE_INPUT_TXT = 6

# do initial checks on inputs.txt
f = open("inputs.txt", "r")
inputs = f.read().split("\n")
f.close()

if len(inputs) <= 0:
    print("Error: inputs.txt must have 2 lines")
    exit()

for line in inputs:
    if len(line.split()) != ITEMS_PER_LINE_INPUT_TXT:
        print(f"Error: inputs.txt must have {ITEMS_PER_LINE_INPUT_TXT} lines")
        print("Check README.txt for the exact format of inputs.txt")
        exit()
    
    items = line.split(" ")

    # check dates format
    dates = items[0].split("/")
    if len(dates) != 3:
        print("Error: dates must be in the format YYYY/MM/DD")
        exit()
    if len(dates[0]) != 4:
        print("Error: year must be in the format YYYY")
        exit()
    if len(dates[1]) != 2:
        print("Error: month must be in the format MM")
        exit()
    if len(dates[2]) != 2:
        print("Error: day must be in the format DD")
        exit()
    try:
        dates[0] = int(dates[0])
        dates[1] = int(dates[1])
        dates[2] = int(dates[2])
    except:
        print("Error: dates must be in the format YYYY/MM/DD")
        exit()
    
    # check am/pm
    if items[2].lower().replace(".", "") != "am" and items[2].lower().replace(".", "") != "pm":
        print("Error: start time must be in the format HH:MM AM/PM")
        exit()
    if items[4].lower().replace(".", "") != "am" and items[4].lower().replace(".", "") != "pm":
        print("Error: end time must be in the format HH:MM AM/PM")
        exit()
    
    # check time
    if items[1].count(":") != 1:
        print("Error: start time must be in the format HH:MM AM/PM")
        exit()
    if items[3].count(":") != 1:
        print("Error: end time must be in the format HH:MM AM/PM")
        exit()

for i, line in enumerate(inputs):
    inputs[i] = line.split(" ")

# modify input to generalized format
for i, line in enumerate(inputs):
    inputs[i][2] = inputs[i][2].lower().replace(".", "")
    inputs[i][4] = inputs[i][4].lower().replace(".", "")
NAME = NAME.title()

username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

chrome_options = Options()
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://caltech.instructure.com/")
sleep(1)

# input username and password
driver.find_element(By.ID, 'username').send_keys(username)
sleep(0.2)
password_field = driver.find_element(By.ID, 'password').send_keys(password)
sleep(0.2)
password_field = driver.find_element(By.ID, 'password').send_keys("\n")
sleep(2)

# go to calendar and create event
driver.find_element(By.ID, 'global_nav_calendar_link').click()
sleep(0.5)

def make_appt(month, day, year, start_time, end_time, name, description):
    driver.find_element(By.ID, 'create_new_event_link').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//a[contains(@href,"#edit_appointment_group_form_holder")]').click()
    date_input = driver.find_element(By.NAME, "date")
    date_input.clear()
    date_input.send_keys(f'{year}-{month}-{day}')
    driver.find_element(By.NAME, "start_time").send_keys(start_time)
    sleep(1)
    ActionChains(driver).send_keys('\t').perform()
    ActionChains(driver).send_keys(end_time).perform()
    sleep(1)

    # change appt to correct config
    driver.find_element(By.XPATH, '//*[@id="edit_appointment_form"]/div[2]/div[2]/ul/li[1]/label').click()
    driver.find_element(By.XPATH, '//*[@id="edit_appointment_form"]/div[2]/div[2]/ul/li[3]/label').click()

    # fill out name and description
    driver.find_element(By.NAME, 'title').send_keys(name)
    driver.find_element(By.NAME, 'description').send_keys(description)

    # select calendar
    driver.find_element(By.XPATH, f"//*[text()='Select Calendars']").click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="edit_appointment_form"]/div[1]/div[1]/div/div/ul/li/label').click()
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="edit_appointment_form"]/div[4]/button').click()
    sleep(4)

f = open("past_appts.json", "r")
past_dates = set(list(json.load(f)))
f.close()

for line in inputs:

    date = line[0].split("/")
    year = date[0]
    month = date[1]
    day = date[2]

    start_time = f"{line[1]} {line[2]}"
    end_time = f"{line[3]} {line[4]}"
    description = line[5]

    
    if "/".join(date) in past_dates:
        print(f"Skipping {date}")
        continue
    try:
        make_appt(month, day, year, start_time, end_time, NAME, description)
    except Exception as e:
        print(f"Error on {date}: {e}")
    sleep(1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    sleep(1)
    