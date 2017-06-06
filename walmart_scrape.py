 #!/user/bin/python

"""
	Chelsea Crain 
	10/29/2016
	
	Attempts to save pages of soda price
		information from Instacart.com
 """
 

from __future__ import print_function, division
from lxml import html
import csv
from itertools import izip_longest
import itertools
from os.path import join, dirname, realpath
from pandas import Series, DataFrame
import pandas as pd
from os import path
from datetime import date
import fileinput
import os
import numpy
import time 
from shutil import copyfile
from selenium import webdriver
import time, os, re, codecs, math, random, csv, datetime
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import smtplib
import sys

# path = "H:\Soda_Tax_Scrapes\Scrape20_03.15.17"

# wal = os.path.join(path, "Walmart")

area = "walmart"

delay = 30

# list_of_zips = "zip_list_" + area + ".csv"
# list_of_zips = os.path.join(path, "zip_list_" + area + ".csv")
# list_of_categories = os.path.join(path, "list_categories_instacart.csv")
# done_zips_name = os.path.join(wal, "done_zips_" + area + ".csv")
# done_list_name = os.path.join(wal, "done_list_" + area + ".csv")



	
def get_done_lists(done_list_name, done_zips_name):

	try:
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
		#print(done_list)
		
	except:
		file = open(done_list_name, 'w')
		file.write("done" +  "\n")
		file.close()
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
		
	try:
		df = pd.read_csv(done_zips_name)
		done_zips = df['done'].tolist()
	except:
		file = open(done_zips_name, 'w')
		file.write("done" + "," + "service_notes" + "\n")
		file.close()
		df = pd.read_csv(done_zips_name)
		done_zips = df['done'].tolist()
		
	return done_list, done_zips
	
def count_letters(zip):

	letters = len(zip) - zip.count(' ')
	
	if letters < 5:
		zip = "0" + str(zip)
	else:	
		zip = str(zip)
		
	print(zip)
	
	return zip

def get_to_search_page():

	url = "http://grocery.walmart.com/usd-estore/m/home/anonymouslanding.jsp"
	
	driver = webdriver.Chrome('C:\Program Files (x86)'
				'\Google\Chrome\Application\chromedriver.exe')
	driver.get(url)
	
	WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.CLASS_NAME, "js-content")
				))
	
	return driver
	
def change_zip(zip, driver):

	WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.ID, 'postalCode')
			))
			
	zip_search = driver.find_element_by_id('postalCode')
	zip_search.send_keys(zip)
	
	try:
		enter = driver.find_element_by_xpath('.//button[contains(text(), "Check Availability")]')
		enter.click()
	except:
		time.sleep(3)
		enter = driver.find_element_by_xpath('.//button[contains(text(), "Check Availability")]')
		enter.click()
	
	try:
		WebDriverWait(driver, 10).until(
					EC.presence_of_element_located(
					(By.XPATH, './/*[contains(text(), "Start Shopping")]')
					))
		driver.find_element_by_xpath('.//*[contains(text(), "Start Shopping")]').click()
		print("clicked out")
	except:
		print("good to go")
		
	try:	
		WebDriverWait(driver, 10).until(
					EC.presence_of_element_located(
					(By.CLASS_NAME, 'emailentry')
					))
		no_service = driver.find_element_by_xpath('//input[@value="Join Waitlist"]')
		return True
		
	except:	
		
				
		return False


				
def search_for_cat(category, driver):
	
	search_box = driver.find_element_by_xpath('.//*[@placeholder="Search"]')
		
	## delete last entry
	for x in range(0,30):
		search_box.send_keys(Keys.BACKSPACE)
	
	## enter new one
	search_box.send_keys(category)
	search_box.send_keys(Keys.ENTER)
	

	WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, "js-content")
			))
	
def prep_file(zip, category, id, wal):

	zip_path = os.path.join(wal, zip)
	if not os.path.exists(zip_path):
		os.makedirs(zip_path)
					
	file = open(os.path.join(zip_path, id + ".txt"), "w")
	
	return file
					
