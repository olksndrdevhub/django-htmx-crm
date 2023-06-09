
import time

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import CrmUser
from . import models
from .helpers import prepare_pagination

# Create your views here.
@login_required(login_url='accounts:auth')
@staff_member_required(login_url='accounts:auth')
def home_view(request):
    template_name = 'crm_home.html'
    products = models.Product.objects.all()
    orders = models.Order.objects.all()
    clients = CrmUser.objects.filter(is_client=True)

    context = {
        'products': products,
        'orders': orders,
        'orders_count': orders.count(),
        'products_total': products.count(),
        'products_out_of_stock_total': products.filter(availability=False).count(),
        'clients': clients,
        'clients_total': clients.count(),
    }
    return render(request, template_name, context)


def products_view(request):
    template_name = 'products.html'
    context = {}

    products = models.Product.objects.all()

    query = request.GET.get("search", None)
    if query:
        products = models.Product.objects.filter(title__icontains=query)

    if request.htmx:
        time.sleep(1)
        template_name = 'partials/products_table_body.html'

    page = request.GET.get('page', 1)
    products, total_products = prepare_pagination(products, page, 3)

    context["products"] = products
    context["total_products"] = total_products

    return render(request, template_name, context)


def hx_add_order(request):
    partial_template_name = 'partials/add_order_form.html'

    return render(request, partial_template_name)


def hx_add_client(request):
    partial_template_name = 'partials/add_client_form.html'
    clients = None
    context = {}

    if request.method == 'POST':
        partial_template_name = 'partials/clients_list.html'

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        new_client = CrmUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_client=True,
        )
        clients = CrmUser.objects.filter(is_client=True)
        context['clients'] = clients
        context['clients_total'] = clients.count()
        messages.add_message(request, messages.SUCCESS, 'New Client added!')

    return render(request, partial_template_name, context)


def hx_add_product(request):
    partial_template_name = 'partials/add_product_form.html'
    products = None
    context = {}

    if request.method == 'POST':
        partial_template_name = 'partials/products_list.html'

        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        availability = False
        if request.POST.get('availability') == 'True':
            availability = True

        models.Product.objects.create(
            title=title,
            price=price,
            description=description,
            availability=availability,
            created_by=request.user
        )
        products = models.Product.objects.all()
        total_products = products.count()
        if request.POST.get('page', False):
            partial_template_name = 'partials/products_table_body.html'
            products, total_products = prepare_pagination(query=products, items_per_page=3)

        context = {
            'products': products,
            'products_total': total_products
        }
        if not request.POST.get('page', False):
            context['products_out_of_stock_total'] = products.filter(availability=False).count()
        messages.add_message(request, messages.SUCCESS, 'New Product added!')

    return render(request, partial_template_name, context)


def hx_delete_product(request, id):
    try:
        product = models.Product.objects.get(id=id)
        product.delete()
        messages.add_message(request, messages.WARNING, 'Product successfully deleted!')
    except models.Product.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Product didn\'t exist...')
    partial_template_name = 'partials/products_table_body.html'
    products = models.Product.objects.all()
    products, total_products = prepare_pagination(query=products, items_per_page=3)

    context = {
        'products': products,
        'products_total': total_products
    }
    return render(request, partial_template_name, context)
