from cgi import test
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Cart,Product,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from indimart.settings import EMAIL_HOST_USER
import random

class ProductView(View):
 def get(self,request):
  totalitem=0
  topwears = Product.objects.filter(category = 'TW')
  bottomwears = Product.objects.filter(category = 'BW')
  mobiles = Product.objects.filter(category = 'M')
  laptops = Product.objects.filter(category ='L' )
  if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'totalitem':totalitem})


class ProductDetailView(View):
 def get(self,request,pk):
    totalitem=0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
      totalitem=len(Cart.objects.filter(user=request.user))
      item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/productdetail.html',
    {'product':product , 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem}) 
  
@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get("prod_id")
 product = Product.objects.get(id=product_id)
 Cart(user=user , product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 totalitem=0
 if request.user.is_authenticated:
  totalitem=len(Cart.objects.filter(user=request.user))
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempaamount = (p.quantity * p.product.discounted_price )
    amount += tempaamount
    total_amount = amount + shipping_amount
   return render(request, 'app/addtocart.html', {'carts':cart, 'total_amount':total_amount, 'amount':amount,'totalitem':totalitem})
  else:
   return render(request, 'app/emptycart.html')
   
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount=0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempaamount = (p.quantity * p.product.discounted_price )
    amount += tempaamount
    total_amount = amount + shipping_amount
    data = {
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':total_amount
    }
  return JsonResponse(data)
 



def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount=0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempaamount = (p.quantity * p.product.discounted_price )
    amount += tempaamount
    total_amount = amount + shipping_amount
    data = {
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':total_amount
    }
  return JsonResponse(data)


def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount=0.0
  shipping_amount = 70.0  
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempaamount = (p.quantity * p.product.discounted_price )
    amount += tempaamount
    total_amount = amount + shipping_amount
    data = {
      'amount':amount,
      'totalamount':total_amount
    }
  return JsonResponse(data,c)




def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 totalitem=0
 add= Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
 totalitem=0
 op = OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})


def mobile(request,data=None):
 totalitem=0
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'OnePlus' or data == 'IQOO' or data == "Realme" or data == 'Tecno_Phantom':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data4=None):
 totalitem=0
 if data4 == None:
  laptop = Product.objects.filter(category='L')
 elif data4 == 'Lenovo' or data4 == 'HP' or data4 == 'DELL' or data4 == "Apple" or data4 == 'Mi':
  laptop = Product.objects.filter(category='L').filter(brand=data4)
 if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/laptop.html',{'laptop':laptop,'totalitem':totalitem})

def bottomWear(request,data1=None):
 totalitem=0
 if data1 == None:
    bottomwears= Product.objects.filter(category='BW')
 elif data1 == 'Lycra' or data1 == 'Urbano' :
  bottomwears = Product.objects.filter(category='BW').filter(brand=data1)
 if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/bottomWear.html',{'bottomwears':bottomwears,'totalitem':totalitem})


def topWear(request,data2=None):
 totalitem=0
 if data2 == None:
    topwears= Product.objects.filter(category='TW')
 elif data2 == 'Lymio' or data2 == 'Raymond' :
  topwears = Product.objects.filter(category='TW').filter(brand=data2)
 if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/topWear.html',{'topwears':topwears,'totalitem':totalitem})

def VerifyOTP(request):
 userotp= request.POST.get('otp')
 otp = CustomerRegistrationView(otp)
 if userotp == otp:
  return redirect('login')


class CustomerRegistrationView(View):
 def get(self,request):
   form = CustomerRegistrationForm()
   return render(request, 'app/customerregistration.html', {'form':form})
 def post(self,request):
  email = request.POST.get('email')
  form =CustomerRegistrationForm(request.POST)
  if form.is_valid():
    otp=random.randint(100000, 999999)
    send_mail("User Data: ", f"Verify Your Email by the OTP: {otp}" , EMAIL_HOST_USER,[email],fail_silently=True)
    messages.success(request, 'Congratulation!! Registered Successfully')
    form.save()
    return render(request,'app/verify.html',{'otp':otp,'email':email})
  return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount = 70.0
 total_amount=0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
    for p in cart_product:
      tempaamount = (p.quantity * p.product.discounted_price )
      amount += tempaamount
    total_amount = amount + shipping_amount 
 return render(request, 'app/checkout.html', {'add':add ,'totalamount':total_amount , 'cart_items':cart_items})

@login_required
def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect("paymentcompleted")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  totalitem:0
  form = CustomerProfileForm()
  if request.user.is_authenticated:
   totalitem=len(Cart.objects.filter(user=request.user))
  return render(request,'app/profile.html',{'form':form, 'active':'btn-primary','totalitem':totalitem})
 
 def post(self,request):
  form =CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulation!! Profile Updated Successfully')
  return render(request,'app/profile.html',{'form':form , 'active':'btn-primary'})
 
def payment_completed_view(request):
 return render(request, 'app/payment-completed.html')
 
def payment_failed_view(request):
 return render(request, 'app/payment-failed.html')

def paymentCompleted(request):
 return render(request, 'app/paymentcompleted.html')
