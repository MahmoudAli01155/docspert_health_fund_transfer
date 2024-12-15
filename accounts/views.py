from django.shortcuts import render, redirect

# Create your views here.

import csv
import uuid
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer





#############[ api function ]##################################

class ImportAccountsView(APIView):
    def post(self, request):
        file = request.FILES['file']
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in reader:
            # print(row)
            Account.objects.create(
                account_number=uuid.UUID(row['ID']),
                account_holder=row['Name'],
                balance=row['Balance']
            )
        return Response({"status": "Accounts imported successfully"}, status=status.HTTP_201_CREATED)

class ListAccountsView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

class AccountDetailView(APIView):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

class TransferFundsView(APIView):
    def post(self, request):
        from_account = get_object_or_404(Account, account_number=request.data['from_account'])
        to_account = get_object_or_404(Account, account_number=request.data['to_account'])
        amount = float(request.data['amount'])

        if from_account.balance < amount:
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()

        transaction = Transaction.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)






#############[ mvt function ]##################################

def import_accounts(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in reader:
            Account.objects.create(
                account_number=uuid.UUID(row['ID']),
                account_holder=row['Name'],
                balance=row['Balance']
            )
        return redirect('list-accounts')
    return render(request, 'accounts/import_accounts.html')

def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/list_accounts.html', {'accounts': accounts})

def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'accounts/account_detail.html', {'account': account})

def transfer_funds(request):
    if request.method == 'POST':
        from_account = get_object_or_404(Account, account_number=request.POST['from_account'])
        to_account = get_object_or_404(Account, account_number=request.POST['to_account'])
        amount = float(request.POST['amount'])

        if from_account.balance < amount:
            return render(request, 'accounts/transfer_funds.html', {'error': 'Insufficient funds'})

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()

        Transaction.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

        return redirect('list-accounts')

    return render(request, 'accounts/transfer_funds.html')
