from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from taggit.models import Tag
from .forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from userauth.models import Profile,ContactUs
from django.core import serializers
from django.db.models.signals import post_save


import calendar
from django. db. models. functions import ExtractMonth
from django.db.models import Count,Avg,Q


from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from paypal.standard.forms import PayPalPaymentsForm
from .models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,wishlist,Address


# Create your views here.
def index(request):
    products=Product.objects.filter(product_status="published",featured=True).order_by("-id")
    context={
        'products':products
    }
    return render(request,"base/index.html",context)


def product_list_view(request):
    products=Product.objects.filter(product_status="published")

    context={
        'products':products,
    }
    return render(request,"base/product_list.html",context)


def category_list_view(request):
    categories= Category.objects.all().annotate(product_count=Count("category"))

    context={
        'categories':categories
    }
    return render(request,"base/category-list.html",context)


def category_product_list_view(request,cid):
    category=Category.objects.get(cid=cid)
    products=Product.objects.filter(product_status="published",category=category)

    context={
        'category':category,
        'products':products
    }
    return render(request,"base/category-product-list.html",context)


def vendor_list_view(request):
    vendors=Vendor.objects.all()

    context={
        'vendors':vendors,
    }
    return render(request,"base/vendor-list.html",context)


def vendor_detail_view(request,vid):
    vendor=Vendor.objects.get(vid=vid)
    products=Product.objects.filter(vendor=vendor,product_status="published")

    context={
        'vendor':vendor,
        'products':products,
    }
    return render(request,"base/vendor-detail.html",context)



def product_detail_view(request,pid):
    product=Product.objects.get(pid=pid)
    #product=get_object_or_404(Product,pid=pid)

    products=Product.objects.filter(category=product.category).exclude(pid=pid)
    p_image=product.p_images.all()

    #getting all review
    reviews=ProductReview.objects.filter(product=product).order_by("-id")
    #getting average rating review(⚝)
    average_rating=ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    #product Review form
    review_form= ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count ()

    if user_review_count > 0:
        make_review =False

    context={
        'product':product,
        'p_image':p_image,
        'products':products,
        'reviews':reviews,
        'average_rating':average_rating,
        'review_form':review_form,
        'make_review':make_review,
    }
    return render(request,"base/product-detail.html",context)



def tag_list(request,tag_slug=None):

    products=Product.objects.filter(product_status="published",).order_by("-id")

    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        products=products.filter(tags__in=[tag])

    context={
        'products':products,
        'tag':tag,
    }
    return render(request,"base/tag.html",context)


def ajax_add_review(request,pid):
    try:
        product=Product.objects.get(pk=pid)
        user=request.user


        review=ProductReview.objects.create(
            user=user,
            product=product,
            review=request.POST['review'],
            rating=request.POST['rating'],
        )

        context={
            'user':user.username,
            'review':request.POST['review'],
            'rating':request.POST['rating'],
        }

        average_reviews=ProductReview.objects.filter(product=product).aggregate(rating=(Avg("rating")))

        return JsonResponse(
            {
                'bool':True,
                'context':context,
                'average_reviews':average_reviews,
                # 'review':review
            }
        )
    except ObjectDoesNotExist:  # Use ObjectDoesNotExist to handle the specific exception
        return JsonResponse({'bool': False, 'error': 'Product not found'})


# def search_view(request):
#     quary=request.GET['q']

#     products=Product.objects.filter(Q(title__icontains=quary)|Q(description_icontains=quary))

#     context={
#         'products':products,
#         'quary':quary,
#     }
#     return render(request,"base/search.html",context)


def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    context = {
        'products': products,
        'query': query,
    }

    return render(request, "base/search.html", context)



def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors=request.GET.getlist("vendor[]")

    min_price=request.GET['min_price']
    max_price=request.GET['max_price']

    products=Product.objects.filter(product_status="published").order_by("-id").distinct()

    products=products.filter(price__gte=min_price)
    products=products.filter(price__lte=max_price)

    if len(categories)>0:
        products=products.filter(category__id__in=categories).distinct()

    if len(vendors)>0:
        products=products.filter(vendor__id__in=vendors).distinct()
        
    data=render_to_string("base/async/product-list.html",{'products':products})
    return JsonResponse({"data":data})


