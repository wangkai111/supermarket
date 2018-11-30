from django.shortcuts import render

from db.base_view import BaseView


class TrueOrder(BaseView):
    """确认订单"""

    def get(self, request):
        # 获取用户id
        user_id = request.session.get("id")
        return render(request, "order/tureorder.html")

    def post(self, request):
        pass


class Order(BaseView):
    """确认订单"""

    def get(self, request):
        return render(request, "order/order.html")

    def post(self, request):
        pass
