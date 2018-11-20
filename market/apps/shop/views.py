from django.shortcuts import render


def shop_index(request):  # 商城主页
    return render(request, "shop/index.html")


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


def shop_speed(request):    # 零食飞速
    return render(request,'shop/speed.html')


def shop_list(request):     # 琳琅的店
    return render(request,'shop/list.html')


def shop_detail(request):   # 商品详情
    return render(request,'shop/detail.html')


def shop_category(request):    # 超市
    return render(request,'shop/category.html')
