 #!/user/bin/python

"""
	Chelsea Crain 
	10/29/2016
	
	Attempts to save pages of soda price
		information from Instacart.com
 """
 

from __future__ import print_function, division
from lxml import html
import csv, sys
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
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import sys


delay = 15



def get_done_lists(done_list_name, done_zips_name):

	try:
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
		#print(done_list)
	except:
		file = open(done_list_name, 'w')
		file.write("done" + "," + "\n")
		file.close()
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
		
	try:
		df = pd.read_csv(done_zips_name)
		done_zips = df['done'].tolist()
	except:
		file = open(done_zips_name, 'w')
		file.write("done" + "," +  "service_notes" + "\n")
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

def get_to_search_page(email_address, password_text):

	url = "https://www.instacart.com/"
	
	opts = Options()
	opts.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
	
	driver = webdriver.Chrome('C:\Program Files (x86)'
				'\Google\Chrome\Application\chromedriver.exe', chrome_options=opts)
	
	driver.get(url)
	
	time.sleep(5)
	
	try:
		## login
		login = driver.find_element_by_partial_link_text('Log in').click()
		
		time.sleep(5)
		
		email = driver.find_element_by_name('email')
		email.send_keys(email_address)
		
		password = driver.find_element_by_name('password')
		password.send_keys(password_text)
		
		submit = driver.find_element_by_xpath("//button[@type='submit']").click()
		
		try:
			WebDriverWait(driver, delay).until(
					EC.presence_of_element_located(
					(By.CLASS_NAME, "primary-nav-link")
					))
			driver.find_element_by_xpath('//*[@class="icModalContent addressPickerModal"]')
			driver.find_element_by_xpath('//*[@class="ic-icon ic-icon-x-bold icModalClose"]').click()
			print("clicked out of choose address")
		except:
			x=0
		try:
			WebDriverWait(driver, delay).until(
					EC.presence_of_element_located(
					(By.CLASS_NAME, "primary-nav-link")
					))
		except:
			deactivated = driver.find_element_by_xpath('//fieldset[@class="email error"]')
			print("deactivated")
			send_email('deactivated', 'na')
	except:
		print("already logged in")
	
	# time.sleep(10)
	
	return driver

def send_email(issue, area):

	TO = 'chelsea-crain@uiowa.edu'
	FROM = 'chelsea.crain@gmail.com'
	
	if issue == 'deactivated':
		TEXT = 'INSTACART ACCOUNT HAS BEEN DEACTIVATED'
	if issue == 'done':
		TEXT = 'DONE WITH INSTACART AREA'
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login('chelsea.crain@gmail.com', '1207Dgl#$')
	
	send_it = server.sendmail(TO, FROM, TEXT)

