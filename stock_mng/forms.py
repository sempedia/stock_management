from django import forms
from .models import Stock, StockHistory
from django.core.exceptions import ValidationError


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']
        
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required.')
        for item in Stock.objects.all():
            if item.category == category:
                raise forms.ValidationError(str(category) + ' is already created.')
        return category
              
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required.')
        for item in Stock.objects.all():
            if item.item_name == item_name:
                raise forms.ValidationError(str(item_name) + ' is already created.')
        return item_name


class StockSearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']
        
          
class StockHistorySearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'start_date', 'end_date']
        
class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issued_quantity', 'issued_to']
        
class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['received_quantity', 'received_by']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
    
