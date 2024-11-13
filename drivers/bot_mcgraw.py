#!/usr/bin/env python

# Author: Github - nrkorte
#
# Hi there!
# 
# You are welcome to look through my code to see what is going on underneath the hood and improve it if you'd like
# This program is not the most efficient (time-wise or storage-wise) but it gets the job done much faster than a human can
# The main hub that sends requests for completing questions is in mcbegin()
# From there each question type, prompt, and answer is parsed, completed, and stored through individual function calls
#
# Happy hunting!

# Standard Python imports
import sys
import re
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService

# New function to show cursor movement and clicks
def show_cursor_action(action_description):
    print(f"Action: {action_description}")

# Sets the window for the chromedriver to a second screen if you have one
def set_window_position_safely(x, y, driver):
    try:
        driver.set_window_position(x, y)
    except Exception as e:
        print(f"An error occurred while setting window position: {e}")

# Logs you into canvas
def mcstart(user, passw, link, driver):
    time.sleep(3)
    show_cursor_action("Navigating to the link.")
    driver.get(link)
    print("Navigated to the link.")

    # Wait for the page to load completely
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Wait for the username field and input the username
    try:
        show_cursor_action("Waiting for the username field to be present...")
        username_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "userNameInput")))
        username_field.send_keys(user)
        show_cursor_action("Entered username.")
    except TimeoutException:
        print("The username field was not found within the timeout period.")

    # Wait for the password field and input the password
    try:
        show_cursor_action("Waiting for the password field to be present...")
        password_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "passwordInput")))  # Use ID here
        password_field.send_keys(passw)
        show_cursor_action("Entered password.")
    except TimeoutException:
        print("The password field was not found within the timeout period.")

    # Click on the "Sign in" button
    print("Waiting for the Sign in button to be clickable...")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='submitButton']"))).click()
    print("Clicked on the Sign in button.")

    # Wait for a new tab to open
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab

    # Verify that we are on the new tab and print its contents
    print("Current URL:", driver.current_url)

    # New code to click on the "Join" link using the provided XPath
    print("Waiting for the 'Join' link to be present...")
    join_link_xpath = "//*[@id='integration-meeting-list']/div/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/div/div/a"  # Provided XPath
    try:
        # Wait for the "Join" link to be present
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, join_link_xpath)))
        print("Element found. Now waiting for it to be clickable...")
        
        # Now wait for the link to be clickable
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, join_link_xpath))).click()
        print("Clicked on 'Join' link.")

        # Wait for a new tab to open
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)  # Wait for a new tab to open

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the last opened tab

        # Verify that we are on the new tab and print its contents
        print("Current URL after clicking 'Join':", driver.current_url)

        # Attempt to click the cancel button using keyboard action
        try:
            # Simulate pressing the Enter key to click the focused button (Cancel)
            webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
            print("Pressed Enter to click the 'Cancel' button in the popup.")
        except Exception as e:
            print(f"Error while trying to press Enter: {e}")

            # Attempt to click the cancel button using keyboard action
        try:
            # Simulate pressing the Enter key to click the focused button (Cancel)
            webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
            print("Pressed Enter to click the 'Cancel' button in the popup.")
        except Exception as e:
            print(f"Error while trying to press Enter: {e}")

        # Click on the specified button after handling the popup
        button_xpath = "//*[@id='zoom-ui-frame']/div[2]/div/div[2]/h3[2]/span/a"  # Provided XPath for the new button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
        print("Clicked on the specified button.")

        # Verify that we are on the zoom page and print its contents
        print("Current URL after clicking 'Join':", driver.current_url)

        # Attempt to click the cancel button using keyboard action
        try:
            # Simulate pressing the Enter key to click the focused button (Cancel)
            webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
            print("Pressed Enter to click the 'Cancel' button in the popup.")
        except Exception as e:
            print(f"Error while trying to press Enter: {e}")


        # Now wait for the Join link to be clickable
        blu_join_link_xpath = "/html/body/div[2]/div[2]/div/div[2]/h3[2]/span/a"  # Provided XPath
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, blu_join_link_xpath))).click()
        print("Clicked on 'blue Join button' link.")
    except Exception as e:
        print(f"Failed to click blue join button: {e}")

    
    

