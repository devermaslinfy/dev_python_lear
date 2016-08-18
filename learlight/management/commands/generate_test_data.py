import logging
import datetime
import dateutil.parser
import random
import math

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.models import Count

from learlight.models import Account, Associate, Customer, JewelryType

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate and populate database with test data'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.default_logo_image_url = "https://s3.amazonaws.com/learlight-assets/email-jewlery-logo.png"
        self.account_names_list = None
        self.internal_id = 0
        
    def add_arguments(self, parser):
        parser.add_argument('--num_associates', type=int, default=75, help="Number of associates to create")
        parser.add_argument('--num_accounts', type=int, default=6, help="Number of accounts to create")
        parser.add_argument('--num_stores', type=int, default=23, help="Number of stores to create")
        parser.add_argument('--num_transactions', type=int, default=2000, help="Number of transactions to create")
        parser.add_argument('--transactions_start', default="2015-07-09T19:00:55Z", help="Start date for transactions")
        parser.add_argument('--transactions_end', default=datetime.datetime.now().isoformat(), help="End date for transactions")
        parser.add_argument('--transaction_rates', default=[47, 33, 20], help="Percentage of transactions that are quotes, pictures, and drops (i.e. 60, 30, 10)")    
        parser.add_argument('--reset', dest='reset', action='store_true')
        parser.set_defaults(reset=False)

    def handle(self, *args, **options):
        logger.info("Generate test data with options: %s" % options)

        if options['reset']:
            self.reset_database()

        self.generate_associates(options['num_associates'])
        self.generate_accounts(options['num_accounts'])
        self.generate_stores(options['num_stores'])
        self.assign_associates()
        self.generate_transactions(options['num_transactions'], {
            k: options[k] for k in ['transactions_start', 'transactions_end', 'transaction_rates']
        })
        
    def next_internal_id(self):
        self.internal_id += 1
        return str(self.internal_id)

    def get_excluded_ids(self, model_name):
        exclude_model_ids = {
            "learlight.account": [1,2],
            "auth.user": [1,2,3,4,5,6,7,8,9],
        }
        if model_name in exclude_model_ids:
            return exclude_model_ids[model_name]
        return []
    
    def reset_database(self):
        logger.info("Resetting the database (superuser preserved)")
        Customer.objects.exclude(pk__in=self.get_excluded_ids('learlight.customer')).delete()
        User.objects.exclude(pk__in=self.get_excluded_ids('auth.user')).delete()
        Account.objects.exclude(pk__in=self.get_excluded_ids('learlight.account')).delete()
        
    def generate_associates(self, num_associates):
        logger.info("Generating %d associates" % num_associates)
        i = 0
        while i < num_associates:
            username='associate%d' % i
            random_name = self.random_name()
            user = User(
                username=username,
                password=User.objects.make_random_password(),
                email='%s@localhost' % username,
                first_name=random_name[0],
                last_name=random_name[1],
            )
            user.save()
            associate = Associate(user=user, associate_id=self.next_internal_id(), created_by=1, updated_by=1)
            associate.save()
            i += 1
    
    def assign_associates(self):
        users = User.objects.exclude(pk__in=self.get_excluded_ids('auth.user'))
        num_users = len(users)
        accounts = Account.objects.exclude(pk__in=self.get_excluded_ids('learlight.account'))
        num_accounts = len(accounts)
        num_users_per_account = num_users / num_accounts

        associates_for = {}
        account_idx = 0
        i = 0
        for user in users:
            associates_for.setdefault(account_idx, []).append(user)
            i += 1
            if (account_idx + 1 < num_accounts) and (i % num_users_per_account == 0):
                account_idx += 1
        
        for account_idx in associates_for:
            account = accounts[account_idx]
            owner = associates_for[account_idx].pop()
            account.associates.add(*[user.id for user in associates_for[account_idx]])
            account.owner = owner
            account.save()
    
    def generate_accounts(self, num_accounts):
        logger.info("Generating %d accounts" % num_accounts)
        i = 0
        accounts = []
        while i < num_accounts:
            store_name = self.random_account_name()
            store_location = self.random_account_location()
            account = Account(
                internal_id=self.next_internal_id(),
                name=store_name,
                logo_image_url=self.default_logo_image_url,
                email="account%d@localhost" % i,
                phone_number="123-456-7890",
                address=store_location['address'],
                city=store_location['city'],
                state=store_location['state'],
                postal_code=store_location['postal_code'],
                parent_account=None,
                created_by=1,
                updated_by=1,
            )
            accounts.append(account)
            i += 1
        Account.objects.bulk_create(accounts)
    
    def generate_stores(self, num_stores):
        logger.info("Generating %d stores" % num_stores)
        accounts = Account.objects.filter(parent_account__isnull=True).exclude(pk__in=self.get_excluded_ids('learlight.account'))
        num_accounts = len(accounts)
        num_stores_per_account = num_stores / num_accounts
        
        account_idx = 0
        store_idx = 0
        stores = []
        while store_idx < num_stores:
            store_name = self.random_account_name()
            store_location = self.random_account_location()

            store = Account(
                internal_id=self.next_internal_id(),
                name=store_name,
                logo_image_url=self.default_logo_image_url,
                email="store%d@localhost" % store_idx,
                phone_number="123-456-7890",
                address=store_location['address'],
                city=store_location['city'],
                state=store_location['state'],
                postal_code=store_location['postal_code'],
                parent_account=accounts[account_idx],
                created_by=1,
                updated_by=1,
            )
            store_idx += 1
            if account_idx + 1 < num_accounts and (store_idx % num_stores_per_account == 0):
                account_idx += 1
            stores.append(store)
        Account.objects.bulk_create(stores)
        
        # Add "stores" relationship to the main/top-level account
        result_stores = Account.objects.filter(parent_account__isnull=False).exclude(pk__in=self.get_excluded_ids('learlight.account'))
        account_stores = {}
        for store in result_stores:
            account_stores.setdefault(store.parent_account.id, []).append(store.id)

        for account_id in account_stores:
            account = Account.objects.get(pk=account_id)
            account.stores.add(*account_stores[account_id])
            account.save()
    
    def generate_transactions(self, num_transactions, options):
        logger.info("Generating %d transactions" % num_transactions)

        start_date = dateutil.parser.parse(options['transactions_start'])
        end_date = dateutil.parser.parse(options['transactions_end'])
        quote_rate, email_rate, drop_rate = options['transaction_rates']
        rate_buckets = [
            ['quote', (quote_rate/100.0) * num_transactions],
            ['email', (email_rate/100.0) * num_transactions],
            ['drop', (drop_rate/100.0) * num_transactions],
        ]
        rate_buckets_diff = num_transactions - sum([ b[1] for b in rate_buckets])
        if rate_buckets_diff > 0:
            rate_buckets[-1][1] += rate_buckets_diff

        jewelry_types = JewelryType.objects.all()
        num_jewelry_types = len(jewelry_types)

        stores = Account.objects.annotate(associates_count=Count('associates__id')) \
            .filter(parent_account__isnull=False,associates_count__gt=0) \
            .exclude(pk__in=self.get_excluded_ids('learlight.account'))
        num_stores = len(stores)

        transaction_idx = 0
        customers = []
        while transaction_idx < num_transactions:
            random_store_idx = int(random.random() * num_stores)
            random_user_idx = 0
            random_jewelry_type_idx = int(random.random() * num_jewelry_types)
            random_jewelry_value = int(random.random() * 5000) + 1
            random_rate_bucket_idx = int(random.random() * len(rate_buckets))
            random_rate_bucket = rate_buckets[random_rate_bucket_idx]
            transaction_completed = (random_rate_bucket[0] in ('quote', 'email'))
            quote_requested = (random_rate_bucket[0] == 'quote')
            store_associate = stores[random_store_idx].associates.all()[random_user_idx]

            customer = Customer(
                account=stores[random_store_idx],
                associate=store_associate,
                authorized=True,
                first_name='Customer',
                last_name=str(transaction_idx),
                email='customer%d@localhost' % transaction_idx,
                quote_requested=quote_requested,
                transaction_completed=transaction_completed,
                jewelry_type=jewelry_types[random_jewelry_type_idx],
                jewelry_value=random_jewelry_value,
                created_by=store_associate.id,
                updated_by=store_associate.id,
            )
            customers.append(customer)

            random_rate_bucket[1] -= 1
            if random_rate_bucket[1] == 0:
                rate_buckets.pop(random_rate_bucket_idx)
            transaction_idx += 1

        Customer.objects.bulk_create(customers)
        
        date_created = end_date
        customer_idx = 0
        for customer in Customer.objects.exclude(pk__in=self.get_excluded_ids('learlight.customer')):
            customer_idx += 1
            if customer_idx % 100 == 0:
                date_created = date_created - datetime.timedelta(days=1)
                if date_created.date() < start_date.date():
                    date_created = start_date
            customer.date_created = date_created
            customer.date_updated = date_created
            customer.save(update_fields=['date_created', 'date_updated'])

    def random_account_name(self):
        if self.account_names_list is None:
            self.account_names_list = '''
Jewelry Empire
Special Engagements Jewelers
The Gold Lodge
Holidaze Jewelry
Diamond Sea
The Jewelry Place
The Golden Goose
Gold Galore
Lux Fine Jewelry
Holy Grail Jewelers
Touch of Gold
Sunkissed Jewelry
Sterling Co. Jewelry
Loves Jewelers
Trinity Jewelers & Co.
Travelers Jewelers
Pot of Gold
Watch Me Custom Jewelry
Ice Jewelers
The Diamond Band
Ireland Gold
Magic Clasp Jewelry
Goldmine Jewelry
Charming Jewelry Store
Ring of Memories Jewelers
Marias Touch Jewelry
She Said Yes! Jewelers
Johnson Jewelers
Sparkles Shop
The Velvet Box
Diamonds
Greater than Gold Jewelers
Stone Appeal
Metal Spectrum Jewelry Store
Illuminate Jewelers
Classics Jewelry
Infinity Jewelers
Classical Customs Jeweler
The Gallery
Smith Jewelers & Co.
The Galleria of Gems
The Looking Glass Jewelers
The Gemstone Gallery
The Jewelers Loupe
Luxury Gold
Making Memories Custom Jewelry
The Platinum People
Spring Jewelers
Jewelry Palace
Goldbar Jewelry Store
'''.strip().splitlines()
        return random.choice(self.account_names_list)

    def random_name(self):
        names = '''
SMITH
JOHNSON
WILLIAMS
JONES
BROWN
DAVIS
MILLER
WILSON
MOORE
TAYLOR
ANDERSON
THOMAS
JACKSON
WHITE
HARRIS
MARTIN
THOMPSON
GARCIA
MARTINEZ
ROBINSON
CLARK
RODRIGUEZ
LEWIS
LEE
WALKER
HALL
ALLEN
YOUNG
HERNANDEZ
KING
WRIGHT
LOPEZ
HILL
SCOTT
GREEN
ADAMS
BAKER
'''.strip().splitlines()
        return [random.choice(names).title(), random.choice(names).title()]
    
    
    def random_account_location(self):
        locations = [
            {"address": "98 Jackson St.", "city": "Salem", "state": "MA", "postal_code": "01970"},
            {"address": "111 Main St.", "city": "Burlington", "state": "MA", "postal_code": "01803"},
            {"address": "50 Quarry St.", "city": "Quincy", "state": "MA", "postal_code": "02170"},
            {"address": "1 Oxford St.", "city": "Cambridge", "state": "MA", "postal_code": "02138"},
            {"address": "1 City Hall Sq.", "city": "Boston", "state": "MA", "postal_code": "02201"},
        ]
        return random.choice(locations)
    