def change_zip(zip, driver):
	try:
		exit = driver.find_element_by_xpath('//*[@class="ic-icon ic-icon-x-bold icModalClose"]').click()

	except:
		x=0
			
	try:
		try:
			a = driver.find_element_by_xpath('//button[@class="pickup-only-modal-'
			 'location-item ic-btn ic-btn-secondary"]')
			
			a.click()
		except:
			time.sleep(1)
			a = driver.find_element_by_xpath('//button[@class="pickup-only-modal-'
				'location-item ic-btn ic-btn-white-selected"]')
			
			a.click()
		
		submit = driver.find_element_by_xpath('//button[@class="ic-btn'
						' ic-btn-success"]')
		submit.click()
		print("clicked out of pickup")
		
	except:
		print("good to go")
		
	try:	
		change_zip = driver.find_element_by_xpath('//a[@aria-label='
									 '"change zipcode"]')
		change_zip.click()
		pick_up = False

	except:	
		try:
			driver.find_element_by_xpath('.//a[@class="Topbar-logo"]').click()
			time.sleep(1)
			change_zip = driver.find_element_by_xpath('.//a[@aria-label="change zipcode"]')
			change_zip.click()
			pick_up = False
			
		except:
			try:
				change_zip = driver.find_element_by_xpath('//i[@class="ic-icon ic-icon-location-marker"]')
				change_zip.click()
				pick_up = False
		
			except:
				try: 
					time.sleep(2)
					store = driver.find_elements_by_xpath('.//h3[contains(@class, "ic-text-truncate")]')[7]
					store.click() 
					pick_up = False
					print("clicked on store to go back")
					time.sleep(4)
					try:
						gotit = driver.find_element_by_xpath('.//*[contains(@classs, "ic-btn ic-btn-lg ic-btn-secondary")]').click()
					except:
						x=0
					time.sleep(2)
					change_zip = driver.find_element_by_xpath('//i[@class="ic-icon ic-icon-location-marker"]')
					change_zip.click()
				except:
					try:
						choose_store = driver.find_element_by_xpath('.//img[@alt="Instacart Demo"]')	
						choose_store.click()
						change_zip = driver.find_element_by_xpath('.//button[@type="submit"]')
						change_zip.click()
						pick_up = False
					except:
						pick_up = True
						print("pickup")
					
	if pick_up == False:
		enter_zip = driver.find_element_by_xpath('//input[@pattern="[0-9]*"]')
		enter_zip.send_keys(zip)
		
		submit = driver.find_element_by_xpath('//button[contains(@class,"ic-btn ic-btn-primary '
							'ic-btn-block")]')
		submit.click()
		
		try:
			print("looking for stupid address module")
			WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.XPATH,'//*[@class="icModalContent addressPickerModal"]')
				))
			print("found address picker module")
			print(driver.find_element_by_xpath('//*[@class="icModalContent addressPickerModal"]'))
			exit = driver.find_element_by_xpath('//*[@class="ic-icon ic-icon-x-bold icModalClose"]')
			# exit =
			time.sleep(1)
			exit.click()
			print("clicked out of choose address")
		except:
			x=0
			
		WebDriverWait(driver, delay).until(
				EC.presence_of_element_located(
				(By.CLASS_NAME,"twitter-typeahead")
				))
		try:
			error = driver.find_element_by_class_name('error-module***')
			error = True
			print("error = true")
		except:
			error = False
			print("error = false")
		
		return error, pick_up
	
	elif pick_up == True:
		error = False
		return error, pick_up
		
def search_for_cat(category, driver):
	
	time.sleep(3)
	
	WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, "twitter-typeahead")
			))

		
	try:
		gotit = driver.find_element_by_class_name('grocery-icon').click()
	except:
		x=0
			
	search_box = driver.find_elements_by_xpath('//div[@class="search=bar primary-nav-search-bar"]')
	
	try:
		bad_weather_notice = driver.find_element_by_class_name('toast-dismiss').click()
	except:
		x=0
			
	print("len search box: %s" %len(search_box))
	
	
	try:
		search_box = driver.find_element_by_xpath('//div[@class="search-bar primary-nav-search-bar"]//'
													'input[@class="tt-input search-field"]')
		for x in range(0,30):
			search_box.send_keys(Keys.BACKSPACE)
		print("search box [0]")
	except:
		driver.execute_script("window.history.go(-1)")
		WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.XPATH, '//div[@class="search-bar primary-nav-search-bar"]')
			))
		search_box = driver.find_element_by_xpath('//div[@class="search-bar primary-nav-search-bar"]//'
													'input[@class="tt-input search-field"]')
		for x in range(0,30):
			search_box.send_keys(Keys.BACKSPACE)
		print("search box [1]")
	
	try:
		gotit = driver.find_element_by_class_name('grocery-icon').click()
	except:
		x=0
	
	try:
		print("checking for choose address module")
		WebDriverWait(driver, 2).until(
				EC.presence_of_element_located(
				(By.XPATH,'//*[@class="icModalContent addressPickerModal"]')
				))
		exit = driver.find_element_by_xpath('//*[@class="ic-icon ic-icon-x-bold icModalClose"]')
		exit.click()
		print("clicked out of choose address")
	except:
		x=0	
		
	search_box.send_keys(category)
	print("entered category")
	
	try:
		gotit = driver.find_element_by_class_name('grocery-icon').click()
	except:
		try:
			choose_store = driver.find_element_by_class_name('location-name')	
			
			a = driver.find_element_by_xpath('//button[@class="pickup-only-modal-'
			 'location-item ic-btn ic-btn-secondary"]')
			
			a.click()
			
			submit = driver.find_element_by_xpath('//button[@class="ic-btn'
							' ic-btn-success"]')
			submit.click()
			print("clicked enter")
		except:
			print("no got it or pickup to get rid of")
			
	try:
		enter = driver.find_element_by_xpath('//div[@class="search-bar '
						'primary-nav-search-bar"]//button[@type="submit"]')
		
		enter.click()
		# print("clicked enter")
	except:
		# try:
		search_box.send_keys(Keys.ENTER)
		print("clicked enter")
		# except:
			# no_retailer = driver.find_element_by_xpath('//i[@class="ic-icon ic-icon-x-bold icModalClose"]')
			# no_retailer.click()
			# demo = True
	time.sleep(2)
	try:
		demo = driver.find_element_by_link_text('Instacart Demo')
		demo = True
	except:
		demo = False
		
	time.sleep(2)
	
	return demo
	
