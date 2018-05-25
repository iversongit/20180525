from flask import Blueprint, render_template, session, jsonify, request
from sqlalchemy import or_

from user.models import User, House, Area, Facility, HouseImage, Order
from utils import status_code
from utils.functions import db
import re
import os

from utils.settings import UPLOAD_DIRS

house = Blueprint("house",__name__)

@house.route('/myhouse/')
def myhouse():
    return render_template("myhouse.html")


@house.route('/auth_myhouse/',methods=['GET'])
def auth_myhouse():
    user = User.query.get(session["user_id"])
    if user.id_card: # 用户已经实名认证
        # 返回房屋信息,按照房屋信息由新到旧排序
        houses = House.query.filter(House.user_id==user.id).order_by(House.id.desc())
        house_list = []
        for house in houses:
            house_list.append(house.to_dict())
        return jsonify(house_list=house_list,code=status_code.OK)
    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)

@house.route('/newhouse/',methods=['GET'])  # 发布新房源
def newhouse():
    return render_template("newhouse.html")

@house.route('/area_facility/',methods=['GET'])
def area_facility():
    areas = Area.query.all() # 获取所有的区域信息
    area_list = [area.to_dict() for area in areas]

    facilities = Facility.query.all() # 获取所有的设施信息
    facility_list = [facility.to_dict() for facility in facilities]

    return jsonify(area_list=area_list,facility_list=facility_list)

@house.route('/add_house/',methods=['POST'])
def add_house():
    house_dict = request.form
    # house_dict = request.form.to_dict() --> 将元组转换为字典
    # facility_ids = request.form.getlist('facility')
    title = house_dict.get('title')
    price = house_dict.get('price')
    area_id = house_dict.get('area_id')
    address = house_dict.get('address')
    room_count = house_dict.get('room_count')
    acreage = house_dict.get('acreage')
    unit = house_dict.get('unit')
    capacity = house_dict.get('capacity')
    beds = house_dict.get('beds')
    deposit = house_dict.get('deposit')
    min_days = house_dict.get('min_days')
    max_days = house_dict.get('max_days')
    facilities = house_dict.getlist('facility')

    user = User.query.get(session['user_id'])

    house = House()
    house.user_id = user.id
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    house.add_update()

    facility_list = []
    for facility in facilities:
        fac = Facility.query.get(facility)
        house.facilities.append(fac)
        facility_list.append(fac)
    db.session.add_all(facility_list)
    db.session.commit()
    return jsonify(code=status_code.OK,houseid=house.id)

    # if facility_ids:
    #     facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()
    #     house.facilities = facilities
    # try:
    #    house.add_update()
    # except Exception as e:
    #    return jsonify(status_code.DATABASE_ERROR)
    # return jsonify(code=status_code.OK,houseid=house.id)

@house.route('/add_picture/',methods=['POST'])
def add_picture():
    file_dict = request.files
    if 'house_image' in file_dict:
        f1 = file_dict['house_image']
        if not re.match(r'^image/.*$', f1.mimetype):  # mimetype:上传文件的类型
            return jsonify(status_code.MYHOUSE_UPLOAD_IMAGE_IS_ERROR)

        # 保存成功
        url = os.path.join(UPLOAD_DIRS, f1.filename) # 绝对地址
        f1.save(url)  # 保存图片到指定路径

        houseid = request.form.get('house_id')
        house = House.query.get(houseid)
        image_url = os.path.join('/static/upload', f1.filename) # 相对地址
        try:
            if not house.index_image_url:
                house.index_image_url = image_url
                house.add_update()
            house_image = HouseImage()
            house_image.house_id = houseid
            house_image.url = image_url
            house_image.add_update()
            return jsonify(code=status_code.OK, url=image_url)
            # return render_template("profile.html",url=image_url)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)

@house.route('/detail/',methods=["GET"])  # 一定要是methods 不能是method
def detail():
    # houseid = request.args.get('id')
    # house = House.query.get(houseid)
    # data = {
    #     'house':house,
    #     'code':status_code.OK
    # }
    print("i am in")
    return render_template("detail.html")

@house.route('/housedetail/',methods=['GET'])
def housedetail():
    houseid = request.args.get('id')
    house = House.query.get(houseid)
    booking = 1  # 判断房主还是游客
    if 'user_id' in session:
        if(house.user_id == session['user_id']):
            booking = 0
    return jsonify(code=status_code.OK,house=house.to_full_dict(),booking=booking)

@house.route('/booking/',methods=['GET'])
def booking():
    return render_template("booking.html")

@house.route('/index/',methods=['GET'])
def index():
    return render_template("index.html")

@house.route('/hindex/',methods=['GET'])
def hindex():
    user_name = ''
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        user_name = user.name
    houses = House.query.order_by(House.id.desc()).all()[:5]
    hlist = [house.to_dict() for house in houses]
    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   user_name=user_name,
                   hlist = hlist,
                   alist = alist)

@house.route('/search/',methods=['GET'])
def search():
    return render_template("search.html")

@house.route('/allsearch/',methods=['GET'])
def house_search():
    search_list = request.args
    area_id = search_list.get('aid')
    start_date = search_list.get('sd')
    end_date = search_list.get('ed')
    sort_key = search_list.get('sk')

    if sort_key:
        if sort_key == 'booking':
            sort_key = House.room_count.desc()
        elif sort_key == 'price-inc':
            sort_key = House.price.asc()
        elif sort_key == 'price-des':
            sort_key = House.price.desc()
        elif sort_key == 'new':
            sort_key = House.id.desc()
    else:
        sort_key = House.id.desc()

    houses = House.query.order_by(sort_key).filter(House.area_id == area_id)
    # houses = House.query.filter(House.area_id == area_id)
    # houses = houses.filter(House.area_id == area_id)
    # 对房屋进行处理
    order1 = Order.query.filter(Order.begin_date>=start_date,
                       Order.end_date<=end_date)
    order2 = Order.query.filter(Order.begin_date<=end_date,
                       Order.end_date>=end_date)
    order3= Order.query.filter(Order.begin_date<=start_date,
                       Order.end_date>=start_date)
    order4 = Order.query.filter(Order.begin_date<=start_date,
                       Order.end_date>=end_date)

    order_list1 = [o1.house_id for o1 in order1]
    order_list2 = [o2.house_id for o2 in order2]
    order_list3 = [o3.house_id for o3 in order3]
    order_list4 = [o4.house_id for o4 in order4]

    order_list = order_list1 + order_list2 + order_list3 + order_list4
    order_list = list(set(order_list))

    # orders = Order.query.filter(or_(Order.begin_date<=end_date,Order.end_date>=start_date))
    # order_list = [orders.house_id for order in orders]

    houses = houses.filter(House.id.notin_(order_list))
    hlist = [house.to_full_dict() for house in houses]


    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   hlist=hlist,
                   alist=alist)
