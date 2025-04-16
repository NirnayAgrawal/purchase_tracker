from django.shortcuts import render, redirect
import pandas as pd
from .models import Item
from django.utils import timezone
from .models import Purchase, Item
from datetime import date
from .models import Item, ItemUpload
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import openpyxl
import openpyxl
from openpyxl.styles import Font

def export_purchases_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Today's Purchases"

    ws.append(["Item Name", "Supplier", "Quantity"])
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for p in Purchase.objects.filter(date=date.today()):
        ws.append([p.item.name, p.item.supplier, p.quantity])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=today_purchases.xlsx'
    wb.save(response)
    return response


def delete_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase.delete()
    return redirect('item-list')

def edit_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    if request.method == 'POST':
        new_qty = request.POST.get('quantity')
        if new_qty:
            purchase.quantity = new_qty
            purchase.save()git add .
        return redirect('item-list')

def upload_items(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        upload = ItemUpload.objects.create()  # 👈 New upload instance

        for _, row in df.iterrows():
            Item.objects.get_or_create(
                name=row['Item Name'],
                supplier=row['Supplier'],
                upload=upload  # 👈 Link item to this upload
            )

        return redirect('item-list')  # Go to homepage after upload

    return render(request, 'tracker/upload.html')


def item_list(request):
    query = request.GET.get('q', '')
    
    latest_upload = ItemUpload.objects.order_by('-uploaded_at').first()
    items = Item.objects.none()

    if latest_upload:
        items = Item.objects.filter(name__icontains=query, upload=latest_upload)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')

        if item_id and quantity:
            item = Item.objects.get(id=item_id)
            Purchase.objects.create(item=item, quantity=quantity)
        return redirect('item-list')

    today_purchases = Purchase.objects.filter(date=date.today())

    return render(request, 'tracker/item_list.html', {
        'items': items,
        'query': query,
        'today_purchases': today_purchases
    })

