def new_place_dict_from_json(json):
    print "MADE IT TO THIS METHOD" + p
    p = json
    p["food"] = None
    p["outlets"] = None
    return p


'''
class UserHelper(object):
from model.Place import Place

@classmethod
def add_place(klass, first_name, last_name, phone, image_url):
    doc = {
        User.A_FIRST_NAME:first_name,
        User.A_LAST_NAME:last_name,
        User.A_IMAGE_URL:image_url,
        User.A_PHONE:phone
    }
    user_id = User.create_or_update_user(doc)

    if not user_id:
        return ApiResponse.USER_COULD_NOT_CREATE
    else:
        return user_id

@classmethod
def get_user_by_phone(klass, phone):
    user = User.get_user_by_phone(phone)
    if not user:
        return ApiResponse.USER_NOT_FOUND
    else:
        return user

@classmethod
def get_users_by_id(klass, user_ids):
    users = User.get_users_by_user_ids(user_ids)
    if not users:
        return ApiResponse.USER_NOT_FOUND
    else:
        return users

@classmethod
def get_user_by_id(klass, user_id):
    user = User.get_user_by_user_id(user_id)
    if not user:
        return ApiResponse.USER_NOT_FOUND
    else:
        return user    

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