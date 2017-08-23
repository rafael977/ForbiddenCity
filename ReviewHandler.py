# pylint: skip-file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class ReviewHandler:
    location_category_mapping = {
        'sprite-feedHotel':'hotel',
        'sprite-feedAttraction':'attraction',
        'sprite-feedRestaurant': 'restaurant'
    }
    review_rating_mapping = {
        'bubble_1': 1,
        'bubble_2': 2,
        'bubble_3': 3,
        'bubble_4': 4,
        'bubble_5': 5
    }

    def __init__(self, url, member_uid):
        self.member_uid = member_uid
        self.driver = webdriver.Chrome('driver\chromedriver.exe')
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 30)

    def get_data(self):
        reviews = []
        locations = []
        page = self.driver.page_source
        page_reviews, page_locations = self.parse_page(page, self.member_uid)
        reviews.extend(page_reviews)
        locations.extend(page_locations)
        
        button = self.driver.find_element_by_id('cs-paginate-next')

        while 'disabled' not in button.get_attribute('class'):
            self.driver.execute_script('return document.getElementsByClassName("cs-content-container")[0].remove();')        
            button.click()
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cs-content-container')))

            page = self.driver.page_source
            page_reviews, page_locations = self.parse_page(page, self.member_uid)
            reviews.extend(page_reviews)
            locations.extend(page_locations)

            button = self.driver.find_element_by_id('cs-paginate-next')
            
        print(reviews, locations)        
        self.driver.close()
        return reviews, locations

    def parse_page(self, page, member_uid):
        bs = BeautifulSoup(page, 'html.parser')
        all_reviews = bs.find_all('li', class_='cs-review')
        reviews = []
        locations = []
        for review in all_reviews:
            location = review.find('div', class_='cs-review-location').a.string.strip()
            if 'Beijing' in location:
                reviews.append({
                    'member_id': member_uid,
                    'location_id': location,
                    'review': review.find('a', class_='cs-review-title').string.strip(),
                    'rating': self.review_rating_mapping[review.find('div', class_='cs-review-rating').span['class'][1]]
                })
                locations.append({
                    '_id': location,
                    'location': location,
                    'category': self.location_category_mapping[review.find('div', class_='cs-type-hint')['class'][1]]
                })
        return reviews, locations

# rh = ReviewHandler('https://www.tripadvisor.com.sg/members/TipperNC', 'uid123')
# rh.get_data()