#old code
# def add_to_cart(request):
#     cart_product={}

#     cart_product[str(request.GET['id'])] = {
#         'title':request.GET['title'],
#         'qty':request.GET['qty'],
#         'price':request.GET['price']
#     }

#     if 'cart_data_obj' in request.session:
#         if str(request.GET['id']) in request.session['cart_data_obj']:
#             cart_data=request.session['cart_data_obj']
#             cart_data[str(request.GET['id'])]['qty']=int(cart_product[str(request.GET['id'])]['qty'])
#             cart_data.update(cart_data)
#             request.session['cart_data_obj']=cart_data
#         else:
#             cart_data=request.session['cart_data_obj']
#             cart_data.update(cart_data)
#             request.session['cart_data_obj']=cart_data
    
#     else:
#         request.session['cart_data_obj']=cart_product
#     return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj'])})


def add_to_cart(request):
    cart_product = {}
    product_id = request.GET.get('id')
    product_qty = int(request.GET.get('qty'))
    product_title = request.GET.get('title')
    product_price = request.GET.get('price')
    product_pid = request.GET.get('pid')
    product_image = request.GET.get('image')



    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if product_id in cart_data:
            cart_data[product_id]['qty'] += product_qty
        else:
            cart_data[product_id] = {
                'title': product_title,
                'qty': product_qty,
                'price': product_price,
                'image':product_image,#add
                'pid':product_pid,#add
            }
        request.session['cart_data_obj'] = cart_data
    else:
        cart_product[product_id] = {
            'title': product_title,
            'qty': product_qty,
            'price': product_price,
            'image':product_image,#add
            'pid':product_pid,#add

        }
        request.session['cart_data_obj'] = cart_product

    total_cart_items = len(request.session['cart_data_obj'])

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': total_cart_items})




