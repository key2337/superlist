from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    
    # 统一改成复数形式 items
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})