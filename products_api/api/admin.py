from django.contrib import admin

from api.models import Item, Lot, RelatedProduct, Session


class ItemAdmin(admin.ModelAdmin):
    list_display = ['db_id', 'code', 'type', 'created']
    search_fields = ['code', 'type']


class RelatedProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtin', 'trade_item_unit_descriptor', 'created']
    search_fields = ['id', 'item__code', 'gtin', 'trade_item_unit_descriptor']
    raw_id_fields = ['item']


class LotAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'bbd', 'created', 'modified', 'item']
    raw_id_fields = ['item', 'session']


class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_id', 'session_start_time', 'session_end_time', 'supplier_id', 'user_id', 'created']
    search_fields = ['session_id', 'supplier_id', 'user_id']


admin.site.register(Item, ItemAdmin)
admin.site.register(RelatedProduct, RelatedProductAdmin)
admin.site.register(Lot, LotAdmin)
admin.site.register(Session, SessionAdmin)
