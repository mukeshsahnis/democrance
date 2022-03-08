from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path(
        "v1/create_customer/",
        views.create_customer,
        name="create_customer",
    ),
    path("v1/quote/", views.quote, name="quote"),
    path("v1/quote/create/", views.create_quote, name="create_quote"),
    path("v1/quote/accept/", views.accept_quote, name="accept_quote"),
    path(
        "v1/quote/search_customers/",
        views.search_customers,
        name="search_customers",
    ),
    path("dash/", views.dash, name="dash"),
]
