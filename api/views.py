import datetime as dt
import json

from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from api.models import Customer


@require_POST
@csrf_exempt
def create_customer(request):
    # Get customer data from request
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    dob = data.get("dob")
    dob = dt.datetime.strptime(dob, "%d-%m-%Y").date()

    # Create customer object
    customer = Customer.objects.create(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        dob=dob,
    )
    customer.save()

    # convert customer object to dict
    customer_dict = model_to_dict(
        customer, fields=["first_name", "last_name", "dob"]
    )
    # Return jsonResponse
    return JsonResponse(customer_dict)