def get_aisle(driver, category):
	try:
		all_results = driver.find_element_by_xpath('//a[@class="'
					'ic-btn ic-btn-sm ic-btn-secondary"]')
		all_results.click()
		print("more results")
		return False
		
	except:
		# try:
			# WebDriverWait(driver, delay).until(
					# EC.presence_of_element_located(
					# (By.XPATH, '//li[@class="dropdown nav-dropdown"]')
					# ))
					
			# dropdown = driver.find_element_by_xpath('//li[@class="dropdown nav-dropdown"]')
			# dropdown.click()
			# print("clicked dropdown")
			# time.sleep(1)
		# except:
			# try:
				# search_for_cat(category, driver)
				# WebDriverWait(driver, delay).until(
					# EC.presence_of_element_located(
					# (By.XPATH, '//li[@class="dropdown nav-dropdown"]')
					# ))
					
				# dropdown = driver.find_element_by_xpath('//li[@class="dropdown nav-dropdown"]')
				# dropdown.click()
			# except:
				# return True
		# WebDriverWait(driver, delay).until(
		# EC.presence_of_element_located(
		# (By.CLASS_NAME, 'dropdown-menu')
		# ))
		
		
		# text = driver.find_element_by_xpath('html[@lang="en"]').text
		# text = text.encode('utf-8').strip()
		
		try:
			
			if category == 'juice':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Juice & Nectars")]')

			if category == 'bread':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Bread")]')
				
			if category == 'bottled water':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Water, Seltzer & Sparkling Water")]')	
			
			if category == 'milk':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Milk")]')	
			
			if category == 'pasta':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Dry Pasta")]')	
				
			if category == 'cereal':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Cereal")]')	
				
			if category == 'soft drinks':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Soft Drinks")]')	
			
			if category == 'tea':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Tea")]')	
			
			if category == 'sports and energy drinks':
				aisle = driver.find_element_by_xpath('.//div[@class="inline"]//span[contains(text(), "Energy & Sports Drinks")]')	
			
			try:			
				aisle.click()
			except:
				dropdown.click()
			
			time.sleep(1)	
			
			time.sleep(random.randint(0,3))
			print("clicked on aisle")
			return False
			
		except:
			
			return True
			
def get_stores(driver):
	
	x = random.randint(1,80)
	if x == 30:
		print("pausing")
		time.sleep(20)
	
	try:
		store_link	= driver.find_element_by_xpath('//a[@class="primary-nav-link"]')
		store_link.click()
		
	except:
		try:
			store_link	= driver.find_element_by_xpath('//a[@class="primary-nav-link"]')
			store_link.click()
			choose_store = driver.find_element_by_xpath('//i[@class="ic-icon ic-icon-x-bold icModalClose"]')
			choose_store.click()
		except:
			no_retailer = driver.find_element_by_xpath('//i[@class="ic-icon ic-icon-x-bold icModalClose"]')
			no_retailer.click()
	
	time.sleep(2)
	
	WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, "retailer-chooser-header")
			))
			
	stores = driver.find_elements_by_xpath('.//div[@class="retailer-option-body"]')
	
	print("number of stores: %s" %len(stores))
	
	return len(stores)
		
