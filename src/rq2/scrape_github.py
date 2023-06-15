import logging
from time import sleep

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By

log = logging.getLogger()
log.debug("Starting browser...")
browser = webdriver.Chrome()
log.debug("Visiting page...")
browser.get("https://github.com/apache/skywalking/pull/5666")

# Load full page
while True:
    try:
        load_everything = browser.find_element_by_class_name("ajax-pagination-form")
        button = load_everything.find_element_by_tag_name("button")
        button.click()
        log.debug("Loading more conversations...")
    except selenium.common.exceptions.NoSuchElementException:
        break
    except selenium.common.exceptions.StaleElementReferenceException:
        continue
sleep(2)

# Load review discussions
log.debug("Load outdated review conversations...")
review_discussions = browser.find_elements(By.CLASS_NAME, "js-toggle-outdated-comments")
for d in review_discussions:
    browser.execute("arguments[0].click()", d)


browser.close()
