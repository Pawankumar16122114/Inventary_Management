from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    CustomUser, Category, Supplier, Product,
    StockTransaction, PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem
)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'email', 'phone', 'address')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'sku', 'description', 'category', 'supplier',
                  'price', 'cost', 'quantity', 'low_stock_threshold', 'image_url')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ('product', 'transaction_type', 'quantity', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if qty <= 0:
            raise forms.ValidationError('Quantity must be positive.')
        return qty


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ('supplier', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items_formset = PurchaseOrderItemFormSet(
            self.data or None,
            instance=self.instance if self.instance.pk else None,
        )


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ('product', 'quantity_ordered', 'unit_price')


PurchaseOrderItemFormSet = forms.inlineformset_factory(
    PurchaseOrder, PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('notes',)


class SalesOrderItemForm(forms.ModelForm):
    class Meta:
        model = SalesOrderItem
        fields = ('product', 'quantity', 'unit_price')


SalesOrderItemFormSet = forms.inlineformset_factory(
    SalesOrder, SalesOrderItem,
    form=SalesOrderItemForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
