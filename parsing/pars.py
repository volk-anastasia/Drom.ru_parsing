from bs4 import BeautifulSoup
from requests import get
from time import sleep
from random import random
import csv

page = 1
cars = []

for page in range(1, 101):
    print(page)
    url = f'https://tomsk.drom.ru/auto/used/all/page{page}/?unsold=1'
    value = random()
    scaled_value = 1 + (value * (9 - 5))
    sleep(scaled_value)
    response = get(url)
    html_page = BeautifulSoup(response.text, 'html.parser')  # код страницы

    car_offers = html_page.find_all('a', class_='css-1oas0dk e1huvdhj1')
    for car in car_offers:
        car_data = {}
        car_head = car.find('div', class_='css-16kqa8y e3f4v4l2')
        car_head_list = car_head.text.split(',')

        car_name = car_head_list[0]
        if car_name:
            car_data['car_name'] = car_name

        car_year = car_head_list[1]
        if car_year:
            car_data['car_year'] = car_year

        car_price = (car.find('div', class_='css-1dv8s3l eyvqki91'))
        if car_price:
            car_data['car_price'] = car_price.text.replace('\xa0', '').replace('₽', '')

        car_region = (car.find('span', class_='css-1488ad e162wx9x0'))
        if car_region:
            car_data['car_region'] = car_region.text

        car_tech = (car.find('div', class_='css-1fe6w6s e162wx9x0')
                    .find_all('span', class_='css-1l9tp44 e162wx9x0'))
        car_tech_list = [element.get_text().strip() for element in car_tech]
        for row in car_tech:
            row = row.text.split(',')
            temp_list = [element.strip().replace(' км', '') for element in row if element.strip()]
            temp_list = temp_list[:5]
            car_tech_list.append(temp_list)

            car_engine = car_tech_list[0]
            if car_engine:
                car_data['car_engine'] = car_engine

            car_petrol = car_tech_list[1]
            if car_petrol:
                car_data['car_petrol'] = car_petrol

            car_transmission = car_tech_list[2]
            if car_transmission:
                car_data['car_transmission'] = car_transmission

            car_drive = car_tech_list[3]
            if car_drive:
                car_data['car_drive'] = car_drive

            try:
                car_mileage = car_tech_list[4]
                if car_mileage:
                    car_data['car_mileage'] = car_mileage.replace('км', '').replace(' ', '')
            except IndexError:
                pass
            except AttributeError:
                pass
        cars.append(car_data)

with open('../carsu_Томск.csv', mode='w', newline='', encoding='utf-16') as csvfile:
    fieldnames = ['car_name', 'car_year', 'car_price',
                  'car_region', 'car_engine', 'car_petrol',
                  'car_transmission', 'car_drive', 'car_mileage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cars)
