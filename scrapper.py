# pylint: skip-file
import requests as rq
from bs4 import BeautifulSoup
import re

host_uri = 'https://www.tripadvisor.com.sg'
main_page_url = 'https://www.tripadvisor.com.sg/Attraction_Review-g294212-d319086-Reviews-Forbidden_City_The_Palace_Museum-Beijing.html'
page_base_url = 'https://www.tripadvisor.com.sg/Attraction_Review-g294212-d319086-Reviews-or{0}-Forbidden_City_The_Palace_Museum-Beijing.html'
overlay_page_base_url = 'https://www.tripadvisor.com.sg/MemberOverlay?Mode=owa&uid={0}&c=&scr={1}&fus=false&partner=false&LsoId=&metaReferer=Attraction_Review'

def parse_main_page():
    
    main_page_html = rq.get(main_page_url).text
    bs = BeautifulSoup(main_page_html, 'html.parser')

    total_review_num = int(bs.find('p', class_='pagination-details').find_all('b')[-1].string.replace(',', ''))
    
    for offset in range(0, total_review_num, 10):
        parse_page(page_base_url.format(offset))

def parse_page(url):
    page_html = rq.get(url).text
    bs = BeautifulSoup(page_html, 'html.parser')

    review_container = bs.find_all('div', class_='review-container')
    for review in review_container:
        member_info = review.find('div', class_='memberOverlayLink')['id'].split('-')
        member_id = member_info[0].split('_')[1]
        review_id = member_info[1].split('_')[1]
        print('---Processing review id: ' + review_id + '---')
        print('Member id: ' + member_id)

        review_quotes = review.find('span', class_='noQuotes').string
        print('Quote: ' + review_quotes)

        rating_text = review.find('div', class_='rating reviewItemInline').span['class']
        rating = {
            'ui_bubble_rating bubble_10': 10,
            'ui_bubble_rating bubble_20': 20,
            'ui_bubble_rating bubble_30': 30,
            'ui_bubble_rating bubble_40': 40,
            'ui_bubble_rating bubble_50': 50
        }[rating_text]

        review = {
            '_id': review_id,
            'member_id': member_id,
            'review': review_quotes,
            'rating': rating
        }

        overlay_page_url = overlay_page_base_url.format(member_id, review_id)
        overlay_page_html = rq.get(overlay_page_url).text
        bs_overlay = BeautifulSoup(overlay_page_html, 'html.parser')
        member_page_url = host_uri + bs_overlay.find('div', class_='memberOverlayRedesign g10n').a['href']
        print('Member page url: ' + member_page_url)
        parse_member_page(member_page_url, member_id)

        print('---------------------------------------------\n')

def parse_member_page(url, id):
    member_page_html = rq.get(url).text
    bs = BeautifulSoup(member_page_html,'html.parser')

    # retrieve member basic info
    name = bs.find('span', class_='nameText').string.strip()
    since = bs.find('p', class_='since').string.strip()[6:]
    age_gender = bs.find('div', class_='ageSince').find_all('p')[1].string.strip()
    age_gender_regex = re.compile(r'^((?P<age>\d+-\d+) year old)?( )?(?P<gender>male|female)?$', re.IGNORECASE)
    age_gender_search = age_gender_regex.search(age_gender)
    age = age_gender_search.group('age')
    gender = age_gender_search.group('gender')
    # retrieve travel style
    travel_styles = []
    for node in bs.find_all('div', class_='tagBubble unclickable'):
        travel_styles.append(node.contents[1].strip())
    # retieve contribution
    contribs = []
    contrib_nodes = bs.find('div', class_='modules-membercenter-content-summary').find_all('a', class_='content-link')
    for c in contrib_nodes:
        key = c['name']
        value = c.string.split(' ')[0]
        contribs.append({key:value})
    # retrieve total points
    total_points = int(bs.find('div', class_='points_info tripcollectiveinfo').find('div', class_='points').string.strip().replace(',', ''))

    parse_member_reviews(bs)
    print('''Name: {},
Since: {},
Age: {},
Gender: {},
Travel Style: {},
Contributions: {},
Total Points: {}'''.format(name, since, age, gender, travel_styles, contribs, total_points))

def parse_member_reviews(bs):
    
    pass

# parse_page('https://www.tripadvisor.com.sg/Attraction_Review-g294212-d319086-Reviews-Forbidden_City_The_Palace_Museum-Beijing.html')
parse_member_page('https://www.tripadvisor.com.sg/members/arcmed72', 1)
parse_member_page('https://www.tripadvisor.com.sg/members/JodyBAdelaide', 1)