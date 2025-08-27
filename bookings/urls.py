from django.urls import path
from . import views

urlpatterns = [
    path("services/<int:pk>/book/", views.booking_form, name="booking_form"),
    path("mine/", views.my_bookings, name="my_bookings"),
    path("order-success/<int:booking_id>/", views.order_success, name="order_success"),
]
