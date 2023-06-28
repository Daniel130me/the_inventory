"""invent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from dashboard import views as dashboard_views
from customer import views as customer_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='user-register'),
    path('login/', user_views.signin, name='user-login'),
    path('', dashboard_views.index,  name='dashboard-index'),
    path('logout/', user_views.signout, name='user-logout'),
    path('profile/', user_views.profile, name='user-profile'),
    path('profile_update/', user_views.profile_update, name='user-profile_update'),
    path('product_form/', dashboard_views.product_form, name='dashboard-product_form'),
    path('profile_details/', user_views.profile_details, name='user-profile_details'),
    path('product/', dashboard_views.products, name='dashboard-products'),
    path('add_product/', dashboard_views.add_product, name='dashboard-add_product'),
    path('product_table/', dashboard_views.product_table, name='dashboard-product_table'),
    path('product_update/', dashboard_views.product_update, name='dashboard-product_update'),
    path('delete_product/', dashboard_views.delete_product, name='dashboard-delete_product'),
    path('delete_category/', dashboard_views.delete_category, name='dashboard-delete_category'),
    path('delete_order/', dashboard_views.delete_order, name='dashboard-delete_order'),
    path('category_details/', dashboard_views.category_details, name='dashboard-category_details'),
    path('add_category/', dashboard_views.add_category, name='dashboard-add_category'),
    path('edit_category/', dashboard_views.edit_category, name='dashboard-edit_category'),
    path('order/', dashboard_views.order, name='dashboard-order'),
    path('order_table/', dashboard_views.order_table, name='dashboard-order_table'),
    path('customer/', customer_views.customer, name='customer'),
    path('add_order_request/', customer_views.add_order_request, name='customer-add_order_request'),
    path('customer_order_table/', customer_views.customer_order_table, name='customer-customer_order_table'),
    path('change_order_status/', customer_views.change_order_status, name='customer-change_order_status'),
    path('user/', user_views.user, name='user-user'),
    path('user_table/', user_views.user_table, name='user-user_table'),
    path('send_data/', dashboard_views.send_data, name='user-send_data'),
    path('user/<int:pk>/',user_views.user_page, name='user-user_page' ),
    path('delete_user/', user_views.delete_user, name='user-delete_user'),
    path('user_update/', user_views.user_update, name='user-user_update'),
    path('add_staff/', user_views.add_staff, name='user-add_staff'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
