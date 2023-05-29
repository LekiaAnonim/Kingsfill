from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import (PasswordResetDoneView, PasswordResetConfirmView,
                                        PasswordResetCompleteView, PasswordChangeView,
                                       PasswordChangeDoneView, PasswordResetView)
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.views.generic import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.urls import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Batch, Sale, Shop
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseCreateView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.http import JsonResponse
from datetime import date, datetime
from django.views.generic import FormView
from django.views.generic.list import MultipleObjectMixin
from .form import SaleForm, BatchForm, ShopForm
from django.db.models import Sum, Count
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from io import BytesIO
UserModel = get_user_model()
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'



class BatchView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = 'batch.html'
    context_object_name = 'batches'
    paginate_by = 12
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, *args, **kwargs):

        # Call the base implementation first to get the context
        context = super(BatchView, self).get_context_data(**kwargs)
        
        return context
class ShopView(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'shop.html'
    context_object_name = 'shops'
    paginate_by = 12
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

class ShopDetailView(DetailView):
    model = Shop
    template_name = "shop_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        batches = Batch.objects.filter(shop=self.object).order_by('-id')
        context['batches'] = batches
        return context
class CustomersView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'customers_list.html'
    context_object_name = 'customers'
    paginate_by = 12
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

    def get_queryset(self):

        shop = get_object_or_404(Shop, id=self.kwargs.get('id'))
        customers_group = Sale.objects.filter(batch__shop = shop).values('customer_phone').annotate(Sum('kg'), Sum('price'))
        # print(customers_group)
        return customers_group
class SaleDetail(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sale_detail.html'
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

class BatchCreateView(LoginRequiredMixin, CreateView):
    model = Batch
    template_name = 'batch_form.html'
    form_class = BatchForm
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"


class BatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Batch
    template_name = 'batch_form.html'
    form_class = BatchForm
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    template_name = 'shop_form.html'
    form_class = ShopForm
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

class ShopUpdateView(LoginRequiredMixin, UpdateView):
    model = Shop
    template_name = 'shop_form.html'
    form_class = ShopForm
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

class BatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Batch
    success_url = reverse_lazy('GasApp:batches')
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

class ShopBatchView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = "shop_batch.html"
    paginate_by = 12
    context_object_name = 'batches'
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"
    
    def get_queryset(self):
        shop = get_object_or_404(Shop, pk=self.kwargs.get('id'))
        return Batch.objects.filter(shop=shop).order_by('date_created').order_by('-id')
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShopBatchView,
                        self).get_context_data(**kwargs)
        shop = get_object_or_404(Shop, pk=self.kwargs.get('id'))
        batches = Batch.objects.filter(shop=shop).order_by('date_created').order_by('-id')
        context['shop'] = shop
        context['batches'] = batches
        return context

import csv

def csv_download(request):
    # get queryset of batch sales with id filter
    batch_sales = Sale.objects.all().order_by('-batch__shop__shop_name').order_by('-batch__batch_name').order_by('-date').order_by('-id')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=sale_data.csv'
    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(['Transaction ID', 'Kg', 'Price', 'Payment Method', 'Date', 'Batch', 'Shop'])
    for sale in batch_sales:
        writer.writerow([sale.id, sale.kg, sale.price, sale.payment_type, sale.date, sale.batch.batch_name, sale.batch.shop.shop_name])

    return response

class BatchSaleView(LoginRequiredMixin, ListView, FormView):
    model = Sale
    template_name = "batch_sale.html"
    paginate_by = 12
    form_class = SaleForm
    login_url = "GasApp:login"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        return Sale.objects.filter(batch=batch).order_by('date').order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(BatchSaleView,
                        self).get_context_data(**kwargs)
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        batch_sales = Sale.objects.filter(batch=batch).order_by('-date').order_by('-id')


       
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

        shop = get_object_or_404(Shop, id=self.kwargs.get('shop_id'))
        context['shop'] = shop

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
        batch_sales = Sale.objects.filter(batch=batch).order_by('-date').order_by('-id')
        
        # Date Display in Stats Tab
        if batch_sales.last() == None:
            latest_date = date.today()
        else:
            latest_date = Sale.objects.filter(batch=batch).first().date

        latest_month = latest_date.strftime('%m')
        latest_day = latest_date.strftime('%d')
        
        date_request = request.GET.get('date-filter')
        if date_request == None:
            date_ = latest_date   
        else:
            date_ = date_request
        batch_data_date = Sale.objects.filter(batch=batch, date = date_).values()
        batch_sales_pos = Sale.objects.filter(batch=batch, payment_type='POS', date = date_).values()
        batch_sales_cash = Sale.objects.filter(batch=batch, payment_type='Cash', date = date_).values()
        batch_sales_transfer = Sale.objects.filter(batch=batch, payment_type='Bank Transfer', date = date_).values()

        # Calculate the sum of kg and price for total batch sales and each payment type
        batch_data_date_kg = batch_data_date.aggregate(Sum('kg'))['kg__sum']
        batch_data_date_price = batch_data_date.aggregate(Sum('price'))['price__sum']
        batch_sales_date_pos_kg = batch_sales_pos.aggregate(Sum('kg'))['kg__sum']
        batch_sales_date_pos_price = batch_sales_pos.aggregate(Sum('price'))['price__sum']
        batch_sales_date_cash_kg = batch_sales_cash.aggregate(Sum('kg'))['kg__sum']
        batch_sales_date_cash_price = batch_sales_cash.aggregate(Sum('price'))['price__sum']
        batch_sales_date_transfer_kg = batch_sales_transfer.aggregate(Sum('kg'))['kg__sum']
        batch_sales_date_transfer_price = batch_sales_transfer.aggregate(Sum('price'))['price__sum']

        # Month Display in Stats Tab
        month_request = request.GET.get('month-filter')
        if month_request == None:
            month_ = latest_date.month
            year_ = latest_date.year
        else:
            month_request_ = datetime.strptime(month_request, '%Y-%m')
            month_ = month_request_.month
            year_ = month_request_.year
        batch_data_month = Sale.objects.filter(batch=batch, date__month = month_, date__year = year_).values()
        batch_sales_pos_month = Sale.objects.filter(batch=batch, payment_type='POS', date__month = month_, date__year = year_).values()
        batch_sales_cash_month = Sale.objects.filter(batch=batch, payment_type='Cash', date__month = month_, date__year = year_).values()
        batch_sales_transfer_month = Sale.objects.filter(batch=batch, payment_type='Bank Transfer', date__month = month_, date__year = year_).values()

        batch_data_month_kg = batch_data_month.aggregate(Sum('kg'))['kg__sum']
        batch_data_month_price = batch_data_month.aggregate(Sum('price'))['price__sum']
        batch_sales_month_pos_kg = batch_sales_pos_month.aggregate(Sum('kg'))['kg__sum']
        batch_sales_month_pos_price = batch_sales_pos_month.aggregate(Sum('price'))['price__sum']
        batch_sales_month_cash_kg = batch_sales_cash_month.aggregate(Sum('kg'))['kg__sum']
        batch_sales_month_cash_price = batch_sales_cash_month.aggregate(Sum('price'))['price__sum']
        batch_sales_month_transfer_kg = batch_sales_transfer_month.aggregate(Sum('kg'))['kg__sum']
        batch_sales_month_transfer_price = batch_sales_transfer_month.aggregate(Sum('price'))['price__sum']

        # ----------------------------------------------------------------------------------
        # Year Display in Stats Tab
        year_request = request.GET.get('year-filter')
        if year_request== None:
            year_real = latest_date.year
            # batch_data_year = Sale.objects.filter(batch=batch, date__year = year_real).values()
        else:
            year_real = year_request
        batch_data_year = Sale.objects.filter(batch=batch, date__year = year_real).values()
        batch_sales_pos_year = Sale.objects.filter(batch=batch, payment_type='POS', date__year = year_real).values()
        batch_sales_cash_year = Sale.objects.filter(batch=batch, payment_type='Cash', date__year = year_real).values()
        batch_sales_transfer_year = Sale.objects.filter(batch=batch, payment_type='Bank Transfer', date__year = year_real).values()

        batch_data_year_kg = batch_data_year.aggregate(Sum('kg'))['kg__sum']
        batch_data_year_price = batch_data_year.aggregate(Sum('price'))['price__sum']
        batch_sales_year_pos_kg = batch_sales_pos_year.aggregate(Sum('kg'))['kg__sum']
        batch_sales_year_pos_price = batch_sales_pos_year.aggregate(Sum('price'))['price__sum']
        batch_sales_year_cash_kg = batch_sales_cash_year.aggregate(Sum('kg'))['kg__sum']
        batch_sales_year_cash_price = batch_sales_cash_year.aggregate(Sum('price'))['price__sum']
        batch_sales_year_transfer_kg = batch_sales_transfer_year.aggregate(Sum('kg'))['kg__sum']
        batch_sales_year_transfer_price = batch_sales_transfer_year.aggregate(Sum('price'))['price__sum']

        context['batch_sales_year_pos_kg'] = batch_sales_year_pos_kg
        context['batch_sales_year_pos_price'] = batch_sales_year_pos_price
        context['batch_sales_year_cash_kg'] = batch_sales_year_cash_kg
        context['batch_sales_year_cash_price'] = batch_sales_year_cash_price
        context['batch_sales_year_transfer_kg'] = batch_sales_year_transfer_kg
        context['batch_sales_year_transfer_price'] = batch_sales_year_transfer_price

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

        context['batch_sales_date_pos_kg'] = batch_sales_date_pos_kg
        context['batch_sales_date_pos_price'] = batch_sales_date_pos_price
        context['batch_sales_date_cash_kg'] = batch_sales_date_cash_kg
        context['batch_sales_date_cash_price'] = batch_sales_date_cash_price
        context['batch_sales_date_transfer_kg'] = batch_sales_date_transfer_kg
        context['batch_sales_date_transfer_price'] = batch_sales_date_transfer_price

        context['latest_date'] = latest_date
        context['latest_month'] = latest_month
        context['latest_day'] = latest_day
        context['month_'] = month_
        context['year_'] = year_
        context['batch_data_month'] = batch_data_month
        context['batch_data_month_kg'] = batch_data_month_kg
        context['batch_data_month_price'] = batch_data_month_price
        context['batch_sales_month_pos_kg'] = batch_sales_month_pos_kg
        context['batch_sales_month_pos_price'] = batch_sales_month_pos_price
        context['batch_sales_month_cash_kg'] = batch_sales_month_cash_kg
        context['batch_sales_month_cash_price'] = batch_sales_month_cash_price
        context['batch_sales_month_transfer_kg'] = batch_sales_month_transfer_kg
        context['batch_sales_month_transfer_price'] = batch_sales_month_transfer_price

        context['year_real'] = year_real
        context['batch_data_year_kg'] = batch_data_year_kg
        context['batch_data_year_price'] = batch_data_year_price
        context['batch_sales_year_pos_kg'] = batch_sales_year_pos_kg
        context['batch_sales_year_pos_price'] = batch_sales_year_pos_price
        context['batch_sales_year_cash_kg'] = batch_sales_year_cash_kg
        context['batch_sales_year_cash_price'] = batch_sales_year_cash_price
        context['batch_sales_year_transfer_kg'] = batch_sales_year_transfer_kg
        context['batch_sales_year_transfer_price'] = batch_sales_year_transfer_price

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

        if batch_sales:
            form.instance.sale_id = batch_sales.id+1
            self.object = form.save()
            return redirect('GasApp:sale-receipt', batch_sales.id+1)
        else:
            form.instance.sale_id = 1
            self.object = form.save()
            return redirect('GasApp:sale-receipt', 1)

class SearchResultsList(ListView):
    model = Sale
    context_object_name = "sales"
    template_name = "search.html"

    def get_queryset(self):
        batch = get_object_or_404(Batch, id=self.kwargs.get('id'))
        return Sale.objects.filter(batch=batch).order_by('-date')

class UserLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = 'login.html'
    context_object = {"login_form": AuthenticationForm}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            
            login(request, user)
            messages.success(request, f"Login Successful ! "
                                f"Welcome {user.username}.")
            if user.is_superuser == True:
                return redirect('GasApp:shops')
            
            else:
                shop = get_object_or_404(Shop, user=user)
                return redirect('GasApp:shop-batches', shop.id)

        else:
            messages.error(request,
                           f"Please enter a correct username and password. Note that both fields may be case-sensitive."
                           )
            return render(request, self.template_name, self.context_object)




class PasswordResetView(PasswordResetView):
    template_name = 'registration/pwd_reset_form.html'
    email_template_name = "registration/email_text/password_reset_email.html"
    from_email = ''
    subject_template_name = "registration/email_text/password_reset_subject.txt"
    success_url = reverse_lazy("GasApp:password_reset_done")

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/email_text/password_reset_done.html' 

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/email_text/password_reset_confirm.html'
    success_url = reverse_lazy("GasApp:password_reset_complete")

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/email_text/password_reset_complete.html'

class PasswordChangeView(PasswordChangeView):
    template_name = 'registration/email_text/password_change_form.html'
    success_url = reverse_lazy("GasApp:password_change_done")

class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/email_text/password_change_done.html'

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, f'Hi {user.username}, your registration was successful!! .')
        return reverse('GasApp:shops')
    else:
        return reverse_lazy('GasApp:email_verification_invalid')


class EmailVerificationConfirm(TemplateView):
    template_name = 'registration/email_verification_confirm.html'


class EmailVerificationInvalid(TemplateView):
    template_name = 'registration/email_verification_invalid.html'





def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
                result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def render_pdf_view(request):
    template_path = 'sale_detail.html'
    context = {}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("utf8")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

#Creating a class based view
class GeneratePdf(DetailView):
    model=Sale
    template_path = 'sale_detail.html'
    def get(self, request, *args, **kwargs):
        data = Sale.objects.filter(id=self.kwargs.get('id'))
        open('result.html', "w").write(render_to_string('sale_detail.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('result.html')
            
            # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')