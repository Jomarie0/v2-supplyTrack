from django.shortcuts import render, redirect
from .models import Product, StockMovement
from .forms import ProductForm, StockMovementForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def inventory_list(request):
    products = Product.objects.all()
    form = ProductForm()
    movement_form = StockMovementForm()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(product_id=product_id)
                form = ProductForm(request.POST, instance=product)
            except Product.DoesNotExist:
                form = ProductForm(request.POST)  # fallback
        else:
            form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('inventory:inventory_list')

    context = {
        'products': products,
        'form': form,
        'movement_form': movement_form,
    }
    return render(request, 'inventory/inventory_list.html', context)


@csrf_exempt
def delete_products(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if ids:
            Product.objects.filter(id__in=ids).delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'no ids provided'}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)
