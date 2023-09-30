from django.contrib import admin
from .models import Stock, Category, StockHistory
from .forms import StockCreateForm
# Register your models here.

class StockCreateAdmin(admin.ModelAdmin):
    form = StockCreateForm
    list_display = ['category', 'item_name', 'quantity', 'issued_quantity', 'issued_by', 'issued_to', 'received_quantity', 'received_by', 'phone_number', 'created_by', 'reorder_level', 'last_updated', 'export_to_csv']
    list_filter = ['category']
    search_fields = ['category', 'item_name']
    
admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
admin.site.register(StockHistory)

