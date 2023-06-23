from datetime import datetime
import pytz
from django.shortcuts import render, HttpResponse, reverse, HttpResponseRedirect, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login
from django.db.models.functions import Lower
from django.views import View
from .forms import ProductCreationForm,NewUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import pandas as pd
from .models import Products,Sells, Adds, Order

user_registration_token = "admin-4598-users"
# Create your views here.
def register_request(request):
  form = NewUserForm(request.POST)
  if form.is_valid():
    registration_token = form.cleaned_data['registration_token']
    if registration_token!= user_registration_token:
      messages.error(request, 'Provide the correct registration token.')
      return redirect('.')
    user = form.save()
    login(request, user)
    messages.success(request, "Registration successful." )
    return redirect("products-list")
  messages.error(request, f"Unsuccessful registration. Invalid information.{form.errors.as_json(escape_html=True)}")
  form = NewUserForm()
  return render (request=request, template_name="user_register.html", context={"register_form":form})
	
class ProductsListView(ListView):
    model = Products
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductsListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by(Lower("name"))
        return qs
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["now"] = timezone.now()
      return context

class ProductCreateView(LoginRequiredMixin,View):
    def get(self):
        context = {
            "form":ProductCreationForm()
        }
        return render(self.request,"market/product_create.html",context)
    def post(self, *args, **kwargs):
        data = ProductCreationForm(self.request.POST) 
        try:
            if data.is_valid():
                data_vals = data.cleaned_data
                data.save()
                messages.success(self.request,f"Added {data_vals.get('name')} to products.")
                return   redirect('products-list')
            else:
              messages.error(self.request, data.errors)
              return redirect("products-list")
        except Exception as raised_exception:
            messages.error(self.request, str(raised_exception))
            return redirect("products-list")
                
class ProductEditView(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
      ids = self.request.GET.get('ids', '').split(',')
      quantities = list(self.request.GET['quantities'])
      date = datetime.now(pytz.timezone('Africa/Lagos'))
      db_order = Order( order_time= date)
      db_order.save()
      order_id = db_order.id

      name_list = []
      costs_list = []
      for i in range(len(ids)):
        db_product = Products.objects.get(id=ids[i])
        req_quant = int(quantities[0])
        cost = req_quant*db_product.unit_price
        
        db_sell = Sells(
          product=db_product,
          product_name = db_product.name,
          quantity=req_quant,
          cost= cost,
          order = db_order,
          date_sold= date
          )
        db_product.quantity -= req_quant
        db_sell.save()
        db_product.save()
        name_list.append(db_sell.product_name)
        costs_list.append(db_sell.cost)
      
      total_cost = sum(costs_list)
      name_list.append("total")
      costs_list.append(total_cost)
      name_list.append("date")
      costs_list.append(date.strftime("%H:%M:%S %d-%m-%y" ))

      data_dict = {
         "Names": name_list,
         "costs": costs_list
      }
      
      return JsonResponse(data_dict)
    
    def post(self, *args, **kwargs):
        try:
            id = self.request.POST['id']
            db_product = Products.objects.get(id=id)
            quantity = int( self.request.POST['number'])
            if self.request.POST['action']=='add':
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
  
class ProductUpdateView(LoginRequiredMixin,UpdateView):
    # specify the model you want to use
    model = Products
  
    # specify the fields
    fields = [
        "name",
        "unit_price"
    ]
    success_url = "/"

class SellsTransactionsView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
      data = self.request.GET
      sells_query_filter = Sells.objects
      if data.get('name') is not None:
        sells_query_filter = sells_query_filter.filter(product_name==data.get('name'))
      if data.get('after_date') is not None:
        sells_query_filter = sells_query_filter.filter(date_sold>=data.get('date'))
      if data.get('before_date') is not None:
        sells_query_filter = sells_query_filter.filter(date_sold<=data.get('before_date'))
      sells_query_filter = sells_query_filter.order_by('-date_sold').values()
      context = {
        'sells':sells_query_filter
      }
      return render(self.request, 'market/sells_transactions.html', context)

class AddsTransactionsView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
      data = self.request.GET
      sells_query_filter = Adds.objects.all()
      
      sells_query_filter = sells_query_filter.order_by('-date_added').values()
      context = {
        'adds':sells_query_filter
      }
      return render(self.request, 'market/adds_transactions.html', context)
      
class ProductsDeleteView(LoginRequiredMixin,DeleteView):
    model = Products
    success_url ="/"    
    template_name = "market/product_delete.html"

