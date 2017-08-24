# pylint:skip-file
from MemberPageHandler import MemberPageHandler
from DbHandler import DbHandler
from ReviewHandler import ReviewHandler

# mh = MemberPageHandler()
# mh.parse_main_page()

dbh = DbHandler()
members = dbh.get_all_not_processed_member()
while members.count() > 0: # loop until all member processed
    for member in members:
        print('--- Processing member id: ', member['_id'], 'page: ', member['page_url'], ' ---')
        rh = ReviewHandler(member['page_url'], member['_id'])
        try:
            reviews, locations = rh.get_reviews()
            dbh.insert_places(locations)
            dbh.insert_reviews(reviews)

            dbh.set_member_processed(member['_id'])
        except Exception as e:
            print(e)
        print('-----------------------------------------------')

    members = dbh.get_all_not_processed_member()

