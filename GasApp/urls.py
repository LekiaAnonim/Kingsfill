from django.urls import path
from . import views

app_name = 'GasApp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
#     path('base', views.BaseView.as_view(), name='base'),
    path('batches', views.BatchView.as_view(), name='batches'),
     path('shops', views.ShopView.as_view(), name='shops'),
    path('shop/<int:id>/customers', views.CustomersView.as_view(), name='customers'),
    path('shop/<int:shop_id>/batch/<int:id>/sales', views.BatchSaleView.as_view(), name='batch-sales'),
    path('shop/<int:id>/batches', views.ShopBatchView.as_view(), name='shop-batches'),
    path('shop/<int:id>/batch/create', views.BatchCreateView.as_view(), name='batch-create'),
    path('shop/<int:id>/batch/<int:pk>/update', views.BatchUpdateView.as_view(), name='batch-update'),
     path('shop/create', views.ShopCreateView.as_view(), name='shop-create'),
    path('shop/<int:pk>/update', views.ShopUpdateView.as_view(), name='shop-update'),
    path('sale/<int:pk>/receipt', views.SaleDetail.as_view(), name='sale-receipt'),
    path(
        route='search_results',
        view=views.SearchResultsList.as_view(),
        name='search_results'
    ),
    # Login and Password reset
    path(
        route='login',
        view=views.UserLoginView.as_view(),
        name='login'
    ),
    path(
        route='reset-password',
        view=views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset_complete/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password-change', views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('activate/<uidb64>/<token>/',
         views.activate, name='activate'),

    path('print', views.GeneratePdf.as_view(), name='print')
]
