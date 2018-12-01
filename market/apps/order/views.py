from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from db.base_view import BaseView
from order.models import Transport, Order, OrderGoods
from shop.models import Shop_SKU
from user.help import verify_login_required
from user.models import Address
from django_redis import get_redis_connection
from datetime import datetime
import random
from alipay import AliPay
import os
from django.conf import settings
import time


class TrueOrder(View):
    """确认订单"""

    def get(self, request):
        # 获取用户id
        user_id = request.session.get("id")
        # 判断用户是否登录
        if user_id is None:
            return redirect("user:登录")
        # 获取到购物车中所有商品
        sku_ids = request.GET.getlist("sku_id")
        # 获取到整数商品id
        sku_ids = [int(sku_id) for sku_id in sku_ids]
        # 设置商品初始化为空列表
        skus = []
        try:
            # 获取到收货地址
            address = Address.objects.filter(userid_id=user_id).order_by("-isDefault").first()
        except Address.DoesNotExist:
            return redirect("car:购物车界面")
        # 连接redis
        r = get_redis_connection("default")
        # 设置键
        cart_id = "cart_id_{}".format(user_id)
        # 设置一个价格列表
        total_price = 0
        # 获取到一个商品的信息
        for sku_id in sku_ids:
            # 第一种
            # try:
            #     sku_id = int(sku_id)
            # except:
            #     return redirect("shop:超市")
            # 第二种
            try:
                # 查询出商品对象
                sku = Shop_SKU.objects.get(pk=sku_id)
            except Shop_SKU.DoesNotExist:
                return redirect("shop:超市")

            # 获取购物车中商品的数量
            count = r.hget(cart_id, sku_id)
            try:
                count = int(count)
            except:
                return redirect("shop:超市")

            # 将每个商品的数量加入到商品对象上
            sku.count = count
            # 计算总价
            total_price += sku.sku_price * count

            # 将查询出来的商品都添加到列表中
            skus.append(sku)

        # 处理运输方式
        transport = Transport.objects.filter(isDelete=False).order_by("tran_price")
        # 渲染页面
        context = {
            "address": address,
            "skus": skus,
            "total_price": total_price,
            "transport": transport,
        }
        return render(request, "order/tureorder.html", context)

    @transaction.atomic
    def post(self, request):
        # 获取用户id
        user_id = request.session.get("id")
        # 判断用户是否登录
        if user_id is None:
            return JsonResponse({"name": 1, "err": "没有登录!"})
        # 接收参数
        address_id = request.POST.get("address_id")
        sku_ids = request.POST.getlist("sku_id")
        transport = request.POST.get("transport")

        # 判断是否都接收到
        if not all([address_id, sku_ids, transport]):
            return JsonResponse({"name": 2, "err": "参数错误"})

        # 转为整数
        try:
            address_id = int(address_id)
            transport = int(transport)
            sku_ids_int = [int(sku_id) for sku_id in sku_ids]
        except:
            return JsonResponse({"name": 3, "err": "参数错误"})

        # 判断收货地址是否存在
        try:
            address = Address.objects.get(pk=address_id, isDelete=False)
        except Address.DoesNotExist:
            return JsonResponse({"name": 4, "err": "收货地址不存在"})

        # 判断运输方式是否存在
        try:
            trans = Transport.objects.get(pk=transport, isDelete=False)
        except Transport.DoesNotExist:
            return JsonResponse({"name": 5, "err": "运输方式不存在"})

        # 保存数据到订单信息表中
        # 创建一个订单编号
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randint(10000, 99999))
        # 得到收货地址
        addresses = "{}{}{}{}".format(address.hcity, address.hproper, address.harea, address.detail)

        # 自己控制事务
        sid = transaction.savepoint()

        # 创建一个订单信息表对象
        order = Order.objects.create(
            order_sn=order_sn,
            user_id=user_id,
            username=address.username,
            telephone=address.telephone,
            address=addresses,
            transport=trans.tran_name,
            transport_price=trans.tran_price
        )

        # 连接redis
        r = get_redis_connection("default")
        # 设置键
        cart_id = "cart_id_{}".format(user_id)

        # 计算商品总价格
        order_amount = 0
        # 获取到商品id对象
        for sku_id in sku_ids_int:
            try:
                skus = Shop_SKU.objects.select_for_update().get(pk=sku_id, isDelete=False)
            except Shop_SKU.DoesNotExist:
                # 回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({"name": 6, "err": "商品不存在"})

            # 获取购物车中那个的数量
            count = r.hget(cart_id, sku_id)
            count = int(count)

            # 保存库存足够
            if skus.sku_stock < count:
                # 回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({"name": 7, "err": "库存不足"})

            # 保存数据到订单商品表中
            OrderGoods.objects.create(
                goods_sku=skus,
                order=order,
                count=count,
                price=skus.sku_price
            )

            # 销量增加
            skus.sku_sale += count
            # 库存减少
            skus.sku_stock -= count
            # 商品保存
            skus.save()

            # 统计总价格
            order_amount += skus.sku_price * count

        # 计算实付总金额
        try:
            order.order_amount = order_amount
            order.save()
        except:
            # 回滚
            transaction.savepoint_rollback(sid)
            return JsonResponse({"name": 8, "err": "保存实付总金额失败"})

        # 都成功,删除购物车中的数据
        r.hdel(cart_id, *sku_ids_int)

        # 提交事务
        transaction.savepoint_commit(sid)

        # 成功后跳转到订单支付页面
        return JsonResponse({"name": 0, "msg": "创建订单成功", "order_sn": order_sn})


