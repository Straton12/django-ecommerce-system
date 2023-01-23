from django.shortcuts import render
from django.views import View
from .models import *
from .forms import*
from  django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        else:
            totalitems=0
        context={'bottoms':bottomwears,'mobiles':mobiles,'laptops':laptops,'totalitems':totalitems}
        return render(request,'app/home.html',context)

class productDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(id=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        else:
            totalitems=0
        context={'product':product,'item_already_in_cart':item_already_in_cart,'totalitems':totalitems}
        return render(request, 'app/productdetail.html',context)
@login_required
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user =request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        else:
            totalitems=0
        if cart_product:
            for p in cart_product:
                tempamount = (p.quatity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
            context ={'carts':cart,'amount':amount,'total_amount':total_amount,'totalitems':totalitems}
            return render(request, 'app/addtocart.html',context)
        else:
             return render(request, 'app/emptycart.html')
    
def plus_cart(request):
    if request.method == 'GET':
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id,) & Q(user=request.user))
        c.quatity +=1
        c.save()
        amount = 0.0
 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        for pr in cart_product:
            tempamount = (pr.quatity * pr.product.discounted_price)
            amount = amount+tempamount
            
            
        data = {
            'quatity':c.quatity,
            'amount':amount,
            'totalamount':amount + 70.6
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id,) & Q(user=request.user))
        c.quatity -=1
        c.save()
        amount = 0.0
 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        for pr in cart_product:
            tempamount = (pr.quatity * pr.product.discounted_price)
            amount = amount+tempamount
            
            
        data = {
            'quatity':c.quatity,
            'amount':amount,
            'totalamount':amount + 70.6
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id,) & Q(user=request.user))
        c.delete()
        amount = 0.0
 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        for pr in cart_product:
            tempamount = (pr.quatity * pr.product.discounted_price)
            amount = amount+tempamount
            
            
        data = {
            'amount':amount,
            'totalamount':amount + 70.6
        }
        return JsonResponse(data)
    

def buy_now(request):
    return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    context = {'add':add,'totalitems':totalitems}
    return render(request, 'app/address.html',context)

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    context={'order_palced':op,'totalitems':totalitems}
    return render(request, 'app/orders.html',context)


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'iphone' or data == 'samsung':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below-30000':
        mobile = Product.objects.filter(category='M').filter(discounted_price__lt=30000)
    elif data == 'above-30000':
        mobile = Product.objects.filter(category='M').filter(discounted_price__gt=30000)
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    else:
        totalitems=0
    context={'mobile':mobile,'totalitems':totalitems}
    return render(request, 'app/mobile.html',context)

def laptop(request):
    laptop = Product.objects.filter(category='L')
    context={'laptop':laptop}
    return render(request, 'app/laptop.html',context)

def bottomwear(request):
    bottom = Product.objects.filter(category='BW')
    context={'bottom':bottom}
    return render(request, 'app/bottomwear.html',context)

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        context = {'form':form}
        return render(request, 'app/customerregistration.html',context)
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!!! you registered succesfully ')
        context = {'form':form}
        return render(request, 'app/customerregistration.html',context)
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount =70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    if cart_product:
        for p in cart_product:
            temamount=(p.quatity * p.product.discounted_price)
            amount +=temamount
        total_amount=amount+shipping_amount
    context={'add':add,'totalamount':total_amount,'cartitems':cart_items,'totalitems':totalitems}
    return render(request, 'app/checkout.html',context)

@login_required
def payment_done(request):
    user = request.user
    print("__________________________________________")
    custid=request.GET.get('custid')
    print("hello")
    print(custid)
    customer = Customer.objects.get(id=custid)
    print(customer)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quatity=c.quatity).save()
        c.delete()
    return redirect('orders')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form =CustomerProfileForm()
        context = {'form':form}
        return render(request,'app/profile.html',context)
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            redirect('/profile/')
            messages.success(request,'Congragulation !!! Profile updated successfully')
            reg =Customer
            form =CustomerProfileForm('')
        return render(request,'app/profile.html',context)