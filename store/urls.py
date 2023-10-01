
from django.contrib import admin
from django.urls import path, include
from stock_mng import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    path('list_items/', views.list_items, name='list_items'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_items/<str:pk>', views.update_items, name='update_items'),
    path('delete_items/<str:pk>', views.delete_items, name='delete_items'),
    path('stock_detail/<str:pk>', views.stock_detail, name='stock_detail'),
    path('issued_items/<str:pk>', views.issued_items, name='issued_items'),
    path('received_items/<str:pk>', views.received_items, name='received_items'),
    path('reorder_level/<str:pk>', views.reorder_level, name='reorder_level'),
    path('list_history/', views.list_history, name='list_history'),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
