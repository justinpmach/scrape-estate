from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import json
import re

app = Flask(__name__)


def get_page_content(zipcode):
	agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	page = requests.get(get_formatted_location_url(zipcode), headers=agent)
	parsed_data = parse(page).string
	# print('parsed_data: ', parsed_data)
	regex_data = re.findall(r'"unfilteredMarketStats":(.*?),"user', parsed_data)
	print(regex_data[0])
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

def get_formatted_location_url(zipcode):
	location = {'zipcode': zipcode}
	return ("https://www.zillow.com/rental-manager/market-trends/{zipcode}/?bedrooms=1".format(zipcode=location['zipcode']))

def parse(page):
	soup = BeautifulSoup(page.content, 'html.parser')
	print('soup: ', soup, type(soup))
	sibling = soup.find(id="modal-root")
	print('sibling: ', sibling)
	next_sibling = sibling.find_next_sibling("script")
	return next_sibling;

with app.app_context():
	get_page_content('92708')


# if __name__ == "__main__":
# 	app.run(debug=True)