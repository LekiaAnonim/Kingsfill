from django.urls import path
from . import views

app_name = 'GasApp'

urlpatterns = [
    path('batches', views.BatchView.as_view(), name='batches'),
    path('batch/<int:id>/sales', views.BatchSaleView.as_view(), name='batch-sales'),
    path('batch/create', views.BatchCreateView.as_view(), name='batch-create'),
    path('batch/<int:pk>/update', views.BatchUpdateView.as_view(), name='batch-update'),
    path('sale/<int:pk>/receipt', views.SaleDetail.as_view(), name='sale-receipt'),
    path(
        route='search_results',
        view=views.SearchResultsList.as_view(),
        name='search_results'
    ),
]
