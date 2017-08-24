# pylint: skip-file
import requests as rq
import json
from bs4 import BeautifulSoup
import re

class ReviewHandler:
    cookie_ping_url = 'https://www.tripadvisor.com.sg/CookiePingback'
    data_url = 'https://www.tripadvisor.com.sg/ModuleAjax'
    headers = {
        'accept': "text/javascript, text/html, application/xml, text/xml, */*",
        'origin': "https://www.tripadvisor.com.sg",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'dnt': "1",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-SG,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,en-US;q=0.2,zh-TW;q=0.2"
    }
    action = '[{{"name":"FETCH","resource":"modules.membercenter.model.ContentStreamComposite","params":{{"offset":{offset},"limit":50,"page":"PROFILE","memberId":"{memberId}"}},"id":"clientaction739"}}]'
    data = {
        'actions': "",
        'authenticator':'DEFAULT',
        'token': "",
        'version':5
    }
    
    def __init__(self, member_page_url, member_uid):
        self.session = rq.session()
        self.session.headers = self.headers
        self.member_page_url = member_page_url
        self.member_uid = member_uid

    
    def get_reviews(self):
        page = self.session.get(self.member_page_url)

        bs = BeautifulSoup(page.text, 'html.parser')
        # retrieve member ID and review pages
        pattern = re.compile(r'\"memberId:(?P<memberId>[^\"]+)\"', re.IGNORECASE | re.MULTILINE)
        script = bs.find('script', text=pattern)
        if script:
            match = pattern.search(script.string)
            if match:
                member_id = match.group('memberId')
        # retrieve token
        pattern = re.compile(r"'token': \"(?P<token>[^\"]+)\"", re.IGNORECASE | re.MULTILINE)
        script = bs.find('script', text=pattern)
        if script:
            match = pattern.search(script.string)
            if match:
                token = match.group('token')
        # set cookie
        rq.utils.add_dict_to_cookiejar(self.session.cookies, {'roybatty': token})
        self.session.post(self.cookie_ping_url, params = {"early":"true"}, cookies = self.session.cookies)
        # print(self.session.cookies)
        # retrieve number of pages
        num_pages = int(bs.find('div', class_='cs-pagination-bar-inner').contents[-1].string.strip())

        for i in range(0, num_pages):
            self.data['actions'] = self.action.format(offset= i * 50, memberId = member_id)
            self.data['token'] = token
            # print(self.data)
            
            r = self.session.post(self.data_url, data=self.data)
            print(r.text)
            reviews = []
            places = []
            if r.json():
                r_data = r.json()

                review_data = r_data['store']['modules.unimplemented.entity.AnnotatedItem']
                location_data = r_data['store']['modules.unimplemented.entity.JSONLocation']

                for review_key in review_data.keys():
                    review = review_data[review_key]
                    location_key = str(review['locationId'])
                    if location_key in location_data.keys():
                        location = location_data[location_key]
                        if location['city'] == 'Beijing':
                            review_item = {
                                '_id': str(review['id']),
                                'member_id': self.member_uid,
                                'location_id': location_key,
                                'review': review['title'],
                                'rating': review['rating'],
                                'date': review['formattedDate']
                            }
                            location_item = {
                                '_id': str(location['id']),
                                'place': location['location_string'],
                                'category': location['category']['name']
                            }
                            reviews.append(review_item)
                            places.append(location_item)

            return reviews, places

rh = ReviewHandler('https://www.tripadvisor.com.sg/members/katak27', 'uid')
reviews, places = rh.get_reviews()
print('Reviews: ', reviews, '\n', 'Places: ', places)