def click_on_store(driver, i):
	print("in click on store")
	
	try:
			bad_weather_notice = driver.find_element_by_class_name('toast-dismiss').click()
	except:
			x=0

	WebDriverWait(driver, delay).until(
		EC.presence_of_element_located(
		(By.CLASS_NAME, "retailer-group-label")
		))
		
	reset = False
	skip = False
	
	WebDriverWait(driver, delay).until(
		EC.presence_of_element_located(
		(By.CLASS_NAME, "retailer-option-inner-wrapper")
		))
	time.sleep(random.randint(0,3))
	try:	
		store = driver.find_elements_by_xpath('.//div[@class="retailer-option-body"]')[i]
	except:
		# try:
		time.sleep(5)
		print(len(driver.find_elements_by_class_name('ic-text-truncate')))
		store =driver.find_elements_by_xpath('.//div[@class="retailer-option-body"]')[i]

		# except:
			# reset = True
			# true = False
			# return reset, skip
	try:
		bad_weather_notice = driver.find_element_by_class_name('toast-dismiss').click()
		time.sleep(1)
	except:
		x=0	
	
	store.click()
		
		
	try:
		choose_store = driver.find_element_by_class_name('location-name')	
		
		a = driver.find_element_by_xpath('//button[@class="pickup-only-modal-'
		 'location-item ic-btn ic-btn-secondary"]')
		
		a.click()
		
		submit = driver.find_element_by_xpath('//button[@class="ic-btn'
						' ic-btn-success"]')
		submit.click()
		
	except:
		print("has delivery")
		
	print("clicked on store")
	
	
	
	return reset, skip
	
def prep_file(zip, category, id, insta):

	zip_path = os.path.join(insta, zip)
	zip_cat_path = os.path.join(zip_path, category)
	if not os.path.exists(zip_cat_path):
		os.makedirs(zip_cat_path)
					
	file = open(os.path.join(zip_cat_path, id + ".txt"), "w")
	
	return file
					
def get_data(file, driver, category, zip):

	time.sleep(1)
	
	try:
		demo = driver.find_element_by_link_text('Instacart Demo')
		demo = True
	except:
		demo = False
		
	if demo == True:
		print("not available in this zip")
		done_file = open(done_zips_name, 'a')
		done_file.write(zip + "," + "no service" + "\n")
		done_file.close()
		return
		
	try:
		pages = driver.find_element_by_class_name('pagination-info').text
		pages = str(pages)
		pages = pages.split()
		
	except:
		try:
			time.sleep(5)
			pages = driver.find_element_by_class_name('pagination-info').text
			pages = str(pages)
			pages = pages.split()
			print(pages)
		except:
			text = driver.find_element_by_xpath('html[@lang="en"]').text
			text = text.encode('utf-8').strip()
			file.write(text)
			return
		
	
	total_pages = pages[3]
	total_pages = int(total_pages)
	print("total pages: %s" %total_pages)
	
	second_try = False
	curr_page = 1
	while curr_page <= total_pages:
	
		WebDriverWait(driver, delay).until(
			EC.presence_of_element_located(
			(By.CLASS_NAME, 'pagination-info')
			))
			
		print("printing page %s" %curr_page)
		
		## get and save all text			
		text = driver.find_element_by_xpath('html[@lang="en"]').text
		text = text.encode('utf-8').strip()
		
		print(str(zip))
		
		if not (str(zip) in text):
			print("in the wrong zip!")
			sys.exit()
		# elif (str(zip) in text):
			# print("in the correct zip")
			
	
		if second_try == False:
			file.write(text)
		
		second_try = False
		try_number = 1
		
		## don't need to click next if it's the last page
		if curr_page < total_pages:
			# print("try number %s" %try_number)
			x = random.randint(1,3)
			time.sleep(x)
			
			x = random.randint(1,70)
			if x == 40:
				print("pausing")
				time.sleep(13)
	
			# try:
			WebDriverWait(driver, delay).until(
					EC.presence_of_element_located(
					(By.CLASS_NAME, "pagination-info")
					))	
			try:		
				arrow = driver.find_element_by_xpath('//a[@class]//span[@class='
						'"ic-icon ic-icon-arrow-right-small-bold"]')
			except:
				time.sleep(3)
				arrow = driver.find_element_by_xpath('//a[@class]//span[@class='
						'"ic-icon ic-icon-arrow-right-small-bold"]')
				
			arrow.click()
			print("clicked on next")
			

		
			WebDriverWait(driver, delay).until(
						EC.presence_of_element_located(
						(By.CLASS_NAME, "pagination-info")
						))
						
			pages = driver.find_element_by_class_name('pagination-info').text
			pages = str(pages)
			pages = pages.split()
			curr_page = pages[1]
			curr_page = int(curr_page)
			total_pages = pages[3]
			total_pages = int(total_pages)
			print("current page %s" %curr_page)
		
		## have to manually go back to first page to reset for next store <- not anymore
		elif curr_page == total_pages:
			curr_page +=1

			
	time.sleep(random.randint(0,3))			
	print("price info saved to text file")		
	
