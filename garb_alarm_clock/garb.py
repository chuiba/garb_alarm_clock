# -*- coding: utf-8 -*-

# 这个是用来获取装扮信息的一个类，逻辑上写得简单了些，不想引用太过复杂的库

import requests
import json

# 获取装扮信息
def get_garb_info(garb_id):
    response = requests.get('https://api.bilibili.com/x/garb/mall/item/suit/v2?item_id=' + str(garb_id))
    res = json.loads(response.text)
    print(res['data']['item']['name'])
    print(res['data']['item']['properties']['fan_share_image'])
    print(res['data']['item']['properties']['sale_quantity'])
    print(res['data']['sale_surplus'])
    name = res['data']['item']['name']
    image = res['data']['item']['properties']['fan_share_image']
    surplus = res['data']['sale_surplus']
    quantity = res['data']['item']['properties']['sale_quantity']
    avatar = res['data']['fan_user']['avatar']
    number = int(quantity) - int(surplus)

    # 如果得不到库存（星座系列，换一个接口）
    if int(quantity) == -1:
        number = get_garb_number(garb_id)

    return name, image, avatar, surplus, quantity, str(number)

# 获取装扮编号
def get_garb_number(garb_id):
    response = requests.get('http://api.bilibili.com/x/garb/rank/fan/recent?item_id=' + str(garb_id))
    res = json.loads(response.text)
    print(res['data']['rank'][0]['number'])
    print(res['data']['rank'][0]['nickname'])
    return int(res['data']['rank'][0]['number'])