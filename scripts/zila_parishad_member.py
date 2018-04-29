import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

OUTPUT_FILE = 'zila_parishad_member.csv'

class BiharScraper:
    def __init__(self,
                 base_url='http://sec.bihar.gov.in/ovc.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

        self.form_data = {
            '__EVENTVALIDATION': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEENCRYPTED': ''
        }

    def GetPostList(self):
        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            # get form data
            self.form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            # get post list
            options = Selector(text=ret.text).xpath('//select[@id="ddlPostName"]/option').extract()

            post_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                post = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                post_list.append(post)

            return post_list
        else:
            print('fail to get post list')

    def GetDistrictList(self, post_value):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddlPostName',
            '__EVENTVALIDATION': self.form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.form_data['__VIEWSTATEGENERATOR'],
            'ddlPostName': post_value
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            if len(Selector(text=ret.text).xpath('//select[@id="ddlBlok"]').extract()) > 0:
                self.ddlBlok = True
            if len(Selector(text=ret.text).xpath('//select[@id="ddlPanchayat"]').extract()) > 0:
                self.ddlPanchayat = True
            if len(Selector(text=ret.text).xpath('//select[@id="ddlWard"]').extract()) > 0:
                self.ddlWard = True

            # get form data
            self.post_form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            # get district list
            options = Selector(text=ret.text).xpath('//select[@id="ddlDistrict"]/option').extract()

            district_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                district = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                district_list.append(district)

            return district_list
        else:
            print('fail to get district list')

    def GetPradesikList(self, post_value, district_value):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddlDistrict',
            '__EVENTVALIDATION': self.post_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.post_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.post_form_data['__VIEWSTATEGENERATOR'],
            'ddlDistrict': district_value,
            'ddlPostName': post_value
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.district_form_data = {
                '__EVENTVALIDATION':Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            # get pradesik list
            options = Selector(text=ret.text).xpath('//select[@id="ddlPradesik"]/option').extract()

            pradesik_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                pradesik = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                pradesik_list.append(pradesik)

            return pradesik_list
        else:
            print('fail to get pradesik list')

    def GetReservationStatus(self, post_value, district_value, pradesik_value):
        # set params
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddlPradesik',
            '__EVENTVALIDATION': self.district_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.district_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.district_form_data['__VIEWSTATEGENERATOR'],
            'ddlDistrict': district_value,
            'ddlPostName': post_value,
            'ddlPradesik': pradesik_value
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.pradesik_form_data = {
                '__EVENTVALIDATION':Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            reservation_status = Selector(text=ret.text).xpath('//span[@id="lblResevationShow"]/text()').extract()[0]

            return reservation_status
        else:
            print('fail to get reservation status')

    def GetBiharList(self, post, district, pradesik, reservation_status):
        self.bihar_form_data = {
            '__EVENTVALIDATION': self.pradesik_form_data['__EVENTVALIDATION'],
            '__VIEWSTATE': self.pradesik_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR':self.pradesik_form_data['__VIEWSTATEGENERATOR']
        }

        page_count = 1
        current_page = 1
        while current_page <= page_count:
            # set params
            if current_page == 1:
                params = {
                    '__EVENTARGUMENT': '',
                    '__EVENTTARGET': '',
                    '__EVENTVALIDATION': self.bihar_form_data['__EVENTVALIDATION'],
                    '__LASTFOCUS': '',
                    '__VIEWSTATE': self.bihar_form_data['__VIEWSTATE'],
                    '__VIEWSTATEGENERATOR': self.bihar_form_data['__VIEWSTATEGENERATOR'],
                    'btnSubmit': 'View',
                    'ddlDistrict': district['value'],
                    'ddlPostName': post['value'],
                    'ddlPradesik': pradesik['value']
                }
            else:
                params = {
                    '__EVENTARGUMENT': 'Page$%s' % (current_page),
                    '__EVENTTARGET': 'gvVoterListDetails',
                    '__EVENTVALIDATION': self.bihar_form_data['__EVENTVALIDATION'],
                    '__LASTFOCUS': '',
                    '__VIEWSTATE': self.bihar_form_data['__VIEWSTATE'],
                    '__VIEWSTATEGENERATOR': self.bihar_form_data['__VIEWSTATEGENERATOR'],
                    'ddlDistrict': district['value'],
                    'ddlPostName': post['value'],
                    'ddlPradesik': pradesik['value']
                }

            # set url
            url = self.base_url

            # get request
            ret = self.session.post(url, data=params)

            if ret.status_code == 200:
                # get form data
                self.bihar_form_data = {
                    '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                    '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                    '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
                }

                trs = Selector(text=ret.text).xpath('//table[@id="gvVoterListDetails"]/tr').extract()

                for idx in range(1, len(trs)):
                    tr = trs[idx]

                    # get bihar information
                    if len(Selector(text=tr).xpath('//td[1]/font/text()').extract()) > 0:
                        sr_no = Selector(text=tr).xpath('//td[1]/font/text()').extract()[0]
                        candidate_name = Selector(text=tr).xpath('//td[2]/font/text()').extract()[0]
                        father_husband_name = Selector(text=tr).xpath('//td[3]/font/text()').extract()[0]
                        gender = Selector(text=tr).xpath('//td[4]/font/text()').extract()[0]
                        age = Selector(text=tr).xpath('//td[5]/font/text()').extract()[0]
                        category = Selector(text=tr).xpath('//td[6]/font/text()').extract()[0]
                        educ = Selector(text=tr).xpath('//td[7]/font/text()').extract()[0]
                        mobile_number = Selector(text=tr).xpath('//td[8]/font/text()').extract()[0]
                        address = Selector(text=tr).xpath('//td[9]/font/text()').extract()[0]
                        email = ''
                        if len(Selector(text=tr).xpath('//td[10]/font/text()').extract()) > 0:
                            email = Selector(text=tr).xpath('//td[10]/font/text()').extract()[0]
                        valid_vote = Selector(text=tr).xpath('//td[11]/font/text()').extract()[0]
                        remarks = Selector(text=tr).xpath('//td[12]/font/text()').extract()[0]

                        # write data into output csv file
                        data = []
                        data.append(post['name'])
                        data.append(district['name'])
                        data.append(pradesik['name'])
                        data.append(reservation_status)
                        data.append(sr_no)
                        data.append(candidate_name)
                        data.append(father_husband_name)
                        data.append(gender)
                        data.append(age)
                        data.append(category)
                        data.append(educ)
                        data.append(mobile_number)
                        data.append(address)
                        data.append(email)
                        data.append(valid_vote)
                        data.append(remarks)
                        self.WriteData(data)
                    else:
                        if len(Selector(text=tr).xpath('//table').extract()) > 0 and page_count == 1:
                            tds = Selector(text=tr).xpath('//table/tr/td').extract()
                            page_count = int(Selector(text=tds[-1]).xpath('//font/text()').extract()[0])
                            break

                current_page += 1
            else:
                print('fail to get bihar list')
                return False

        return True

    def WriteHeader(self):
        # set headers
        header_info = [
            'post',
            'district',
            'number',
            'reservation_status',
            'sr_no',
            'candidate_name',
            'father_husband_name',
            'gender',
            'age',
            'category',
            'educ',
            'mobile_number',
            'address',
            'email',
            'valid_vote',
            'remarks'
        ]

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a', encoding='utf-8'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def Start(self,
              start_post='',
              start_district='',
              start_pradesik=''):

        # write header into output csv file
        if start_district == '' and start_pradesik == '': self.WriteHeader()
        # if start_post == '' and start_district == '' and start_pradesik == '': self.WriteHeader()

        # get post list
        print('getting post list...')
        post_list = self.GetPostList()
        print(post_list)

        post_flag = False
        if start_post == '': post_flag = True

        district_flag = False
        if start_district == '': district_flag = True

        pradesik_flag = False
        if start_pradesik == '': pradesik_flag = True

        for post in post_list:
            if start_post == post['name']: post_flag = True
            if post_flag == False: continue

            # get district list
            print('getting district list for %s...' % (post['name']))
            district_list = self.GetDistrictList(post['value'])
            print(district_list)

            for district in district_list:
                if start_district == district['name']: district_flag = True
                if district_flag == False: continue

                # get pradesik list
                print('getting pradesik list for %s:%s...' % (post['name'], district['name']))
                pradesik_list = self.GetPradesikList(post['value'], district['value'])
                print(pradesik_list)

                for pradesik in pradesik_list:
                    if start_pradesik == pradesik['name']: pradesik_flag = True
                    if pradesik_flag == False: continue

                    # get reservation status
                    print('getting reservation status for %s:%s:%s...' % (post['name'], district['name'], pradesik['name']))
                    reservation_status = self.GetReservationStatus(post['value'], district['value'], pradesik['value'])
                    print(reservation_status)

                    # get bihar list
                    print('getting bihar list for %s:%s:%s...' % (post['name'], district['name'], pradesik['name']))
                    ret_val = self.GetBiharList(post, district, pradesik, reservation_status)
                    print(ret_val)

            #         break
            #     break
            break

def main():
    # create scraper object
    scraper = BiharScraper()

    # start to scrape
    scraper.Start(
        start_post='Zila Parishad Member',
        start_district='',
        start_pradesik=''
    )


if __name__ == '__main__':
    main()
