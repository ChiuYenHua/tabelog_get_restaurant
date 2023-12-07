import requests
import re
import json
from multiprocessing.dummy import Pool as ThreadPool

# Class for get data from tabelog (by place, ex. 'tokyo')
class Tabelog():
    def __init__(self, place):
        # Base url of tabelog tw
        self.base_html ='https://tabelog.com/tw/'
        # Record place want to get data
        self.place = place
        # Record all restaurant type from tabelog(ex. 'ramen', 'steak')
        self.restaurant_type_list = self.__get_all_restaurant_type(self.place)
        # Record all restaurant info by all type in certain place
        self.restaurant_dict_to_write_file = {}

    # Get restaurant type from tabelog+'place'
    def __get_all_restaurant_type(self, place):
        # Get html
        request_html = requests.get(f'{self.base_html}{place}/').text

        # Restaurant type shown by upper picutre in website
        upper_regex =  r'<a class="index-pickup__target" href="https://tabelog.com/tw/tokyo/rstLst/([^<]+)/"><span class="index-pickup__target-inner">([^<]+)</span></a>'
        upper_list = re.compile(upper_regex).findall(request_html)

        # Restaurant type shown by lower picutre in website
        lower_regex = r'<a class="c-link-arrow" href="https://tabelog.com/tw/tokyo/rstLst/([^<]+)/"><span>([^<]+)</span></a>'
        lower_list = re.compile(lower_regex).findall(request_html)

        # Return all type
        return list(set(upper_list + lower_list))
        
    # Get restaurant info by type (input html, extract Top restaurant which score >= 3.5 by type)
    def __get_restaurant_info_from_html(self, html_str):
        restaurant_list_of_dict = []

        restaurant_type_regex = re.compile(r'<div class=\"js-map-marker\"([^<]+)</div>')

        # Extract every restaurant info from html
        for every_restaurant in restaurant_type_regex.findall(html_str):
            temp_dict = {}

            # Extract every detail of restaurant (Str to Dict)
            for every_detail_in_restaturant in every_restaurant.split():
                try:
                    temp_dict[every_detail_in_restaturant.split('=')[0]] = every_detail_in_restaturant.split('=')[1]
                except:
                    pass

            restaurant_list_of_dict.append(temp_dict)

        return sorted(restaurant_list_of_dict, key=lambda d: d['data-score'], reverse=True) 
    
    # Detect if any restaurant score below 3.5, true==there is score below 3.5
    # Input: list of dict
    # Output: bool
    def __check_restaurant_contain_below_score(self, list_of_dict):
        # If empty list, then means out of page
        if list_of_dict==[]:
            return True

        for i in list_of_dict:
            if float(i['data-score'][1:-1]) < 3.50:
                return True
            
        return False

    # Make json file of all restaurant info from 'place'
    def __get_all_restaurnat_info_by_place(self, restaurant_type):
        # Search food webiste start from page one
        page = 1
        # Put every restaurant scored over 3.5 in list
        temp_info_by_type_collect_until_score_below = []

        # Loop through all pages in every restaurant type
        while(1):
            request_html = requests.get(f'https://tabelog.com/tw/{self.place}/rstLst/{page}/?genre_name={restaurant_type[0]}&SrtT=rt').text
            restaurant_info_by_type = self.__get_restaurant_info_from_html(request_html)

            # Check if contains restaurant score < 3.5, then stop for keep searching this food-type
            if self.__check_restaurant_contain_below_score(restaurant_info_by_type):
                break
                
            temp_info_by_type_collect_until_score_below += restaurant_info_by_type
            page += 1
        
        # Make sure no empty list in json file
        if not temp_info_by_type_collect_until_score_below==[]:
            # Update different type of restaurant into dict
            self.restaurant_dict_to_write_file[restaurant_type[0]] = temp_info_by_type_collect_until_score_below
            self.restaurant_dict_to_write_file[restaurant_type[0]+'_chinese'] = restaurant_type[1]

    def multithreading_get_all_restaurnat_info_by_place(self):
        # Loop through all restaurant type (type if a set, ex. ('cake', '蛋糕')) (multithreading process)
        thread = ThreadPool(50)
        thread.map(self.__get_all_restaurnat_info_by_place, self.restaurant_type_list)

    # Write dict result into json file
    def write_result(self):
        with open(f'tabelog_#{self.place}_restaurants_score_above_3.5.json', 'w') as fp:
            json.dump(self.restaurant_dict_to_write_file, fp)



