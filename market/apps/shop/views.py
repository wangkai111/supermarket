from django.shortcuts import render, redirect

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


def shop_detail(request, id):  # 商品详情
    try:
        goods = Shop_SKU.objects.get(pk=id, is_shelf=True)
    except Shop_SKU.DoesNotExist:
        return redirect("shop:商城主页")
    context = {
        "goods": goods,
    }
    return render(request, 'shop/detail.html', context)


def shop_category(request, cate_id):  # 超市
    # 正向查询 多一方模型对象.关联属性
    # 逆向查询 少一方模型对象.多一方模型类_set
    # 进行判断的时候,需要将传入的cate_id转换成整数,因为商品分类里面取的id是整数
    try:
        cate_id = int(cate_id)
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
    sku = Shop_SKU.objects.filter(isDelete=False, is_shelf=True,sort_id_id=cate_id)
    context = {
        "sorts": sorts,
        "sku": sku,
        "cate_id": cate_id,
    }
    return render(request, 'shop/category.html', context)
