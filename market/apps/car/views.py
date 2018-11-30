from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from db.base_view import BaseView
from shop.models import Shop_SKU


class AddShopCart(View):
    """添加购物车"""

    def get(self, request):
        pass

    """
    1.需要验证是否登录
    2.接收参数:购物车加入数量(count),当前商品id(sku_id)
    3.验证数据
        a.都必须是整数
        b.count必须大于0
        c.商品必须存在
        d.判断库存
    4.将选择的商品加入到redis中
    """

    def post(self, request):
        # 通过session获取用户id
        user_id = request.session.get("id")
        if user_id is None:
            # 没有登录,需要返回json对象提示
            return JsonResponse({"name": 1, "errmsg": "没有登录"})
        # 接收参数
        count = request.POST.get("count")
        sku_id = request.POST.get("sku_id")
        # 验证数据
        # a.都必须是整数
        try:
            count = int(count)
            sku_id = int(sku_id)
        except:
            return JsonResponse({"name": 2, "errmsg": "输入的不是整数"})
        # b.count必须大于0
        # if count <= 0:
        #     return JsonResponse({"name": 3, "errmsg": "参数错误"})
        # c.商品必须存在
        try:
            shop_sku = Shop_SKU.objects.get(pk=sku_id)
        except Shop_SKU.DoesNotExist:
            return JsonResponse({"name": 4, "errmsg": "参数错误"})
        # d.判断库存
        if shop_sku.sku_stock < count:
            return JsonResponse({"name": 5, "errmsg": "参数错误"})
        # 将得到的sku_id 和 count 保存到redis中
        # 连接redis
        r = get_redis_connection("default")
        # 使用哈希保存到redis中
        # 设置键,为了更安全,防止外来人员轻松获取到用户id
        cart_id = "cart_id_{}".format(user_id)
        sku_id_count = r.hincrby(cart_id, sku_id, count)

        # 判断当前sku_id中的数量,如果为0,就要从redis中删除
        if sku_id_count == 0:
            r.hdel(cart_id,sku_id)

        # 获取购物车中总数量
        car_count = 0
        car_values = r.hvals(cart_id)
        # print(car_values)
        # 遍历获取里面的值,里面的值是2进制格式,可以解码,也可以直接int转换
        for v in car_values:
            car_count += int(v)
        # 成功的话
        return JsonResponse({"name": 0, "car_count": car_count})


class ShopCart(BaseView):
    """购物车界面显示"""

    def get(self, request):
        """
        获取购物车中的商品信息
        sku_id ,count
        现获取sku_id ,再根据sku_id获取商品的信息
        计算总价格
        """
        # 连接redis数据库
        r = get_redis_connection("default")
        # 获取redis中的sku_id  和 count
        user_id = request.session.get("id")
        # 设置键,为了更安全,防止外来人员轻松获取到用户id
        cart_id = "cart_id_{}".format(user_id)
        # 获取到的该商品数据返回的是以字典的形式,里面的键是sku_id,值是count
        cart_data = r.hgetall(cart_id)

        # 创建一个列表,保存购物车里所有的商品
        skus = []
        # 字典取值,需要遍历
        for sku_id, count in cart_data.items():
            sku_id = int(sku_id)
            count = int(count)

            # 获取到该条商品的对象
            sku = Shop_SKU.objects.get(pk=sku_id)
            # 自定义属性,将商品数量保存到该条商品对象上
            sku.count = count
            # 将其中得到的一条商品添加到列表中
            skus.append(sku)
        # 渲染数据到页面上
        context = {
            "skus": skus,
        }
        return render(request, "car/shopcart.html", context)

    def post(self, request):
        pass
