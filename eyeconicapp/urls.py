from django.urls import path
from .import views

urlpatterns =[
    path('',views.home,name="home"),
    path('admin_login',views.admin_login,name='admin_login'),
    path('alog/',views.alog,name='alog'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('add_product/',views.add_product,name='add_product'),
    path('product_list/',views.product_list,name='product_list'),
    path('add',views.add,name='add'),
    path('update_product/<int:id>/',views.update_product,name="update_product"),
    path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('register/',views.user_register,name='user_register'),
    path('user_login',views.user_login,name='user_login'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart_page,name='cart_page'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:product_id>/', views.checkout, name='buy_now'),
    path('order-success/<str:order_ids>/', views.order_success, name='order_success'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('support/', views.support, name='support'),
    path('admin_reports/', views.admin_reports, name='admin_reports'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]





    


    

