from django.urls import path
from .views import OrderList, OrderCreate, OrderDelete, OrderDetail, OrderUpdate, order_complete

app_name = 'ordersapp'

urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('reade/<int:pk>/', OrderDetail.as_view(), name='reade'),
    path('forming_complete/<int:pk>/', order_complete, name='forming_complete'),
]