from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import json
import re

app = Flask(__name__)

# url = ('https://www.zillow.com/rental-manager/market-trends/san-marcos-ca/')
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
# sibling = soup.find(id="modal-root")
# next_sibling = sibling.find_next_sibling("script")

# city: separate spaces with hyphens
# state: use abbreviations
# def get_formatted_location_url(state, city):
bedrooms_quantity = ['0', '1', '2', '3', '4plus']

def get_formatted_location_url(zip, bedrooms=None, has_beds=False):
	zipcode = zip
	url =  ("https://www.zillow.com/rental-manager/market-trends/{}".format(zipcode))
	if has_beds:
		print('bedrooms: ', bedrooms, type(bedrooms))
		beds = bedrooms_quantity[int(bedrooms)]
		print('beds: ', beds, type(beds))
		if int(bedrooms) >= 4:
			beds = bedrooms_quantity[4]
		url =  ("https://www.zillow.com/rental-manager/market-trends/{}/?bedrooms={}".format(zipcode, beds))
	# url =  ("https://www.zillow.com/rental-manager/market-trends/{zipcode}".format(zipcode=location['zipcode']))
	# location = {'state': state, 'city': city}
	# url =  ("https://www.zillow.com/rental-manager/market-trends/{city}-{state}/".format(state=location['state'], city=location['city']))
	
	print('url: ', url, type(url))
	return url

bedrooms_quantity = ['0', '1', '2', '3', '4plus']
# bedrooms arg should be a string
def get_page_content(zipcode, bedrooms=None, has_beds=False):
	agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	page = requests.get(get_formatted_location_url(zipcode), headers=agent)
	# url = get_formatted_location_url(state, city)
	if has_beds:
		url = get_formatted_location_url(zipcode, bedrooms, has_beds)
	else:
		url = get_formatted_location_url(zipcode)

	# url = ('https://www.zillow.com/rental-manager/market-trends/san-marcos-ca/')
	page = requests.get(url)
	# data = page.text
	parsed_data = parse(page).string
	# print(parsed_data)
	# x = re.search(r"\b^unfilteredMarketStats(.*?)user$\b", parsed_data.string).group(0)
	# x = re.search(r'^unfilteredMarketStats.user$', input(parsed_data.string), flags=re.MULTILINE)
	# re.DOTALL for multiple lines

	# if has_beds:
	regex_data = re.findall(r'"marketStats":(.*?),"user', parsed_data)
	# else:
	# 	regex_data = re.findall(r'"unfilteredMarketStats":(.*?),"user', parsed_data)
	# print(regex_data[0])
	json_object = json.loads(regex_data[0])
	print(json_object)
	# print('date:' ,json_object["date"])
	# print('areaName:' ,json_object["areaName"])
	# print('areaType:' ,json_object["areaType"])
	# print('medianRent:' ,json_object["medianRent"])
	# print('minRent:' ,json_object["minRent"])
	# print('maxRent:' ,json_object["maxRent"])
	# print('monthlyChange:' ,json_object["monthlyChange"])
	# print('yearlyChange:' ,json_object["yearlyChange"])
	return render_template('index.html', details=parsed_data)

def parse(page):
	soup = BeautifulSoup(page.content, 'html.parser')
	sibling = soup.find(id="modal-root")
	print('sibling: ', sibling)
	next_sibling = sibling.find_next_sibling("script")
	# print(type(next_sibling.string))
	# print(next_sibling.string)
	return next_sibling

with app.app_context():
	get_page_content('92708', '1', True)


if __name__ == "__main__":
	app.run(debug=True)