def cart_view(request):
    cart_total_amount=0
    
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            # cart_total_amount += int(item['qty']) * float(item['price'])
            if item.get('price') and item.get('qty'):
                try:
                    price = float(item['price'])
                    qty = int(item['qty'])
                    cart_total_amount += qty * price
                except ValueError:
                    # Handle the case where 'price' or 'qty' is not a valid number
                    pass
        return render(request,"base/cart.html",{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    else:
         messages.warning(request,"Your cart is empty")
         return redirect('index')



def delete_item_from_cart(request):
    product_id=str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            # cart_total_amount += int(item['qty']) * float(item['price'])
            if item.get('price') and item.get('qty'):
                try:
                    price = float(item['price'])
                    qty = int(item['qty'])
                    cart_total_amount += qty * price
                except ValueError:
                    # Handle the case where 'price' or 'qty' is not a valid number
                    pass
    context=render_to_string("base/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})




def update_cart(request):
    product_id=str(request.GET['id'])
    product_qty=request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty']=product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            # cart_total_amount += int(item['qty']) * float(item['price'])
            if item.get('price') and item.get('qty'):
                try:
                    price = float(item['price'])
                    qty = int(item['qty'])
                    cart_total_amount += qty * price
                except ValueError:
                    # Handle the case where 'price' or 'qty' is not a valid number
                    pass
    context=render_to_string("base/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})


@login_required
def checkout_view(request):
    cart_total_amount=0
    total_amount=0
    #checking if cart_data_obj session is exit or not
    if 'cart_data_obj' in request.session:
        #gatting total amound for paypal
        for product_id,item in request.session['cart_data_obj'].items():
            if item.get('price') and item.get('qty'):
                try:
                    price = float(item['price'])
                    qty = int(item['qty'])
                    total_amount += qty * price
                except ValueError:
                    # Handle the case where 'price' or 'qty' is not a valid number
                    pass
        
        #create order object
        order=CartOrder.objects.create(
            user=request.user,
            price=total_amount
        )

        #gatting total amount for cart
        for product_id,item in request.session['cart_data_obj'].items():
            if item.get('price') and item.get('qty'):
                try:
                    price = float(item['price'])
                    qty = int(item['qty'])
                    cart_total_amount += qty * price
                except ValueError:
                    # Handle the case where 'price' or 'qty' is not a valid number
                    pass
            cart_order_products=CartOrderItems.objects.create(
                    order=order,
                    invoice_no="INVOICE NO-" + str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty']) * float(item['price']),
                )    

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': 'Order item no-' + str(order.id),
        'invoice': 'INV-no-'+str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('payment-completed')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment-failed')),

    }
    # Form to render the paypal button
    payment_button_form = PayPalPaymentsForm(initial=paypal_dict)

    try:
        active_address=Address.objects.get(user=request.user,status=True)
    except:
        messages.warning(request,"You select multiple address please select one address")
        active_address=None

    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            # cart_total_amount += int(item['qty']) * float(item['price'])
            if item.get('price') and item.get('qty'):
                try:
                    price = float(item['price'])
                    qty = int(item['qty'])
                    cart_total_amount += qty * price
                except ValueError:
                    # Handle the case where 'price' or 'qty' is not a valid number
                    pass
    return render(request,"base/checkout.html",{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'payment_button_form':payment_button_form,'cart_total_amount':cart_total_amount,'active_address':active_address})


@login_required
def payment_completed_view(request):
    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            # cart_total_amount += int(item['qty']) * float(item['price'])
            if item.get('price') and item.get('qty'):
                try:
                    price = float(item['price'])
                    qty = int(item['qty'])
                    cart_total_amount += qty * price
                except ValueError:
                    # Handle the case where 'price' or 'qty' is not a valid number
                    pass
    # return render(request,"base/payment-completed.html")
    return render(request,"base/payment-completed.html",{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})


@login_required
def payment_failed(request):
    return render(request,"base/payment-failed.html")

@login_required
def coustomer_dashboard(request):
    orders_list=CartOrder.objects.filter(user=request.user).order_by("-id")
    address=Address.objects.filter(user=request.user)

    profile=Profile.objects.get(user=request.user)

    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month","count")
    month=[]
    total_orders=[]

    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    if request.method == "POST":
        address=request.POST.get("address")
        mobile=request.POST.get("mobile")
        new_address=Address.objects.create(
            user=request.user,
            # orders=orders,
            address=address,
            mobile=mobile,
        )
        messages.success(request,"Address modify successfully")
        return redirect('dashboard')
    context={
        'orders_list':orders_list,
        'address':address,
        'profile':profile,
        'orders':orders,
        'month':month,
        'total_orders':total_orders

    }
    return render(request,"base/dashboard.html",context)

@login_required
def order_detail(request,id):
    order=CartOrder.objects.get(user=request.user,id=id)
    order_items=CartOrderItems.objects.filter(order=order)
    context={
        'order_items':order_items
    }
    return render(request,"base/order-detail.html",context)




def make_address_default(request):
    id=request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})

@login_required
def wishlist_view(request):
    try:
        item_wishlist=wishlist.objects.filter(user=request.user)
    except:
        item_wishlist=None
    context={
        'item_wishlist':item_wishlist
    }
    return render(request,"base/wishlist.html",context)


def add_to_wishlist(request):
    product_id=request.GET['id']
    product=get_object_or_404(Product,id=product_id)
    

    contex={}

    wishlist_count=wishlist.objects.filter(product=product,user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        contex={
            "bool":True
        }
    else:
        new_wishlist=wishlist.objects.create(
            user=request.user,
            product=product,
            
        )
        contex={
            'bool':True
        }
    return JsonResponse(contex)



def remove_wishlist(request):
    pid=request.GET['id']
    # wishlist_item=get_object_or_404(wishlist,user=request.user,id=pid)
    wishlist_item=wishlist.objects.filter(user=request.user,id=pid)

    product=wishlist.objects.get(id=pid)
    del_product=product.delete()

    context={
        'bool':True,
        'wishlist_item':wishlist_item
    }
    wishlist_json=serializers.serialize('json',[wishlist_item])
    data=render_to_string("base/async/remove-wishlist.html",context)
    return JsonResponse({"data":data,'wishlist_item':wishlist_json})



def contact(request):
    return render(request,"base/contact.html")

def ajex_contact_form(request):
    full_name=request.GET['full_name']
    email=request.GET['email']
    phone=request.GET['phone']
    subject=request.GET['subject']
    message=request.GET['message']

    contact=ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    ),

       
    data={
        'bool':True,
        'message':"messhage send successfully"
    }

    return JsonResponse({"data":data})

