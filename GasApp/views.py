from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Batch, Sale
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseCreateView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.http import JsonResponse
from datetime import date, datetime
from django.views.generic import FormView
from django.views.generic.list import MultipleObjectMixin
from .form import SaleForm, BatchForm
from django.db.models import Sum, Count

# Create your views here.
class BatchView(ListView):
    model = Batch
    template_name = 'batch.html'
    context_object_name = 'batches'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):

        # Call the base implementation first to get the context
        context = super(BatchView, self).get_context_data(**kwargs)

        return context

class SaleDetail(DetailView):
    model = Sale
    template_name = 'sale_detail.html'

class BatchCreateView(CreateView):
    model = Batch
    # fields = ['batch_name', 'date_created', 'cost', 'kg', 'price_per_kg', 'vendor_name','vendor_phone', 'close_account']
    template_name = 'batch_form.html'
    form_class = BatchForm


class BatchUpdateView(UpdateView):
    model = Batch
    # fields = ['batch_name', 'date_created', 'cost', 'kg', 'price_per_kg', 'vendor_name', 'close_account']
    template_name = 'batch_form.html'
    form_class = BatchForm

class BatchDeleteView(DeleteView):
    model = Batch
    success_url = reverse_lazy('ue_app:channel_detail')



class BatchSaleView(ListView, FormView):
    model = Sale
    template_name = "batch_sale.html"
    paginate_by = 12
    form_class = SaleForm
    # success_url = reverse_lazy('GasApp:sale-receipt')
    # fields = ['kg', 'price', 'date', 'customer_name', 'customer_phone']

    def get_queryset(self):
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        return Sale.objects.filter(batch=batch).order_by('-date')

    def get_context_data(self, *args, **kwargs):
        context = super(BatchSaleView,
                        self).get_context_data(**kwargs)
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        batch_sales = Sale.objects.filter(batch=batch).order_by('-date')


       
        if batch_sales.aggregate(Sum('price'))['price__sum'] == None:
            total_sales_price = 0
        else:
             total_sales_price = batch_sales.aggregate(Sum('price'))['price__sum']

        profit = total_sales_price - batch.cost
        if batch_sales.aggregate(Sum('kg'))['kg__sum'] == None:
            total_sales_kg = 0
        else:
            total_sales_kg = batch_sales.aggregate(Sum('kg'))['kg__sum']

        sales_count = batch_sales.count()

        context['batch_sales'] = batch_sales
        context['batch'] = batch
        context['profit'] = profit
        context['total_sales_kg'] = total_sales_kg
        context['sales_count'] = sales_count
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        batch_sales = Sale.objects.filter(batch=batch).order_by('-date')

        # Date Display in Stats Tab
        latest_date = batch_sales.last().date
        latest_month = latest_date.strftime('%m')
        latest_day = latest_date.strftime('%d')
        
        date_request = request.GET.get('date-filter')
        if date_request == None:
            date_ = latest_date
            batch_data_date = Sale.objects.filter(batch=batch, date = date_).values()
        else:
            date_ = date_request
            batch_data_date = Sale.objects.filter(batch=batch, date = date_).values()

        
        batch_data_date_kg = batch_data_date.aggregate(Sum('kg'))['kg__sum']
        batch_data_date_price = batch_data_date.aggregate(Sum('price'))['price__sum']

        # Month Display in Stats Tab
        month_request = request.GET.get('month-filter')
        if month_request == None:
            
            month_ = latest_date.month
            year_ = latest_date.year
            batch_data_month = Sale.objects.filter(batch=batch, date__month = month_, date__year = year_).values()
        else:
            month_request_ = datetime.strptime(month_request, '%Y-%m')
            print(month_request_)
            month_ = month_request_.month
            year_ = month_request_.year
            batch_data_month = Sale.objects.filter(batch=batch, date__month = month_, date__year = year_).values()

        batch_data_month_kg = batch_data_month.aggregate(Sum('kg'))['kg__sum']
        batch_data_month_price = batch_data_month.aggregate(Sum('price'))['price__sum']

        # ----------------------------------------------------------------------------------
        # Year Display in Stats Tab
        year_request = request.GET.get('year-filter')
        if year_request== None:
            year_real = latest_date.year
            batch_data_year = Sale.objects.filter(batch=batch, date__year = year_real).values()
        else:
            
            year_real = year_request
            batch_data_year = Sale.objects.filter(batch=batch, date__year = year_real).values()

        batch_data_year_kg = batch_data_year.aggregate(Sum('kg'))['kg__sum']
        batch_data_year_price = batch_data_year.aggregate(Sum('price'))['price__sum']

        # -------------------------------------------------------------------------------------------

        if batch_sales.aggregate(Sum('price'))['price__sum'] == None:
            total_sales_price = 0
        else:
             total_sales_price = batch_sales.aggregate(Sum('price'))['price__sum']

        profit = total_sales_price - batch.cost
        if batch_sales.aggregate(Sum('kg'))['kg__sum'] == None:
            total_sales_kg = 0
        else:
            total_sales_kg = batch_sales.aggregate(Sum('kg'))['kg__sum']

        sales_count = batch_sales.count()

        context['date_'] = date_
        context['batch_data_date_kg'] = batch_data_date_kg
        context['batch_data_date_price'] = batch_data_date_price

        context['date_'] = date_
        context['latest_date'] = latest_date
        context['latest_month'] = latest_month
        context['latest_day'] = latest_day
        context['month_'] = month_
        context['year_'] = year_
        context['batch_data_month'] = batch_data_month
        context['batch_data_month_kg'] = batch_data_month_kg
        context['batch_data_month_price'] = batch_data_month_price

        context['year_real'] = year_real
        # context['batch_data_month'] = batch_data_year
        context['batch_data_year_kg'] = batch_data_year_kg
        context['batch_data_year_price'] = batch_data_year_price

        context['batch_sales'] = batch_sales
        context['batch'] = batch
        context['profit'] = profit
        context['total_sales_kg'] = total_sales_kg
        context['sales_count'] = sales_count
        return render(request, self.template_name, context)


    def form_valid(self, form, *args, **kwargs):
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        batch_sales = Sale.objects.filter(batch=batch).last()
        # print(batch_sales)
        form.instance.batch = batch
        if batch_sales == None:
            form.instance.sale_id = 1
            self.object = form.save()
            return redirect('GasApp:sale-receipt', 1)
        else:
            form.instance.sale_id = batch_sales.id+1
            self.object = form.save()
            return redirect('GasApp:sale-receipt', batch_sales.id+1)
        
    
    # def get_success_url(self):
    #     return reverse_lazy('GasApp:sale-receipt', self.sale_form.id)

class SearchResultsList(ListView):
    model = Sale
    context_object_name = "sales"
    template_name = "search.html"

    def get_queryset(self):
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        return Sale.objects.filter(batch=batch).order_by('-date')
        