# Main function that controls the flow
def mcbegin(driver):
    get_into_questions(driver)

    # Removed the dictionary_for_answers and the while loop for questions
    driver.get(driver.current_url)


# Called at the start to choose the begin or resume button
def get_into_questions(driver):
    time.sleep(3)
    try:
        driver.switch_to.window(driver.window_handles[1])
    except:
        print ("You recieved an error because the software attempted to switch to a new window handle without one present. Please restart your program and try again.")
    try:
        WebDriverWait( driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Begin')]"))).click()
    except TimeoutException:
        print(end="1 Failed, ")
    try:
        WebDriverWait( driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Questions')]"))).click()
    except TimeoutException:
        print(end="2 Failed, ")
    try:
        WebDriverWait( driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue Questions')]"))).click()
    except TimeoutException:
        print(end="3 Failed, ")
    try:
        WebDriverWait( driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Start Questions')]"))).click()
    except TimeoutException:
        print(end="4 Failed.")
        
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# Called to ensure that when they try to make you read the book, it is ignored
def get_around_forced_learning(driver, prompt_in_question):
    try:
        WebDriverWait( driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'review a resource')]"))).click()
        WebDriverWait( driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Read About the Concept')]"))).click()
        WebDriverWait( driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'To Questions')]"))).click()
    except TimeoutException:
        print(end="")

# Cleaning up all the extra characters and white space in a prompt
def parse_prompt(prompt_unsplit):
    prompt = prompt_unsplit.split("\n")
    for var in prompt:
        if "Blank" in var or "prompt_array" in var:
            prompt.remove(var)
    ret_str = ""
    for f in prompt:
        ret_str += f
    ret_str = re.sub(r'[\W_]', '', ret_str)
    return ret_str

# Cleaning up answers to only give you the ones you need so you dont try and enter multiple answers
def parse_answer(answer):
    while answer.find("Blank") != -1:
        start = answer.find("Blank")
        inner = 0
        while inner < 9:
            inner += 1
            answer = answer[:start] + answer[start + 1:]
        if answer.find(",") != -1:
            answer = answer[:answer.find(",")]
        if answer.find(" or") != -1:
            answer = answer[:answer.find(" or")]
    return answer

# Cleaning up the extra stuff in multiple choice question answers
def parse_mc_choice_answer(ans):
    return re.sub(r'[\W_]', '', ans)

# Creating the array that is used to store prompts for a matching question
def create_prompt_array_for_matching(driver, number_of_answers):
    count = 0
    add = "/following-sibling::div"
    prompt_array = []
    while count < number_of_answers:
        start = "//div[contains(@class, 'match-row')]"
        inner = 0
        while inner < count:
            start += add
            inner += 1
        count += 1
        prompt_array.append(WebDriverWait (driver, 30).until(EC.presence_of_element_located((By.XPATH, start))).text) # might also just need to run the following sibling thing multiple times with multiple variables getting created

    for i in range(0, len(prompt_array)):
        prompt_array[i] = prompt_array[i].split("\n", 1)[0]

    return prompt_array

# Creating the array that is used to store answers for matching questions
def make_final_array(driver, prompt_array):
    tmp = WebDriverWait (driver, 30).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'correct-list')]"))).text.split("\n")
    answer_array = []
    while len(tmp) > 0:
        tmp.pop(0)
        tmp.pop(0)
        tmp.pop(0)
        answer_array.append(tmp.pop(0))
    final_array = []
    i = 0
    while i < len(prompt_array):
        final_array.append(prompt_array[i])
        final_array.append(answer_array[i])
        i += 1
    return final_array

# Used in ordering questions but not used because the ordering questions do not work
def swap_back (arr, thing, end):
    num = arr.index(thing)
    counter = 0
    while (num > end):
        arr[num] = arr[num - 1]
        arr[num - 1] = thing
        num -= 1
        counter += 1
    return arr, counter

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise Exception("Wrong number of program arguments: found ", len(sys.argv), " needed 3 additional. Exiting now...")
    
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    set_window_position_safely(2000, 0, driver)
    driver.maximize_window()
    
    mcstart(sys.argv[1], sys.argv[2], sys.argv[3], driver)
    mcbegin(driver)

