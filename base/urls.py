from django.urls import path,include
from .import views

urlpatterns = [
    #homepage
    path('',views.index,name="index"),

    path('category/',views.category_list_view,name="category-list"),

    #category
    path('products/',views.product_list_view,name="product-list"),
    path('category/<cid>/',views.category_product_list_view,name="category-product-list"),

    #vender
    path('vendors/',views.vendor_list_view,name="vendor-list"),
    path('vendor/<vid>/',views.vendor_detail_view,name="vendor-detail"),
    
    #product
    path('product/<pid>/',views.product_detail_view,name="product-detail"),
    #tags
    path('products/tag/<slug:tag_slug>/',views.tag_list,name="tags"),
    #add review
    path('ajax_add_review/<int:pid>/',views.ajax_add_review,name="ajax_add_review"),
    #searching
    path("search/",views.search_view, name="search"),
    #filter product url
    path('filter-products/',views.filter_product,name="filter-product"),
    #cart url
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    #cart page url
    path('cart/',views.cart_view,name="cart"),
    #delete item from cart
    path('delete-from-cart/',views.delete_item_from_cart,name="delete-from-cart"),
    #update cart
    path('update-cart/',views.update_cart,name="update-cart"),
    #checkout view
    path('checkout/',views.checkout_view,name="checkout"),
    #paypal url
    path('paypal/',include('paypal.standard.ipn.urls')),
    #paypal completed url
    path('payment-completed/',views.payment_completed_view,name="payment-completed"),
    #paypal faield
    path('payment-failed/',views.payment_failed,name="payment-failed"),
    #dashboard
    path('dashboard/',views.coustomer_dashboard,name="dashboard"),
    #order details url
    path('dashboard/order/<int:id>',views.order_detail,name="order-detail"),
    #making default address
    path('make-default-address/',views.make_address_default,name="make-default-address"),
    #wishlist page
    path('wishlist/',views.wishlist_view,name="wishlist"),
    #add to wishlist
    path('add-to-wishlist/',views.add_to_wishlist,name="add-to-wishlist"),
    #remove to wishlist
    path('remove-from-wishlist/',views.remove_wishlist,name="remove-from-wishlist"),
    #create a contact page for user
    path('contact/',views.contact,name="contact"),
    #add contact form to ajax
    path('ajax-contact-form/',views.ajex_contact_form,name="ajax-contact-form"),


]
