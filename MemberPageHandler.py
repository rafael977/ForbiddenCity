# pylint: skip-file
import requests as rq
from bs4 import BeautifulSoup
import re
from ReviewHandler import ReviewHandler
from DbHandler import DbHandler

class MemberPageHandler:
    host_uri = 'https://www.tripadvisor.com.sg'
    main_page_url = 'https://www.tripadvisor.com.sg/Attraction_Review-g294212-d319086-Reviews-Forbidden_City_The_Palace_Museum-Beijing.html'
    page_base_url = 'https://www.tripadvisor.com.sg/Attraction_Review-g294212-d319086-Reviews-or{0}-Forbidden_City_The_Palace_Museum-Beijing.html'
    overlay_page_base_url = 'https://www.tripadvisor.com.sg/MemberOverlay?Mode=owa&uid={0}&c=&scr={1}&fus=false&partner=false&LsoId=&metaReferer=Attraction_Review'

    def parse_main_page(self):
        main_page_html = rq.get(self.main_page_url).text
        bs = BeautifulSoup(main_page_html, 'html.parser')

        total_review_num = int(bs.find('p', class_='pagination-details').find_all('b')[-1].string.replace(',', ''))
        
        for offset in range(0, total_review_num, 10):
            print('*** Parse offset', offset, ' ***')
            self.parse_page(self.page_base_url.format(offset))

    def parse_page(self, url):
        page_html = rq.get(url).text
        bs = BeautifulSoup(page_html, 'html.parser')

        review_container = bs.find_all('div', class_='review-container')
        for review in review_container:
            try:
                member_info = review.find('div', class_='memberOverlayLink')['id'].split('-')
                member_uid = member_info[0].split('_')[1]
                review_id = member_info[1].split('_')[1]
                print('--- Processing Member uid: ' + member_uid + ' ---')

                overlay_page_url = self.overlay_page_base_url.format(member_uid, review_id)
                overlay_page_html = rq.get(overlay_page_url).text
                bs_overlay = BeautifulSoup(overlay_page_html, 'html.parser')
                member_page_url = self.host_uri + bs_overlay.find('div', class_='memberOverlayRedesign g10n').a['href']
                print('Member page url: ' + member_page_url)
                self.parse_member_page(member_page_url, member_uid)
            except:
                print('error')

            print('---------------------------------------------\n')

    def parse_member_page(self, url, uid):
        member_page_html = rq.get(url).text
        bs = BeautifulSoup(member_page_html,'html.parser')

        # retrieve member basic info
        name = bs.find('span', class_='nameText').string.strip()
        since = bs.find('p', class_='since').string.strip()[6:]
        age, gender = None, None
        if len(bs.find('div', class_='ageSince').find_all('p')) == 2:
            age_gender = bs.find('div', class_='ageSince').find_all('p')[1].string.strip()
            age_gender_regex = re.compile(r'^((?P<age>\d+-\d+) year old)?( )?(?P<gender>male|female)?$', re.IGNORECASE)
            age_gender_search = age_gender_regex.search(age_gender)
            if age_gender_search:
                age = age_gender_search.group('age')
                gender = age_gender_search.group('gender')
        hometown = bs.find('div', class_='hometown').p.string.strip() if bs.find('div', class_='hometown').p is not None else None

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

        member = {
            '_id': uid,
            'name': name,
            'since': since,
            'age': age,
            'gender': gender,
            'hometown': hometown,
            'travel_styles': travel_styles,
            'contributes': contribs,
            'total_points': total_points,
            'page_url': url,
            'is_processed': False
        }
        print("Member info: ", member)

        # retrieve member ID and review pages
        pattern = re.compile(r'\"memberId:(?P<memberId>[^\"]+)\"', re.IGNORECASE | re.MULTILINE)
        script = bs.find('script', text=pattern)
        if script:
            match = pattern.search(script.string)
            if match:
                member_id = match.group('memberId')
        # print(member_id)

        dh = DbHandler()
        dh.insert_member(member)

# mh = MemberPageHandler()
# mh.parse_main_page()
