from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from shop.models import Shop_SKU, Shop_sort, Lunbo, Active, Active_zone


def shop_index(request):  # 商城主页
    # 查询轮播图
    luns = Lunbo.objects.filter(isDelete=False).order_by("order")

    # 查询活动表
    active = Active.objects.filter(isDelete=False)

    # 查询活动专区表
    act_zone = Active_zone.objects.filter(is_shelf=True, isDelete=False)
    context = {
        "luns": luns,
        "active": active,
        "act_zone": act_zone,
    }
    return render(request, "shop/index.html", context)


def shop_detail(request, id):  # 商品详情
    try:
        goods = Shop_SKU.objects.get(pk=id, is_shelf=True)
    except Shop_SKU.DoesNotExist:
        return redirect("shop:商城主页")
    context = {
        "goods": goods,
    }
    return render(request, 'shop/detail.html', context)


def shop_category(request, cate_id, order):
    """商品分类,超市"""
    # 正向查询 多一方模型对象.关联属性
    # 逆向查询 少一方模型对象.多一方模型类_set
    """自定义参数:
    综合    0
    销量降  1
    价格降  2
    价格升  3
    新品    4
    """
    # 进行判断的时候,需要将传入的cate_id转换成整数,因为商品分类里面取的id是整数
    try:
        cate_id = int(cate_id)
        order = int(order)
    except:
        return redirect("shop:超市")

    # 查询商品分类表 所有的分类
    sorts = Shop_sort.objects.filter(isDelete=False)
    # 查询一条
    sort = sorts.first()
    # 默认查询一条分类
    if cate_id == 0:
        cate_id = sort.pk

    # 查询商品sku表中 某个商品分类下的所有商品
    sku = Shop_SKU.objects.filter(isDelete=False, is_shelf=True, sort_id_id=cate_id)
    # 第一种方式查询综合,销量,价格,新品
    # if order == 0:
    #     sku = Shop_SKU.objects.filter(isDelete=False, is_shelf=True, sort_id_id=cate_id)
    # elif order == 1:
    #     sku = Shop_SKU.objects.filter(isDelete=False, is_shelf=True, sort_id_id=cate_id).order_by("sku_sale")
    # elif order == 2:
    #     sku = Shop_SKU.objects.filter(isDelete=False, is_shelf=True, sort_id_id=cate_id).order_by("sku_price")
    # elif order ==3:
    #     sku = Shop_SKU.objects.filter(isDelete=False, is_shelf=True, sort_id_id=cate_id).order_by("-sku_price")
    # elif order ==4:
    #     sku = Shop_SKU.objects.filter(isDelete=False, is_shelf=True, sort_id_id=cate_id).order_by("create_time")
    # 第二种,定义一个列表
    order_list = ["id", "-sku_sale", "sku_price", "-sku_price", "create_time"]
    try:
        # 取出其中一个的排列方式
        order_one = order_list[order]
    except:
        # 如果没有取到,就按照id来排
        order_one = order_list[0]
        order = 0
    # 把取到的其中一种方式传进去排序
    sku = sku.order_by(order_one)

    # 对页面进行分页
    # 设置页面显示几条数据
    pagesize = 1
    # 创建分页对象,显示页面展示2条数据格式
    paginator = Paginator(sku, pagesize)
    # 获取当前页
    now_page = request.GET.get('p', 1)

    try:
        # 获取当前页数据
        page = paginator.page(now_page)
    except PageNotAnInteger:
        # 判断传入的参数是字符串的时候,就显示第一页
        page = paginator.page(1)
        # 判断传入的参数是大于总页数的时候,就显示最后一页
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # 显示购物车的数量
    # 初始购物车数量为0
    car_count = 0
    # 获取到用户id
    user_id = request.session.get("id")
    if user_id:
        # 连接redis数据库
        r = get_redis_connection("default")
        # 设置键,获取cate_id
        cart_id = "cart_id_{}".format(user_id)
        # 从redis中取出商品的数量,hvals属性获取到的是一个列表
        car_values = r.hvals(cart_id)
        # print(car_values)
        # 遍历获取里面的值,里面的值是2进制格式,可以解码,也可以直接int转换
        for v in car_values:
            car_count += int(v)


    context = {
        "sorts": sorts,
        "sku": page,
        "cate_id": cate_id,
        "order": order,
        "car_count":car_count,
    }
    return render(request, 'shop/category.html', context)


def shop_city(request):  # 所在城市
    return render(request, "shop/city.html")


def shop_village(request):  # 所在学校
    return render(request, "shop/village.html")


def shop_tidings(request):  # 消息中心
    return render(request, "shop/tidings.html")


def shop_recharge(request):  # 充值界面
    return render(request, "shop/recharge.html")


def shop_yhq(request):  # 我的红包
    return render(request, 'shop/yhq.html')


def shop_ygq(request):  # 过期红包
    return render(request, "shop/ygq.html")


def shop_speed(request):  # 零食飞速
    return render(request, 'shop/speed.html')


def shop_list(request):  # 琳琅的店
    return render(request, 'shop/list.html')
