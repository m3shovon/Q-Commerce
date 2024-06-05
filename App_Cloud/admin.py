from django.contrib import admin
from .models import Restaurant, FoodItem, MyUser, Table, BookingRecord, FoodOrder,RestaurantCategories
from import_export.admin import ImportExportModelAdmin
from .resources import FoodItemResource

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'min_price', 'max_price', 'tables', 'seats']

# class FoodAdmin(admin.ModelAdmin):
#     list_display = ['restaurant', 'title', 'price']

class FoodAdmin(ImportExportModelAdmin):
    resource_class = FoodItemResource
    list_display = ['restaurant', 'title', 'price']
    search_fields  = ('restaurant__name', 'title', 'price')

class detailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone']
class tablesAdmin(admin.ModelAdmin):
    list_display = ['id','restaurant', 'seats', 'booking_status']
class bookAdmin(admin.ModelAdmin):
    list_display = ['id','user','restaurant', 'table', 'timestamp']

class ordersAdmin(admin.ModelAdmin):
    list_display = ['id','item','user', 'bill', 'timestamp',"order_status"]

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MyUser, detailsAdmin)
admin.site.register(Table, tablesAdmin)
admin.site.register(BookingRecord, bookAdmin)
admin.site.register(FoodOrder, ordersAdmin)
admin.site.register(FoodItem, FoodAdmin)
admin.site.register(RestaurantCategories)