class OrderShow(BaseView):
    """确认支付页面(显示订单信息)"""

    def get(self, request):
        # 获取用户id
        user_id = request.session.get("id")
        # 获取订单编号
        order_sn = request.GET.get("order_sn")
        try:
            # 通过订单编号查询订单信息
            order = Order.objects.get(order_sn=order_sn, user=user_id)
        except Order.DoesNotExist:
            return redirect("shop:商城主页")

        total_price = order.order_amount + order.transport_price
        # 渲染页面
        context = {
            "order": order,
            "total_price": total_price,
        }
        return render(request, "order/order.html", context)

    def post(self, request):
        pass


@verify_login_required
def pay(request):
    """发起支付"""
    # 接收参数
    order_sn = request.GET.get("order_sn")
    if order_sn is None:
        return redirect("shop:商城主页")

    # 获取用户id
    user_id = request.session.get("id")

    # 查询订单信息
    try:
        order = Order.objects.get(order_sn=order_sn, user_id=user_id, status=0)
    except Order.DoesNotExist:
        return redirect("shop:商城主页")

    # 订单总金额
    total = order.order_amount + order.transport_price

    # 订单描述
    brief = "王凯开的电商超市"

    # 发起支付,生成一个支付地址,跳转到支付宝地址上
    app_private_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/private_key.txt")).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/ali_public_key.txt")).read()

    # 创建对象
    alipay = AliPay(
        appid="2016092300577304",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 发起支付
    # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order.order_sn,  # 订单号
        total_amount=str(total),  # 总金额
        subject=brief,  # 订单描述信息
        return_url="http://127.0.0.1:8000/order/success/",
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 跳转到支付链接
    # return HttpResponse("https://openapi.alipaydev.com/gateway.do?{}".format(order_string))
    return redirect("https://openapi.alipaydev.com/gateway.do?{}".format(order_string))


@verify_login_required
def success(request):
    """支付成功"""
    # 发起一次支付查询,查看是否支付成功
    # 发起支付,生成一个支付地址,跳转到支付宝地址上
    app_private_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/private_key.txt")).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/ali_public_key.txt")).read()

    # 创建对象
    alipay = AliPay(
        appid="2016092300577304",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 获取out_trade_no参数
    out_trade_no = request.GET.get("out_trade_no")
    # 获取用户id
    user_id = request.session.get("id")

    # check order status
    paid = False
    for i in range(4):
        result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            break
        else:
            time.sleep(3)
    if paid is False:
        # 支付失败
        context = {
            "message": "支付失败"
        }
    else:
        # 支付成功
        Order.objects.filter(user_id=user_id, order_sn=out_trade_no).update(status=1)
        context = {
            "message": "支付成功"
        }

    # 支付成功后返回的页面
    return render(request, "order/pay.html", context)
