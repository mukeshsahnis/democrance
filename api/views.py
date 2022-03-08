import datetime as dt
import json

from django.contrib import messages
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from api.forms import PolicyForm
from api.models import Customer, Policy


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


@require_POST
@csrf_exempt
def quote(request):
    # Get quote data from request
    data = json.loads(request.body)
    customer_id = data.get("customer_id")
    type = data.get("type")
    premium = data.get("premium")
    cover = data.get("cover")
    state = data.get("state")

    # Create policy object
    policy = Policy(
        customer_id=customer_id,
        type=type,
        premium=premium,
        cover=cover,
        state=state,
    )
    policy.save()

    # convert policy object to dict
    policy_dict = model_to_dict(policy)
    # Return jsonResponse
    return JsonResponse(policy_dict)


# create policy through PolicyForm
def create_quote(request):
    if request.method == "POST":
        form = PolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.customer = request.user
            policy.save()
            msg = "Thanks for your submission."
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect("/")
    else:
        form = PolicyForm()
    return render(request, "create-new-quote.html", {"form": form})
