from django.shortcuts import render, redirect
from django.http import JsonResponse
from dashboard.models import Product, Order
from dashboard.forms import OrderForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='user-login')
def customer(request):
    if not request.user.is_authenticated:
        return redirect('user-login')
    else:
        if request.user.is_staff:
            return redirect('dashboard-index')
        products = Product.objects.values('id','name').order_by('name')
        context = {
            'products':products,
        }
        return render(request, 'customer/customer.html',context)


def add_order_request(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = 'Pending'
            instance.ordered_by = request.user
            instance.save()
            return JsonResponse({'pg':['customer_order_table'],'message':'success','info':'Added succesfully'})
        else:
            list_of_error = []
            for field, errors in form.errors.items():
                for error in errors:
                    list_of_error.append(error)
            return JsonResponse({'message':'.', 'info':list_of_error})

def customer_order_table(request):
    orders = Order.objects.values('id','quantity','status','created_at','updated_at','product_id_id','product_id__name','product_id__image','product_id__category__category_name','ordered_by_id','ordered_by__first_name','ordered_by__last_name').filter(ordered_by_id = request.user.id).order_by('-created_at')
    for order in orders:
        order['product_id__image'] = order['product_id__image'].split("/")[-1] 
    return render(request, 'customer/customer_order_table.html',{'orders':orders})

def change_order_status(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        status = request.POST.get('status')
        if status != 'Canceled':
            status = 'Pending'
        order = Order.objects.get(id=id)
        order.status = status
        order.save()
        return JsonResponse({'message':'success'})      