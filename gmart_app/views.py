from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Product, OrderItem, Order, Department
import os, requests, datetime

# Initialize variables
dept_list = Department.objects.all()
specials_img_path='media/site_header_specials/'  # Path for carousel images
specials_img_list =os.listdir(specials_img_path)
cart_quantity = 0


def index(request):
    if request.user.is_authenticated:
        print("Logged in")
    else:
        print("Not logged in")

# The HomeView class inherits from the ListView class, allowing products to be displayed in list format, filtered by department.
class HomeView(ListView):
    model = Product
    template_name = "gmart_app/home.html"

    # Get Products
    def get_queryset(self):

        # Assume no Department was selected and get all Products
        queryset = Product.objects.all()
        dept_id = self.request.GET.get("dept")
        
        # Filter Products by Department if a Department was selected
        if dept_id:
            queryset = queryset.filter(Product_Department = dept_id)
        return queryset

    # Pass along each Context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['img_specials'] = specials_img_list
        context['departments'] = dept_list
        context['cart_count'] = cart_quantity
        return context

# The OrderItemView inherits from the ListView class, which displays cart contents for the current user
class OrderItemView(ListView):
#if user is authenticated, then show their cart contents (get their rescent non-filled order's order_id to filter the order_item queryset)
    def get_queryset(self):
        template_name = "gmart_app/orderitem_list.html"
        if self.request.user.is_authenticated:
            if Order.objects.filter(Order_User=self.request.user, Order_Ordered=False).exists():
                # Return cart items
                cart_id = Order.objects.filter(Order_User=self.request.user, Order_Ordered=False)[0]
                queryset = OrderItem.objects.all().filter(OrderItem_Order_id = cart_id)
                self.cart_total = 0
                for prod in queryset:
                    prod.OrderItem_Total = prod.OrderItem_Quantity * prod.OrderItem_Product.Product_Price
                    self.cart_total += prod.OrderItem_Total
                if queryset.count() == 0:
                    messages.info(self.request, "Your cart is empty.")
            else:
                # Cart empty
                messages.info(self.request, "Your cart is empty.")
                queryset = OrderItem.objects.none()
        else:
            # User not logged in
            messages.info(self.request, "You must be logged in to access your cart.")
            queryset = OrderItem.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_total'] = self.cart_total
        return context


# The ProductDetailView inherits from DetailView. 
# It provides product detail for a single product, using the product_detail.html page.
class ProductDetailView(DetailView):
    model = Product
    template_name = "gmart_app/product_detail.html"


# The about function displays the about.html page
def about(request):
    context = {}
    context['img_specials'] = specials_img_list
    return render(request, 'gmart_app/about.html', context)


# This function adds a specified quantity of a single product to the user's order
def add_to_cart(request, pk, addQty):
    if request.user.is_authenticated:
        # Get the selected product, using the pk passed into the function.
        selected_product = get_object_or_404(Product, id=pk)
        # Determine whether the cart already has an open order.
        if Order.objects.filter(Order_User=request.user, Order_Ordered=False).exists():
            cart_order = Order.objects.filter(Order_User=request.user, Order_Ordered=False)[0]
            # Determine whether the product is already in the cart.
            if OrderItem.objects.filter(OrderItem_Product=selected_product, OrderItem_Order=cart_order).exists():
                # Item alread in cart, add another by incrementing the quantity.
                cart_order_item = OrderItem.objects.get(OrderItem_Product=selected_product, OrderItem_Order=cart_order)
                cart_order_item.OrderItem_Quantity += addQty
                cart_order_item.save()
                messages.info(request, '%s added to your cart: %s' % (addQty, selected_product.Product_Name))
            else:
                # Item not in cart.  Create one.
                cart_order_item  = OrderItem.objects.create(OrderItem_Product=selected_product, OrderItem_Order=cart_order, OrderItem_Quantity=addQty)
                messages.info(request, '"%s" has been added to your cart.' % selected_product.Product_Name)
        else:
            # Create a new order and create a new item in the order
            new_order = Order.objects.create(Order_User=request.user, Order_Date=datetime.datetime.now())
            new_order_item = OrderItem.objects.create(OrderItem_Product=selected_product, OrderItem_Order=new_order, OrderItem_Quantity=addQty)
            messages.info(request, "This item has been added to your cart.")
        return redirect("gmart-product-detail", pk)
    else:
        messages.info(request, "This site is for members only.  Please login or register a new account.")
        return redirect("login")


# This function removes all quantities of a selected item from the cart.
def remove_from_cart(request, pk, cart):
    # There is no code in this function to maintain the cart's item count.  
        # Instead, there's a custom template tag to display the cart's item count... 
        # see cart_template_tags.py for details
    if OrderItem.objects.filter(pk = pk).exists():
        remove_item = OrderItem.objects.get(pk = pk).OrderItem_Product.Product_Name
        OrderItem.objects.get(pk = pk).delete()
        messages.info(request, '"%s" removed from cart.' % remove_item)
    else:
        messages.info(request, "Item not removed:  There was no matching item to remove from your cart.")
    return redirect("gmart-cart", cart)

