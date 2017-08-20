# pylint: skip-file
import requests as rq
import json


class AjaxHandler:
    api_url = 'https://www.tripadvisor.com.sg/ModuleAjax?'
    form_data_template = 'token=TNI1625!ACC4oJqGlUrwLpBdRz9iUz1l/5xvi4KKYn+uNm1AsRM5BNuxKXJQnGRvU93pu5odlJJAcZP312bxUOG6SEOdNkRWtbav6mJvbt89UUR7RCyXxHEeKiCFRvDOFbIC+EE4m+0iz3lJjCb1jHLrJ843KdqA/q8ZKPKwQdIrQSMf27OU&authenticator=DEFAULT&actions=[{{"name":"FETCH","resource":"modules.membercenter.model.ContentStreamComposite","params":{{"offset":{offset},"limit":50,"page":"PROFILE","memberId":"{memberId}"}},"id":"clientaction739"}}]&version=5'

    def __init__(self, referrer_url, num_pages, member_id, reviewer_id):
        self.num_pages = num_pages
        self.member_id = member_id
        self.reviewer_id = reviewer_id
        self.header = {
            'Content-type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Referer': referrer_url,
            'Cookie': 'TASSK=enc%3AAIrEUkgtZFJJkF%2FlUYhg8AHnUfmhpFYAMnd%2FrFIAHIkk%2BEKim90jAtWvAvP1QZDg0PQGo%2BJUqjl7s%2B%2B2wjDmNd2JETdK9EQpopWGEnlnzpby94kQmjLaArTh4UHF7mN5%2Bw%3D%3D; VRMCID=%1%V1*id.10568*llp.%2F*e.1502507669603; TAUnique=%1%enc%3AE5UqlqdSVZaOx3ZjkwsYnRJzhAwvkFPIEzbgP1Gq9dZIgZdMnu2Mwg%3D%3D; TART=%1%enc%3A6rUW17pi2wNPxm4z6lGOBZ3g%2BfoBoz7SGj1dInTAATGP8Z2WJ2lZWjoPLjKU4R7F3c9QTV5l2qQ%3D; ki_t=1502809173147%3B1502809173147%3B1502809173147%3B1%3B1; ki_r=; ki_u=0ac2f740-32fd-b40b-0593-da97; ki_s=174306%3A1.0.0.0.2%3B174450%3A0.0.0.0.2%3B176330%3A0.0.0.0.2; ServerPool=C; TALanguage=en; TATravelInfo=V2*A.2*MG.186337*HP.2*FL.3*RHS.2d7e1_2017-08-27_1*RVL.2231493_216l8355856_216l186337_227l1595153_227l999329_227l319086_230*DSM.1502809451203*RS.1; CM=%1%HanaPersist%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CHanaSession%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CCpmPopunder_1%2C1%2C1503194812%7CCCSess%2C%2C-1%7CCpmPopunder_2%2C4%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7Ccatchpers%2C3%2C1503413774%7CLaFourchette+MC+Banners%2C%2C-1%7Csh%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C1%2C1503414249%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CSCA%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRBASess%2C%2C-1%7Cperssticker%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TAReturnTo=%1%%2FAttraction_Review%3Fg%3D294212%26reqNum%3D1%26d%3D319086%26changeSet%3DREVIEW_LIST; PAC=AOtsdEk1Cgc-_9jui6D9MDnwAjmu9hYoVHHvsEMEzdhejZ_OfijkkXTK0uj2iMJEtFf9kuh1tNKNl_9UezNQ_NNjmxsq-shsR7JMFX3JEAaZ-MLQAokN3g1_Cmi18Va-Juu5miu4hlUzm04ybLqGUya9edevehAr1-GKlYv_bi9yqSg98n96hEBSXxoxQbsawg%3D%3D; PMC=V2*MS.76*MD.20170804*LD.20170820; TASession=%1%V2ID.6366D0F91BB3414DFBF90A93207A3252*SQ.119*PR.427%7C*LS.members*GR.6*TCPAR.36*TBR.17*EXEX.90*ABTR.83*PHTB.29*FS.40*CPU.0*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*MS.-1*RMS.-1*FLO.319086*TRA.false*LD.319086; TAUD=LA-1502980018608-1*RDD-1-2017_08_17*LG-237808059-2.1.F.*LD-237808060-.....; roybatty=TNI1625!ACC4oJqGlUrwLpBdRz9iUz1l%2F5xvi4KKYn%2BuNm1AsRM5BNuxKXJQnGRvU93pu5odlJJAcZP312bxUOG6SEOdNkRWtbav6mJvbt89UUR7RCyXxHEeKiCFRvDOFbIC%2BEE4m%2B0iz3lJjCb1jHLrJ843KdqA%2Fq8ZKPKwQdIrQSMf27OU%2C1'
        }

    
    def get_data(self):
        for i in range(0, self.num_pages):
            # data = self.form_data_template.format(offset = i * 50, memberId = self.member_id)
            # print('Header:', self.header, '\n', 'Data:', data)
            
            # r = rq.post(self.api_url, headers = self.header, data=data)
            # r_data = r.json()
            f = open('test_data.json', 'r')
            r_data = json.load(f)
            f.close()
            review_data = r_data['store']['modules.unimplemented.entity.AnnotatedItem']
            location_data = r_data['store']['modules.unimplemented.entity.JSONLocation']
            for review_key in review_data.keys():
                review = review_data[review_key]
                location_key = str(review['locationId'])
                location = location_data[location_key]
                if location['city'] == 'Beijing':
                    review_item = {
                        '_id': review['id'],
                        'member_id': self.reviewer_id,
                        'location_id': int(location_key),
                        'review': review['title'],
                        'rating': review['rating']
                    }
                    print('Review: ', review_item)
                    location_item = {
                        '_id': location['id'],
                        'place': location['location_string'],
                        'category': location['category']['name']
                    }
                    print('Location: ', location_item)


ah = AjaxHandler('https://www.tripadvisor.com.sg/members/TipperNC', 1, 'rbpjt2soKDc=', '123')
ah.get_data()
