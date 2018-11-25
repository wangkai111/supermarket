from django.contrib import admin

from shop.models import Shop_sort, Shop_SPU, Unit, Shop_SKU, Shop_album, Lunbo, Active, Active_zone, Active_SKU


# 商品分类
@admin.register(Shop_sort)
class Shop_sortAdmin(admin.ModelAdmin):
    # 设置每页显示的条数
    list_per_page = 5

    # 自定义显示列
    list_display = ["id", "sort_name", "sort_introduction"]

    # 设置在列表页 字段上添加一个 a 标签,从而进入到编辑页面
    list_display_links = ["id", "sort_name"]

    # 列表右侧栏过滤器
    list_filter = ["sort_name"]

    # 搜索框, 用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
    search_fields = ["sort_name"]

    # 定义在添加或者编辑的时候 操作哪些字段
    # 第一种
    # fields = ["name","parent"]

    # 第二种
    fieldsets = (
        ('商品分类名', {'fields': ("sort_name",)}),
        ('商品分类简介', {'fields': ("sort_introduction",)}),
    )


# 商品SPU表
@admin.register(Shop_SPU)
class Shop_SPUAdmin(admin.ModelAdmin):
    # 设置每页显示的条数
    list_per_page = 5

    # 自定义显示列
    list_display = ["id", "spu_name", "spu_content"]

    # 设置在列表页 字段上添加一个 a 标签,从而进入到编辑页面
    list_display_links = ["id", "spu_name"]

    # 列表右侧栏过滤器
    list_filter = ["spu_name"]

    # 搜索框, 用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
    search_fields = ["spu_name"]

    # 定义在添加或者编辑的时候 操作哪些字段
    fieldsets = (
        ('商品SPU名称', {'fields': ("spu_name",)}),
        ('商品SPU详情', {'fields': ("spu_content",)}),
    )


# 商品单位表
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    # 设置每页显示的条数
    list_per_page = 5

    # 自定义显示列
    list_display = ["id", "unit_name"]

    # 设置在列表页 字段上添加一个 a 标签,从而进入到编辑页面
    list_display_links = ["id", "unit_name"]

    # 列表右侧栏过滤器
    list_filter = ["unit_name"]

    # 搜索框, 用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
    search_fields = ["unit_name"]

    # 定义在添加或者编辑的时候 操作哪些字段
    fieldsets = (
        ('单位名', {'fields': ("unit_name",)}),
    )


# 定义一个类, 关联对象
class Shop_albumAdminInline(admin.StackedInline):
    # 关联子对象
    model = Shop_album
    # 额外编辑子对象
    extra = 2

# 商品SKU表
@admin.register(Shop_SKU)
class Shop_SKUAdmin(admin.ModelAdmin):
    # 设置每页显示的条数
    # list_per_page = 5

    # 自定义显示列
    list_display = ["id", "sku_name", "sku_introduction", "sku_price","unit", "sku_stock", "sku_sale", "sku_logo",
                    "is_shelf"]

    # 设置在列表页 字段上添加一个 a 标签,从而进入到编辑页面
    list_display_links = ["id", "sku_name", "sku_price"]

    # 列表右侧栏过滤器
    list_filter = ["sku_name", "sku_price"]

    # 搜索框, 用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
    search_fields = ["sku_name", "sku_stock", "sku_sale", "is_shelf"]

    # 定义在添加或者编辑的时候 操作哪些字段
    fieldsets = (
        ('商品SKU名', {'fields': ("sku_name",)}),
        ('商品SKU简介', {'fields': ("sku_introduction",)}),
        ('商品SKU价格', {'fields': ("sku_price",)}),
        ('商品SKU库存', {'fields': ("sku_stock",)}),
        ('商品SKU销量', {'fields': ("sku_sale",)}),
        ('商品LOGO地址', {'fields': ("sku_address",)}),
        ('商品SKU是否上架', {'fields': ("is_shelf",)}),
        ('商品分类id', {'fields': ("sort_id",)}),
        ('商品SPUid', {'fields': ("spu_id",)}),
        ('单位', {'fields': ("unit",)}),
    )

    # 关联对象
    inlines = [
        Shop_albumAdminInline,
    ]


# 首页活动表
@admin.register(Active)
class ActiveAdmin(admin.ModelAdmin):
    # 设置每页显示的条数
    list_per_page = 5

    # 自定义显示列
    list_display = ["id", "active_name", "image_address"]

    # 设置在列表页 字段上添加一个 a 标签,从而进入到编辑页面
    list_display_links = ["id", "active_name"]

    # 列表右侧栏过滤器
    list_filter = ["active_name"]

    # 搜索框, 用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
    search_fields = ["active_name"]

    # 定义在添加或者编辑的时候 操作哪些字段
    fieldsets = (
        ('活动名称', {'fields': ("active_name",)}),
        ('图片地址', {'fields': ("image_address",)}),
        ('活动地址', {'fields': ("url_address",)}),
    )


class Active_SKUAdminInline(admin.StackedInline):
    # 关联子对象
    model = Active_SKU
    # 额外编辑子对象
    extra = 2


# 首页活动专区
@admin.register(Active_zone)
class Active_zoneAdmin(admin.ModelAdmin):
    # 设置每页显示的条数
    list_per_page = 5

    # 自定义显示列
    list_display = ["id", "zone_name", "zone_content"]

    # 设置在列表页 字段上添加一个 a 标签,从而进入到编辑页面
    list_display_links = ["id", "zone_name","zone_content"]

    # 列表右侧栏过滤器
    list_filter = ["zone_name"]

    # 搜索框, 用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
    search_fields = ["zone_name","zone_content","zone_order","is_shelf"]

    # 定义在添加或者编辑的时候 操作哪些字段
    fieldsets = (
        ('活动专区名称', {'fields': ("zone_name",)}),
        ('活动专区描述', {'fields': ("zone_content",)}),
        ('活动专区排序', {'fields': ("zone_order",)}),
        ('活动专区是否上架', {'fields': ("is_shelf",)}),
    )

    # 关联对象
    inlines = [
        Active_SKUAdminInline,
    ]

# 轮播活动表
@admin.register(Lunbo)
class LunboAdmin(admin.ModelAdmin):
    # 设置每页显示的条数
    list_per_page = 5

    # 自定义显示列
    list_display = ["id", "lunbo_name","lun_image"]

    # 设置在列表页 字段上添加一个 a 标签,从而进入到编辑页面
    list_display_links = ["id", "lunbo_name"]

    # 列表右侧栏过滤器
    list_filter = ["lunbo_name"]

    # 搜索框, 用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
    search_fields = ["lunbo_name"]

    # 定义在添加或者编辑的时候 操作哪些字段
    fieldsets = (
        ('轮播名称', {'fields': ("lunbo_name",)}),
        ('图片地址', {'fields': ("image_address",)}),
        ('轮播商品排序', {'fields': ("order",)}),
        ('商品SKUID', {'fields': ("sku_id",)}),
    )