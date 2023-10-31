from .models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,wishlist,Address
from django.db.models import Max,Min
from django.contrib import messages

def default(request):
    categories=Category.objects.all()
    vendors=Vendor.objects.all()
    min_max_price=Product.objects.aggregate(Min("price"),Max("price"))

    try:
        wishlist_item=wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request,"Please login then you can accessing the wishlist!")
        wishlist_item=0


    try:
        address=Address.objects.get(user=request.user)
    except:
        address=None
    return{
        'categories':categories,
        'address':address,
        'vendors':vendors,
        'min_max_price':min_max_price,
        'wishlist_item':wishlist_item,
    }
