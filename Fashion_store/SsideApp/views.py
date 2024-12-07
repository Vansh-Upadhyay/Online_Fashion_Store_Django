from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from CsideApp.models import Order
from .models import Product, Category
from django.contrib import messages
import csv

    
def dashboard(request):
    fullname = request.session.get('fullname')
    return render(request, 'dashboard.html', {'fullname': fullname})

def manage_order(request):
    all_orders = Order.objects.all()
    return render(request, 'manage_order.html', {'orders': all_orders})

def productD(request):
    products = Product.objects.all()
    return render(request, 'productD.html', {'products': products})

def index(request):
    all_products = Product.objects.filter()[:4]
    pCat = Category.objects.all()[:3]
    return render(request, 'index.html', {'pCat': pCat, 'all_products': all_products})

def add_product(request):
    if request.method == "POST":
        itemName = request.POST['item_name']
        itemDescription = request.POST['item_description']
        itemPrice = request.POST['item_price']
        itemImage = request.FILES['item_image']
        category1 = request.POST['category']
        
        Product(itemName=itemName, itemDescription=itemDescription, 
                itemprice=itemPrice, item_image=itemImage, category_id=category1).save()
        
        messages.success(request, "Product added successfully.")
        return redirect('productD')
    
    messages.error(request, "Failed to add the product. Please try again.")
    return render(request, 'dashboard.html')

def delete_product(request, id):
    try:
        Product.objects.get(id=id).delete()
        messages.success(request, "Product deleted successfully.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    return redirect('productD')

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.itemName = request.POST['item_name']
        product.itemDescription = request.POST['item_description']
        product.itemprice = request.POST['item_price']
        product.category_id = request.POST['category']
        
        if 'item_image' in request.FILES:
            product.item_image = request.FILES['item_image']
        
        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('productD')
    
    return render(request, 'productD.html', {'product': product})

def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "The uploaded file is not a valid CSV file.")
            return redirect('productD')
        if csv_file.multiple_chunks():
            messages.error(request, 'Uploaded file is too big.')
            return redirect('productD')
        
        file_data = csv_file.read().decode('utf-8')
        lines = file_data.split("\n")
        c = len(lines)

        for i in range(1, c - 1):
            fields = lines[i].split(",")
            productName = fields[0]
            prductDes = fields[1]
            productPrice = fields[2]
            productImage = fields[3].strip()

            # Save the product
            Product(itemName=productName, itemDescription=prductDes, 
                    itemprice=productPrice, item_image=productImage.replace('\n', '').replace('\r', '')).save()

        messages.success(request, "Products uploaded successfully.")
    return redirect('productD')
