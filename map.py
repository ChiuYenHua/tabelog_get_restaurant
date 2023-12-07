import folium
import json

class build_map():
    def __init__(self, center_location=[35.65829,  139.70226]):
        # Set start center location
        self.center_location = center_location

        # Create map
        self.map = folium.Map(tiles='CartoDB Positron', 
                 location=center_location, 
                 zoom_start=13, 
                 width=1000, 
                 height=1000)
        
        # Read json
        with open('tabelog_#tokyo_restaurants_score_above_3.5.json', 'r') as f:
            self.tabelog_info = json.load(f)

        # Add config
        self.__config()

        # save
        self.map.save('mmap.html')



    def __config(self):
        # Config - add restaurant location
        for key, value in self.tabelog_info.items():
            if 'chinese' not in key:
                for every_restaurant in value:  
                    folium.Marker(
                        [every_restaurant['data-lng'][1:-1],  every_restaurant['data-lat'][1:-1]], popup=every_restaurant['data-name-ja'][1:-1], tooltip=every_restaurant['data-score'][1:-1]
                    ).add_to(self.map)