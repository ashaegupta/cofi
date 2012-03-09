def new_place_dict_from_json(json):
    p = json
    p["food"] = None
    p["outlets"] = None
    return p
    
'''
class Place():
    str_attrs = [
        "id",
        "name",
        "image_url",
        "url",
        "mobile_url",
        "phone",
        "display_phone",
        "rating_img_url",
        "rating_img_url_small",
        "location_city"
        ]
        
    num_attrs = [
        "location_coordinate_latitude",
        "location_coordinate_latitude",
        "review_count",
        "rating",
        "outlets",
        "food",
        ]
    
    dict_attrs = [
        "location",
        "location_coordinate",
        "location_address",
        "location_display_address"
        ]

    for s in str_attrs:
        setattr(self, s, "")
        
    for n in num_attrs:
        setattr(self, n, None)

    for n in num_attrs:
        setattr(self, n, None)

'''   