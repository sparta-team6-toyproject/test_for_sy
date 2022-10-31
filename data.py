from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.rv3ttod.mongodb.net/test')
db = client.hanghae_10_preliminary


city_code = ['CHLUC188064', 'ESMAD187514', 'ITQLD187791', 'GRCHI189400', 'FRPAR187147', 'US40128932', 'MXCUN150807',
             'USNYC60763', 'MV574293953', 'IDDPS294226', 'PHBOR294260', 'PHCEB294261', 'VNDAD298085']

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

for code in city_code:
    main = requests.get(
        f'https://travel.naver.com/overseas/{code}/city/summary', headers=headers)
    visit = requests.get(
        f'https://travel.naver.com/overseas/{code}/city/topPoi/pattr', headers=headers)
    food = requests.get(
        f'https://travel.naver.com/overseas/{code}/city/topPoi/prstr', headers=headers)
    shopping = requests.get(
        f'https://travel.naver.com/overseas/{code}/city/topPoi/pshp', headers=headers)

    # main 정보 긁어오기
    soup_1 = BeautifulSoup(main.text, 'html.parser')

    destinations = soup_1.select(
        '#__next > div > div.mainContainer_content__Wz08H > div > main')

    for destination in destinations:
        country = destination.select_one(
            'div.commonGeoInfo_basic_information__2JoX_ > div.commonGeoInfo_geo__8ffvr > div > span > span:nth-child(1) > a')
        if country is not None:
            country = country.text
        city_kor = destination.select_one(
            'div.commonGeoInfo_basic_information__2JoX_ > strong')
        if city_kor is not None:
            city_kor = city_kor.text
        city_eng = destination.select_one(
            'div.commonGeoInfo_basic_information__2JoX_ > div.commonGeoInfo_foreign__1uqwq > span.english')
        if city_eng is not None:
            city_eng = city_eng.text
        desc = destination.select_one(
            'div.commonGeoInfo_basic_information__2JoX_ > div.commonGeoInfo_description__b675d > p > span')
        if desc is not None:
            desc = desc.text
        img_list = []
        pics = destination.select(
            'div.topImages_TopImages__30yhR > div > div > ul > li')
        for pic in pics:
            img = pic.select_one('a > div > img')
            img_list.append(img['src'])

        doc = {
            'city': [city_kor, city_eng],
            'country': country,
            'desc': desc,
            'img_url': img_list}
        db.travel.insert_one(doc)

    # 관광명소 정보 긁어오기
    soup_2 = BeautifulSoup(visit.text, 'html.parser')

    places = soup_2.select(
        '#__next > div > div.mainContainer_content__Wz08H > div > div > div.pc_items__38Tga > div.pc_PoiListPc__3rTLN > ul > li')

    site_names = []
    site_imgs = []
    for place in places:
        site = place.select_one(
            'div > div > div > a > div > span.topPoiItem_subject__VYLmJ > b')
        if site is not None:
            site_names.append(site.text)
        pic = place.select_one(
            'div > div > div > a > figure > img')
        site_imgs.append(pic['src'])

        db.travel.update_one(
            {'city': city_kor}, {'$set': {'site_names': site_names}})
        db.travel.update_one(
            {'city': city_kor}, {'$set': {'site_imgs': site_imgs}})

    # 맛집 정보 긁어오기
    soup_3 = BeautifulSoup(food.text, 'html.parser')

    dinning_places = soup_3.select(
        '#__next > div > div.mainContainer_content__Wz08H > div > div > div.pc_items__38Tga > div.pc_PoiListPc__3rTLN > ul > li')

    rest_names = []
    rest_imgs = []
    for dinning in dinning_places:
        rest = dinning.select_one(
            'div > div > div > a > div > span.topPoiItem_subject__VYLmJ > b')
        if rest is not None:
            rest_names.append(rest.text)
        rest_pic = dinning.select_one(
            'div > div > div > a > figure > img')
        rest_imgs.append(rest_pic['src'])

        db.travel.update_one(
            {'city': city_kor}, {'$set': {'rest_names': rest_names}})
        db.travel.update_one(
            {'city': city_kor}, {'$set': {'rest_imgs': rest_imgs}})

    # 쇼핑몰 정보 긁어오기
    soup_4 = BeautifulSoup(shopping.text, 'html.parser')

    shopping_places = soup_4.select(
        '#__next > div > div.mainContainer_content__Wz08H > div > div > div.pc_items__38Tga > div.pc_PoiListPc__3rTLN > ul > li')

    mall_names = []
    mall_imgs = []
    for shop in shopping_places:
        mall = shop.select_one(
            'div > div > div > a > div > span.topPoiItem_subject__VYLmJ > b')
        if mall is not None:
            mall_names.append(mall.text)
        mall_pic = shop.select_one(
            'div > div > div > a > figure > img')
        mall_imgs.append(mall_pic['src'])

        db.travel.update_one(
            {'city': city_kor}, {'$set': {'mall_names': mall_names}})
        db.travel.update_one(
            {'city': city_kor}, {'$set': {'mall_imgs': mall_imgs}})


db.travel.update_one(
    {'city': '루체른'}, {'$set': {'tag': ['유럽', '산', '도심', '역사유적', '미술관']}})
db.travel.update_one(
    {'city': '마드리드'}, {'$set': {'tag': ['유럽', '도심', '역사유적']}})
db.travel.update_one(
    {'city': '로마'}, {'$set': {'tag': ['유럽', '도심', '박물관', '미술관']}})
db.travel.update_one(
    {'city': '아테네'}, {'$set': {'tag': ['유럽', '산', '도심', '역사유적', '박물관']}})
db.travel.update_one(
    {'city': '파리'}, {'$set': {'tag': ['유럽', '도심', '역사유적', '박물관', '미술관']}})
db.travel.update_one(
    {'city': '하와이'}, {'$set': {'tag': ['아메리카', '바다', '쇼핑', '액티비티']}})
db.travel.update_one(
    {'city': '칸쿤'}, {'$set': {'tag': ['아메리카', '바다', '액티비티']}})
db.travel.update_one(
    {'city': '뉴욕'}, {'$set': {'tag': ['아메리카', '도심', '박물관', '미술관', '쇼핑']}})
db.travel.update_one(
    {'city': '몰디브'}, {'$set': {'tag': ['아시아', '바다']}})
db.travel.update_one({'name': '몰디브'}, {'$set': {'country': '몰디브'}})
db.travel.update_one(
    {'city': '발리'}, {'$set': {'tag': ['아시아', '바다', '산', '액티비티']}})
db.travel.update_one(
    {'city': '보라카이'}, {'$set': {'tag': ['아시아', '바다', '액티비티']}})
db.travel.update_one(
    {'city': '세부'}, {'$set': {'tag': ['아시아', '바다', '액티비티']}})
db.travel.update_one(
    {'city': '다낭'}, {'$set': {'tag': ['아시아', '바다', '역사유적', '접근성']}})

db.travel.update_one(
    {'city': '몰디브'}, {'$set': {'country': '몰디브'}})
