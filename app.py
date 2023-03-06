from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import json
import re
from csv import writer

app = Flask(__name__)

def get_page_content(zipcode, bedrooms):
	agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	page = requests.get(get_formatted_location_url(zipcode, bedrooms), headers=agent)
	parsed_data = parse(page).string
	# print('parsed_data: ', parsed_data)
	regex_data = re.findall(r'"marketStats":(.*?),"search', parsed_data)
	# regex_data = re.findall(r'"unfilteredMarketStats":(.*?),"user', parsed_data)
	# print('regex data: ', regex_data)
	json_object = json.loads(str(regex_data[0]))
	# print('json_object: ',json_object)
	# 'areaType': json_object["areaType"],
	# bedrooms = bedrooms,
	area_name = json_object["areaName"],
	date = json_object["date"],
	temperature = json_object["temperature"],
	median_rent = json_object["medianRent"],
	min_rent = json_object["minRent"],
	max_rent = json_object["maxRent"],
	monthly_change = json_object["monthlyChange"],
	yearly_change = json_object["yearlyChange"]
	# print('areaDetails: ', areaDetails)
	print(json_object["areaName"])
	# with open('rentals.csv', 'w', encoding='utf8', newline='') as f:
	# 	thewriter = writer(f)
	# 	header = [
	# 		'AREA',
	# 		'ZIPCODE',
	# 		'DATE',
	# 		'AVERAGE RENT FOR 2 BEDROOM APARTMENT',
	# 		'MINIMUM RENT',
	# 		'MONTH OVER MONTH CHANGE',
	# 		# 'DIFFERENCE',
	# 		'YEARLY CHANGE',
	# 		# 'RENT TREND',
	# 		'TEMPERATURE'
	# 	]
	# 	thewriter.writerow(header)
	info = [
		area_name,
		area_name,
		date,
		median_rent,
		min_rent,
		monthly_change,
		yearly_change,
		temperature
	]
	# 	thewriter.writerow(info)

	# return render_template('index.html', details=parsed_data)
	return info

def get_formatted_location_url(zipcode, bedrooms):
	details = {'zipcode': zipcode, 'bedrooms': bedrooms}
	return ("https://www.zillow.com/rental-manager/market-trends/{zipcode}/?bedrooms={bedrooms}".format(zipcode=details['zipcode'], bedrooms=details['bedrooms']))

def parse(page):
	soup = BeautifulSoup(page.content, 'html.parser')
	# print('soup: ', soup, type(soup))
	sibling = soup.find(id="modal-root")
	# print('sibling: ', sibling)
	next_sibling = sibling.find_next_sibling("script")
	return next_sibling;

def write_csv_file(info):
	with open('rentals.csv', 'w', encoding='utf8', newline='') as f:
		thewriter = writer(f)
		header = [
			'AREA',
			'ZIPCODE',
			'DATE',
			'AVERAGE RENT FOR 2 BEDROOM APARTMENT',
			'MINIMUM RENT',
			'MONTH OVER MONTH CHANGE',
			# 'DIFFERENCE',
			'YEARLY CHANGE',
			# 'RENT TREND',
			'TEMPERATURE'
		]
		thewriter.writerow(header)
		new_info = []
		for result in info:
			result = str(result).replace('(','').replace(')','').replace('"', '').replace(',', '')
			# result = ''.join(str(result))
			new_info.append(result)
		thewriter.writerow(new_info)

with app.app_context():
	# get_page_content('92708', '1')
	write_csv_file(get_page_content('92708', '1'))

# if __name__ == "__main__":
# 	app.run(debug=True)

# areaDetails = {
# 	'areaName': json_object["areaName"],
# 	'areaType': json_object["areaType"],
# 	'date': json_object["date"],
# 	'bedrooms': bedrooms,
# 	'temperature': json_object["temperature"],
# 	'medianRent': json_object["medianRent"],
# 	'minRent': json_object["minRent"],
# 	'maxRent': json_object["maxRent"],
# 	'monthlyChange': json_object["monthlyChange"],
# 	'yearlyChange': json_object["yearlyChange"],
# }