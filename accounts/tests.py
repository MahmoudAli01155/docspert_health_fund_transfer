from django.test import TestCase

# Create your tests here.
from .models import Account, Transaction

class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(account_number='cc26b56c-36f6-41f1-b689-d1d5065b95af', account_holder='John Doe', balance=1000)
        Account.objects.create(account_number='be6acfdc-cae1-4611-b3b2-dfb5167ba5fe', account_holder='Jane Doe', balance=2000)

    def test_account_creation(self):
        account = Account.objects.get(account_number='cc26b56c-36f6-41f1-b689-d1d5065b95af')
        self.assertEqual(account.account_holder, 'John Doe')

    def test_fund_transfer(self):
        from_account = Account.objects.get(account_number='cc26b56c-36f6-41f1-b689-d1d5065b95af')
        to_account = Account.objects.get(account_number='be6acfdc-cae1-4611-b3b2-dfb5167ba5fe')

        from_account.balance -= 500
        to_account.balance += 500

        from_account.save()
        to_account.save()
        self.assertEqual(from_account.balance, 500)
        self.assertEqual(to_account.balance, 2500)