def get_data(file, driver, category):

	
	WebDriverWait(driver, delay).until(
		EC.presence_of_element_located(
		(By.XPATH, './/div[@data-automation-id="productTile"]')
		))
		
	## get and save all text			
	text = driver.find_element_by_xpath('html[@class]').text
	text = text.encode('utf-8').strip()
	
	loading = "Loading ..."
	results = "Search results for: " + category
	wrong = False
	loaded = False
	i = 0
	while loaded == False:
		text = driver.find_element_by_xpath('html[@class]').text
		text = text.encode('utf-8').strip()
		
		if (loading in text) | (results not in text):
			print("still loading")
			time.sleep(2)
					
		elif (loading not in text) & (results in text):
			loaded = True
		
		if i >10:
			wrong = True
			break
	
		i+=1
	file.write(text)
	print("got page 1")
	
	if "Next" in text:
		more = True
	else:
		more = False
	
	i = 2
	
	while more == True:
		## arrow through all pages
		try:
			next = driver.find_element_by_xpath('.//a[contains(text(), "Next")]')
			next.click()
		except:

			time.sleep(2)

			WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.XPATH, './/div[@data-automation-id="productTile"]')
				))
				
			next = driver.find_element_by_xpath('.//span[contains(text(), "Next")]/parent::*')
			next.click()

		
		time.sleep(1.5)
		WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.XPATH, './/div[@data-automation-id="productTile"]')
				))
		text = driver.find_element_by_xpath('html[@class]').text
		
		text = text.encode('utf-8').strip()
		
		loading = "Loading ..."
		results = "Search results for: " + category
		
		loaded = False
		j = 0
		while loaded == False:
			text = driver.find_element_by_xpath('html[@class]').text
			text = text.encode('utf-8').strip()
			
			if (loading in text) | (results not in text):
				print("still loading")
				time.sleep(2)
						
			elif (loading not in text) & (results in text):
				loaded = True
				
			if j >10:
				try:
					driver.execute_script("window.history.go(-1)")
					WebDriverWait(driver, delay).until(
						EC.presence_of_element_located(
						(By.CLASS_NAME, "item__media")
						))
				except:
					wrong = True
					break
		
			j+=1

		file.write(text)
		print("got page %s" %i)

		if "Next" in text:
			more = True
		else:
			more = False
			
		i+=1

			
	file.close()	
			
	print("price info saved to text file")		

	return wrong
					
def main(scrape_name):

	general_path = "H:\Soda_Tax_Scrapes" 
	path = general_path + "\\Scrape_" + scrape_name

	wal = os.path.join(path, "Walmart")
	if not os.path.isdir(wal):
		os.makedirs(wal)

	list_of_zips = general_path + "\\zip_list_walmart.csv"
	list_of_categories = general_path + "\\list_categories.csv"
	done_zips_name = wal + "\\done_zips_walmart.csv"
	done_list_name = wal +  "\\done_list_walmart.csv"

	try:
		df = pd.read_csv(list_of_zips)
		zips = df['zip'].tolist()
		
		df = pd.read_csv(list_of_categories)
		categories = df['category'].tolist()
		print(categories)
		
		done_list, done_zips = get_done_lists(done_list_name, done_zips_name)
		
		print("Number zips done: %s" %len(done_zips))
		
				
		for zip in zips: ## loop through all zips
					
			if zip in done_zips:
				print("already done with this zip:%s" %zip)
				continue
						
			driver = get_to_search_page()
			
			zip = count_letters(str(zip))
			
			## set zipcode 
			print("changing zip")
			no_service = change_zip(zip, driver)
			
			if no_service == True: ## check to make sure it's available
				done_zips_file = open(done_zips_name, 'a')
				done_zips_file.write(zip + "," + "no service" + "\n")
				done_zips_file.close()
				print("no service here")
				driver.close()
				continue 
			
			else:
			
				for category in categories: ## loop through all categories
			
					print("searching for category %s" %category)
					
					id = zip + "_" + category
					
					print(id)
					
					if id in done_list:
						print("already got this category: %s" %id)
						continue
					
					time.sleep(2)
					
					try: 
						driver.find_element_by_xpath('.//h2[contains(text(), "Join the waitlist")]')
						print("no service here")
						continue
					except:
						x=0
					
					## search for category
					
					search_for_cat(category, driver)			
					
					file = prep_file(zip, category, id, wal)
					
					wrong = get_data(file, driver, category)
					
					
					done_file = open(done_list_name, 'a')
					if wrong == False:
						done_file.write(id + "\n")
					elif wrong == True:
						done_file.write(id + "," + "something went wrong" + "," + "\n")
					done_file.close()
			
			done_zips_file = open(done_zips_name, 'a')
			done_zips_file.write(zip + "\n")
			done_zips_file.close()
			
			print("done with zip %s, opening new browser" %zip)
			driver.close()
		
		
		print("Woot woot! All done!")
	
	except:
		sys.exit()
	






if __name__ == '__main__':
    main(sys.argv[1])