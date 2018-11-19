from django.shortcuts import render


def shop_index(request):    # 商城主页
    return render(request, "shop/index.html")
