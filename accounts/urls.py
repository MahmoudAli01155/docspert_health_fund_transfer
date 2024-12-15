from django.urls import path
from .views import *

urlpatterns = [
    path('api-import/', ImportAccountsView.as_view(), name='import-accounts'),
    path('api-accounts/', ListAccountsView.as_view(), name='list-accounts'),
    path('api-accounts/<uuid:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('api-transfer/', TransferFundsView.as_view(), name='transfer-funds'),
    path('temp-import/', import_accounts, name='import-accounts'),
    path('temp-accounts/', list_accounts, name='list-accounts'),
    path('temp-accounts/<uuid:pk>/', account_detail, name='account-detail'),
    path('temp-transfer/', transfer_funds, name='transfer-funds'),
]