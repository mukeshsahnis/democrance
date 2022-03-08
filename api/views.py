import datetime as dt
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from api.forms import PolicyForm, RegisterForm
from api.models import Customer, Policy
from api.utils import get_next_page


def index(request):
    if request.user.is_authenticated:
        return dash(request)
    return home(request)


def home(request):
    return render(request, "home.html")


@login_required
def dash(request):
    quotes = Policy.objects.filter(customer=request.user)
    return render(request, "dashboard.html", {"quotes": quotes})


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


def register(request):
    success_url = get_next_page(
        request.POST.get("next"), settings.LOGIN_REDIRECT_URL
    )

    # Redirect if already logged in
    if request.user.is_authenticated:
        if success_url == request.path:
            raise ValueError(
                "Redirection loop for authenticated user detected. Check that "
                "your redirection doesn't point to a register page."
            )
        return redirect(success_url)

    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():

            user = authenticate(
                username=form.cleaned_data["email2"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect(success_url)
            else:
                user = Customer.objects.create(
                    email=form.cleaned_data["email2"],
                    password=form.cleaned_data["password"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    dob=form.cleaned_data["dob"],
                )
                # login the user
                login(request, user)
                return redirect(success_url)
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


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
@login_required
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


# accept quote
# before changing the status of the policy
# we redirect user to the payment page
# after complition of payment changed the status of the policy to live
@login_required
def accept_quote(request):
    if request.method == "POST":
        quote_id = request.POST.get("quote_id")
        policy = Policy.objects.get(id=quote_id)
        policy.state = "live"
        policy.save()
        msg = "Quote accepted."
        messages.add_message(request, messages.SUCCESS, msg)
        return redirect("/")
    else:
        form = PolicyForm()
    return render(request, "create-new-quote.html", {"form": form})


def search_customers(request):
    search_term = request.GET.get("search_term", "")
    customers = Customer.objects.filter(
        Q(first_name__icontains=search_term)
        | Q(last_name__icontains=search_term)
        | Q(dob__icontains=search_term)
    )
    return render(
        request,
        "search-customers.html",
        {"search_term": search_term, "customers": customers},
    )
