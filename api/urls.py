from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path(
        "v1/create_customer/",
        views.create_customer,
        name="create_customer",
    ),
    path("vi/quote/", views.quote, name="quote"),
]
