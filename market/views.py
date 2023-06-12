from datetime import datetime
import pytz
from django.shortcuts import render, HttpResponse, reverse, HttpResponseRedirect, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from .models import Products,Sells, Adds
from django.views import View
from .forms import ProductCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class ProductsListView(ListView):
    model = Products

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["now"] = timezone.now()
      return context

class ProductCreateView(LoginRequiredMixin,View):
    def get(self, request):
        context = {
            "form":ProductCreationForm()
        }
        return render(self.request,"market/product_create.html",context)
    def post(self, *args, **kwargs):
        data = ProductCreationForm(self.request.POST) 
        try:
            if data.is_valid():
                data.save()
                return   redirect('products-list')
        except Exception as raised_exception:
            return redirect("products-list")
                
class ProductEditView(LoginRequiredMixin,View):
    def post(self, *args, **kwargs):
        try:
            id = self.request.POST['id']
            db_product = Products.objects.get(id=id)
            quantity = int( self.request.POST['number'])
            if self.request.POST['action']=='sell':
                if db_product.quantity>0 and quantity>0:
                    try:
                        if db_product.quantity<quantity:
                          messages.warning(f'not enough to sell')
                          return redirect(reverse('products-list'))
                        try:
                            date_sold = datetime.now(pytz.timezone('Africa/Lagos'))
                            db_sell = Sells(
                            product=db_product,
                            quantity=quantity,
                            product_name = db_product.name,
                            cost = round(quantity*db_product.unit_price, 2),
                            date_sold=date_sold
                            )
                            db_product.quantity -= quantity
                            db_product.last_time_sold = date_sold
                        except Exception as raised_exception:
                            print(raised_exception)
                            messages.error(self.request, 'An error occured retry the request or contact developer.')
                            return redirect(reverse('products-list'))
                        db_sell.save()
                        db_product.save()
                        messages.success(self.request, f'{quantity} pieces of {db_product.name} sold')
                        return redirect(reverse('products-list'))
                    except: 
                      return HttpResponseRedirect(reverse('products-list'), f'number not valid')
                      print(quantity)
                    db_product.quantity -= quantity
                    messages.success(f'sold {quantity}')
                    return redirect(reverse('products-list'))
                elif db_product.quantity==0 and quantity>0:
                    messages.warning(self.request, 'This product is finished.')
                    return redirect(reverse('products-list'))
                else:
                  messages.warning(self.request, ' quantity requested is 0')
                  return redirect(reverse('products-list'))
            elif self.request.POST['action']=='add':
                if quantity>0:
                    date_added = datetime.now(pytz.timezone('Africa/Lagos'))
                    db_add = Adds(
                    product=db_product,
                    product_name = db_product.name,
                    quantity=quantity,
                    date_added=date_added
                    )
                    db_product.quantity += quantity
                    db_product.last_time_updated = date_added
                    db_add.save()
                    db_product.save()
                    messages.success(self.request, f'{quantity} pieces of {db_product.name} added')
                    return redirect(reverse('products-list'))
                else:
                  messages.warning(self.request, ' quantity requested is 0')
                  return redirect(reverse('products-list'))
            return redirect(reverse('products-list'))
        except Exception as raised_exception:
            return HttpResponse(str(raised_exception))
  
class SellsTransactionsView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
      data = self.request.GET
      sells_query_filter = Sells.objects.all()
      if data.get('name') is not None:
        sells_query_filter = sells_query_filter.filter(product_name==data.get('name'))
      if data.get('after_date') is not None:
        sells_query_filter = sells_query_filter.filter(date_sold>=data.get('date'))
      if data.get('before_date') is not None:
        sells_query_filter = sells_query_filter.filter(date_sold<=data.get('before_date'))
      context = {
        'sells':sells_query_filter
      }
      return render(self.request, 'market/sells_transactions.html', context)
        