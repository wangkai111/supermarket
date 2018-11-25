from django.conf.urls import url

from shop.views import shop_index, shop_city, shop_village, shop_tidings, shop_recharge, shop_yhq, shop_ygq, shop_speed, \
    shop_list, shop_detail, shop_category

urlpatterns = [
    url(r'^$',shop_index,name='商城主页'),
    url(r'^shop_city/$',shop_city,name='所在城市'),
    url(r'^shop_village/$',shop_village,name='所在学校'),
    url(r'^shop_tidings/$',shop_tidings,name='消息中心'),
    url(r'^shop_recharge/$',shop_recharge,name='充值'),
    url(r'^shop_yhq/$',shop_yhq,name='我的红包'),
    url(r'^shop_ygq/$',shop_ygq,name='过期红包'),
    url(r'^shop_speed/$',shop_speed,name='零食飞速'),
    url(r'^shop_list/$',shop_list,name='琳琅的店'),
    url(r'^shop_detail/(?P<id>\d+)/$',shop_detail,name='商品详情'),
    url(r'^shop_category/(?P<cate_id>\d+)/$',shop_category,name='超市'),
]