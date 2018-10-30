from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

driver = webdriver.Chrome()
driver.get('http://classfinder.belmont.edu/')

driver.implicitly_wait(5)

term = driver.find_element_by_id('tc2')
term.click()

select_subject = driver.find_element_by_name('subject_code')
WebDriverWait(driver, 10).until(
        EC.staleness_of(select_subject.find_elements_by_tag_name('option')[0]))
options = [x for x in select_subject.find_elements_by_tag_name('option')]
courses = []
crns = []

for i in range(1, len(options)):
    subject = options[i]
    subject.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'rowa')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table_body = soup.find(id='resultsSet')

    attrs = ['crn', 'subject', 'section', 'title', 'credit', 'room', 'begin', 'end', 'days', 'max', 'count',
             'instructor', 'fees']

    for row in table_body.find_all('tr'):
        course = {}
        i = 0
        append = True
        for data in row.find_all('td'):
            if 'Results' in data.text:
                append = False
                continue

            item_string = ''

            for item in data.contents:
                if str(item) != '<br/>' and 'span' not in str(item):
                    item_string += str(item) + ' '

            course[attrs[i]] = item_string.rstrip()
            if course[attrs[i]] in crns:
                append = False
                break
            if attrs[i] == 'crn':
                crns.append(course[attrs[i]])
            i += 1
        if append:
            courses.append(course)

writefile = 'spring19.json'

data = {'courses': courses}

with open(writefile, 'w') as outfile:
    json.dump(data, outfile)