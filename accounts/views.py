from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import uaauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import *
from .filters import OrderFilter


# Create your views here.
@uaauthenticated_user
def signUpPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password2"]
            
            login(request, user)
            # messages.success(
            #     request, f"Account Successfully Created for {username}")
            return redirect('home')
    context = {"form": form}
    return render(request, "accounts/sign_up.html", context)


@uaauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Incorrect Username or password")
    context = {}
    return render(request, "accounts/login.html", context)


@login_required(login_url='login')
@admin_only
def Home(request):
    orders = Order.objects.all().order_by("-date_created")
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {"orders": orders,
               "customers": customers,
               "total_customers": total_customers,
               "total_orders": total_orders,
               "delivered": delivered,
               "pending": pending}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer", "admin"])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,
               "total_orders": total_orders,
               "delivered": delivered,
               "pending":pending}
    return render(request, "accounts/user.html", context)



@login_required(login_url="login")
@allowed_users(allowed_roles=["customer", "admin"])
def accountSetttings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)


    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "accounts/account_settings.html", context)




@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def custumer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {"customer": customer,
               "orders": orders,
               "filter": my_filter,
               }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=7)
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={"customer": customer})
    form_set = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        form_set = OrderFormSet(request.POST, instance=customer)
        if form_set.is_valid():
            form_set.save()
            return redirect('home')

    context = {"form_set": form_set}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("home")

    context = {
        "item": order,
    }
    return render(request, "accounts/delete.html", context)


def logOut(request):
    logout(request)
    return redirect("login")