def get_more_results_data(driver, file):
	WebDriverWait(driver, delay).until(
						EC.presence_of_element_located(
						(By.CLASS_NAME, "item-info")
						))
	text = driver.find_element_by_xpath('html[@lang="en"]').text
	text = text.encode('utf-8').strip()
	file.write(text)
	print("printed more")
	
def get_no_data(driver, file, category):

	print("store doesn't sell %s" %category)
	
	text = driver.find_element_by_xpath('html[@lang="en"]').text
	text = text.encode('utf-8').strip()
	file.write(text)
		
def body(area, scrape_name, email_address, password_text, list_of_zips, list_of_categories, done_zips_name, done_list_name, insta):
	main_start_time = time.time()

	df = pd.read_csv(list_of_zips)
	zips = df['zip'].tolist()
	
	df = pd.read_csv(list_of_categories)
	categories = df['category'].tolist()
	
	done_list, done_zips = get_done_lists(done_list_name, done_zips_name)
	
	print("Number zips done: %s" %len(done_zips))
	
	driver = get_to_search_page(email_address, password_text)
	
	for zip in zips: ## loop through all zips
		
		zip = int(zip)
		print(zip)
		if zip in done_zips:
			print("already done with this zip:%s" %zip)
			continue
			
		time.sleep(2)	
		
		zip_start_time = time.time()
		zip = count_letters(str(zip))
		
		
		## set zipcode 
		print("changing zip")
		error, pick_up = change_zip(zip, driver)
		
		try:
			bad_weather_notice = driver.find_element_by_class_name('toast-dismiss').click()
		except:
			x=0
			# print("no bad weather")
				
		x = random.randint(1,3)
		time.sleep(x)
		
		try:
			demo = driver.find_element_by_link_text('Instacart Demo')
			demo = True
			print("demo = true")
		except:
			demo = False
		
		if (error == True) | (demo == True):
			print("not available in this zip")
			done_file = open(done_zips_name, 'a')
			done_file.write(zip + "," + "no service" + "\n")
			done_file.close()
			
		else:
			for category in categories: ## loop through all categories
				cat_start_time = time.time()
				x = random.randint(1,60)
				if x == 30:
					print("pausing")
					time.sleep(7)
				time.sleep(random.randint(0,3))
				print("searching for category %s" %category)
				
				## search for category
				demo = search_for_cat(category, driver)		
				
				try:
					bad_weather_notice = driver.find_element_by_class_name('toast-dismiss').click()
				except:
					x=0				
					
				try:
					demo = driver.find_element_by_link_text('Instacart Demo')
					demo = True
				except:
					demo = False
					
				if demo == True:
					print("not available in this zip")
					done_file = open(done_zips_name, 'a')
					done_file.write(zip + "," + "no service" + "\n")
					done_file.close()
					break
				else:	
					## get list stores
					num_stores = get_stores(driver)
					
					i=0
					while i in range(0,num_stores): ## loop through all stores

						id = zip + "_" + category + "_" + str(i)
						print(id)
										
						if id in done_list:
							print("already got this store's info")
							i+=1
							continue
							
						print("store #: %s" %(i+1))
						try:
							bad_weather_notice = driver.find_element_by_class_name('toast-dismiss').click()
						except:
							x=0
						reset, skip = click_on_store(driver, i)
						print("clicked on store")
						try:
							oops = driver.find_element_by_link_text('Oops')
							oops = True
						except:
							oops = False
						
						if oops == True:
							continue
								
						# if reset == True:
							# error, pick_up = change_zip(zip, driver)
						
						# if skip == True:
							# i+=1
							# continue
						
						demo = search_for_cat(category, driver)	
							
						file = prep_file(zip, category, id, insta)
										
						try: ## see if pages exist
							WebDriverWait(driver, 5).until(
								EC.presence_of_element_located(
								(By.CLASS_NAME, 'pagination-info')
								))
							pages = driver.find_element_by_class_name('pagination-info').text
							pages_exist = True
							more_results = False
						except: 
							try:
								all_results = driver.find_element_by_xpath('//a[@class="'
										'ic-btn ic-btn-sm ic-btn-secondary"]')
								more_results = True
								print("more results")
								pages_exist = False
								more_results = True
							except:
								pages_exist = False
								more_results = False
						
						print("pages exit: %s" %pages_exist)
						print("more results: %s" %more_results)
						if  (pages_exist) | (more_results): ## print info from store that sells category
							print("going to get aisle")
							################	
							bad_store = get_aisle(driver, category)
							if (bad_store == False) & (pages_exist == True):
								print("getting data")
								get_data(file, driver, category, zip)
							elif (bad_store == False) & (more_results == True):
								print("getting more results data")
								get_more_results_data(driver, file)
								
						
						else: ## saves store name if doesn't have soda items
							get_no_data(driver, file, category)
							
						## go back to page with all stores
						try:
							store_link	= driver.find_element_by_xpath('//a[@class="primary-nav-link"]')
							store_link.click()
													
							WebDriverWait(driver, delay).until(
								EC.presence_of_element_located(
								(By.CLASS_NAME, "retailer-chooser-header")
								))
						except:
							try:
								not_available = driver.find_element_by_xpath('//div[@class="icModalContent'
													' errorModal"]')
								
								driver.execute_script("window.history.go(-1)")
								
								store_link	= driver.find_element_by_xpath('//a[@class="primary-nav-link"]')
								store_link.click()
														
								WebDriverWait(driver, delay).until(
									EC.presence_of_element_located(
									(By.CLASS_NAME, "retailer-chooser-header")
									))
							except:
								no_retailer = driver.find_element_by_xpath('//i[@class="ic-icon ic-icon-x-bold icModalClose"]')
								no_retailer.click()
						
						file.close()	
						
						done_list.append(id)
						done_file = open(done_list_name, 'a')
						
						if pick_up == False:
							done_file.write(id + "\n")
						elif pick_up == True:
							done_file.write(id + "," + "pickup" + "\n")
						
						done_file.close()
						
						i+=1
				
			print("run time for this category: %s" %(time.time() - cat_start_time))
		done_zips_file = open(done_zips_name, 'a')
		done_zips_file.write(zip + "\n")

		print("run time for this zip: %s" %(time.time() - zip_start_time))
		
	print("run time for all : %s" %(time.time() - main_start_time))	
	
	driver.close()
	
	print("Woot woot! All done!")
	
def main(area, scrape_name, email_address, password_text):

	print(area, scrape_name, email_address, password_text)
	
	general_path = "H:\Soda_Tax_Scrapes"
	path = general_path + "\\Scrape_" + scrape_name
	
	if not os.path.isdir(path):
		os.makedirs(path)

	insta = os.path.join(path, "Instacart")
	
	if not os.path.isdir(insta):
		os.makedirs(insta)

	list_of_zips = os.path.join(general_path, "zip_list_" + area + ".csv")
	list_of_categories = os.path.join(general_path, "list_categories.csv")
	done_zips_name = os.path.join(insta, "done_zips_" + area + ".csv")
	done_list_name = os.path.join(insta, "done_list_" + area + ".csv")
	
	print(list_of_zips)
		
	try:
		body(area, scrape_name, email_address, password_text, list_of_zips, list_of_categories, done_zips_name, done_list_name, insta)
		
		# send_email('done', 'na')
		
	
	except:
		sys.exit()





if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])