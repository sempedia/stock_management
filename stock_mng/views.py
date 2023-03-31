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
    title = 'Welcome: This is the Home Page'
    form = 'This is the form'
    body = 'This is the body'
    context = {'title': title,
               'form': form,
               'body': body,
               }
    return redirect('/list_items')
    # return render(request, 'home.html', context)

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

        context = {
            'form': form,
            'header': header,
            'queryset': queryset,
        }
    return render(request, 'list_items.html', context)

def about(request):
    header = 'About us'
    body = ' Stock Management System that ease your life!'
    context = {'header': header,
               'body': body,
               }
    return render(request, 'about.html', context)

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
    # history = HistoricalRecords()
    form = IssueForm(request.POST  or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.received_quantity = 0
        instance.quantity -= instance.issued_quantity
        instance.issued_by = str(request.user)
        # instance.issued_by = str(request.user)
        messages.success(request, 'Successfully Issued Items! ' + str(instance.quantity) + ' ' + str(instance.item_name) + 's now left in Store')
        instance.save()
        return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': 'Issue ' + str(queryset.item_name),
        'queryset': queryset,
        'form': form,
        'username': 'Issued_to: ' + str(request.user),
    }
    return render(request, 'add_items.html', context)


def received_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    # history = HistoricalRecords()
    form = ReceiveForm(request.POST  or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issued_quantity = 0
        instance.quantity += instance.received_quantity
        instance.received_by = str(request.user)
        # instance.received_by = str(request.user)
        messages.success(request, 'Successfully Received Items! ' + str(instance.quantity) + ' ' + str(instance.item_name) + 's now in Store')
        instance.save()
        return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
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
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    context = {
        'header': header,
        'queryset': queryset,
        'form': form,
    }
    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(
                                            item_name__icontains=form['item_name'].value(),
                                            last_updated__range=[
                                                form['start_date'].value(),
                                                form['end_date'].value()])
        if category != '':
            queryset = queryset.filter(category_id=category)
        
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename = "Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'CATEGORY', 'ITEM_NAME', 'QUANTITY IN STORE',
                            'ISSUED QUANTITY', 'RECEIVED QUANTITY', 'LAST UPDATED',
                            'ISSUED BY', 'RECEIVED BY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.id, stock.category, stock.item_name, stock.quantity,
                            stock.issued_quantity, stock.received_quantity, stock.last_updated,
                            stock.issued_by, stock.received_by])
                
            return response
        context = {
         'form': form,
         'header': header,
         'queryset': queryset,
    }
    return render(request, 'list_history.html', context)
