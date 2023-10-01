from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv 
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# from simple_history.models import HistoricalRecords
# Create your views here.

def home(request):
    return redirect('/list_items')
    

@login_required
def list_items(request):
    header = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {'header': header,
               'queryset': queryset,
               'form': form,
               }
    if request.method == 'POST':
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value(),)
        
    if form['export_to_csv'].value() == True:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = "List of stock.csv"'
        writer = csv.writer(response)
        writer.writerow(['CATEGORY', 'ITEM_NAME', 'QUANTITY', 'REORDER_LEVEL', 'TIMESTAMP',
                  'LAST_UPDATED'])
        instance = queryset
        for stock in instance:
            writer.writerow([stock.category, stock.item_name, stock.quantity, stock.reorder_level,
                            stock.timestamp, stock.last_updated])
        return response
    return render(request, 'list_items.html', context)


def contact(request):
    header = 'Contact us'
    body = ' Contact us at '
    context = {'header': header,
               'body': body,
               }
    return render(request, 'contact.html', context)


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    header = 'Add New Item in Stock:'
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {'header': header,
               'form': form,
               }
    return render(request, 'add_items.html', context)


def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('/list_items')
    context = {
        'form': form,
    }
    return render(request, 'add_items.html', context)


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'delete_items.html')


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        'title': queryset.item_name,
        'queryset': queryset,
    }
    return render(request, 'stock_detail.html', context)




def issued_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
        
    if form.is_valid():
        instance = form.save(commit=False)
        instance.received_quantity = 0
        instance.quantity -= instance.issued_quantity
            
        # Set the issued_to field to what is entered in the form
        issued_to = form.cleaned_data.get('issued_to')
        instance.issued_to = issued_to

        messages.success(request, 'Successfully Issued Items! ' + str(instance.quantity) + ' ' + str(instance.item_name) + 's now left in Store')
        instance.save()
        return redirect('/stock_detail/' + str(instance.id))
        
    context = {
        'title': 'Issue ' + str(queryset.item_name),
        'queryset': queryset,
        'form': form,
        'username': 'Issued_to: ' + str(request.user),
    }
    return render(request, 'add_items.html', context)



def received_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
        
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issued_quantity = 0
        instance.quantity += instance.received_quantity
            
        # Set the received_by field to what is entered in the form
        received_by = form.cleaned_data.get('received_by')
        instance.received_by = received_by

        messages.success(request, 'Successfully Received Items! ' + str(instance.quantity) + ' ' + str(instance.item_name) + 's now in Store')
        instance.save()
        return redirect('/stock_detail/' + str(instance.id))
        
    context = {
        'title': 'Receive ' + str(queryset.item_name),
        'queryset': queryset,
        'form': form,
        'username': 'Received_by: ' + str(request.user),
    }
    return render(request, 'add_items.html', context)



def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Reorder Level for ' + str(instance.item_name) + ' is updated to' + str(instance.reorder_level))
        return redirect('/list_items/')
    context = {
        'instance': queryset,
        'form': form,
    }
    return render(request, 'add_items.html', context)

@login_required
def list_history(request):
    header = 'LIST STOCK HISTORY'
    form = StockHistorySearchForm(request.POST or None)
    queryset = StockHistory.objects.all()

    if request.method == 'POST':
        form = StockHistorySearchForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            item_name = form.cleaned_data['item_name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            queryset = StockHistory.objects.filter(
                item_name__icontains=item_name,
                last_updated__range=[start_date, end_date]
            )

            if category:
                queryset = queryset.filter(category=category)

            user_filter = form.cleaned_data['user_filter']
            
            # Depending on the user_filter, filter the history records
            if user_filter == 'issued':
                issued_records = queryset.filter(issued_to=request.user.username)
                # Set Received By to "none" for issued operations
                issued_records.update(received_by='none')
            elif user_filter == 'received':
                received_records = queryset.filter(received_by=request.user.username)
                # Set Issued To to "none" for received operations
                received_records.update(issued_to='none')

            if form.cleaned_data['export_to_csv']:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
                writer = csv.writer(response)
                writer.writerow(['ID', 'CATEGORY', 'ITEM_NAME', 'QUANTITY IN STORE',
                                'ISSUED QUANTITY', 'RECEIVED QUANTITY', 'LAST UPDATED',
                                'ISSUED TO', 'RECEIVED BY'])
                for stock in queryset:
                    writer.writerow([stock.id, stock.category, stock.item_name, stock.quantity,
                                    stock.issued_quantity, stock.received_quantity,
                                    stock.last_updated, stock.issued_to, stock.received_by])
                return response

    context = {
        'header': header,
        'queryset': queryset,
        'form': form,
    }

    return render(request, 'list_history.html', context)


