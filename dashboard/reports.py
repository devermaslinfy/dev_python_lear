import datetime

from django.contrib.auth.models import User
from django.db.models import Count, Sum
from learlight.models import Account, Associate, Customer

REQUEST_TYPES = ('quote', 'pic', 'drop')
QUOTE, PIC, DROP = REQUEST_TYPES


def today_midnight():
    return datetime.date.today()

def tomorrow_midnight():
    return datetime.date.today() + datetime.timedelta(days=1)

def get_date_list(num_days, end_date=None):
    if end_date is None:
        end_date = datetime.date.today()
    return list(reversed([end_date - datetime.timedelta(days=n) for n in range(num_days+1)]))

def fill_date_map(date_list, date_map, date_fmt, default_value):
    new_date_map = {}
    for d in date_list:
        date_str = d.strftime(date_fmt)
        if date_str in date_map:
            new_date_map[date_str] = date_map[date_str]
        else:
            new_date_map[date_str] = default_value
    return new_date_map

def get_date_filter(from_date, to_date):
    if from_date == to_date:
        to_date = None
    filters = {}
    if from_date is not None and to_date is not None:
        filters['date_created__range'] = (from_date, to_date)
    elif from_date is not None:
        filters['date_created__gte'] = from_date
    else:
        filters['date_created__lte'] = to_date
    return filters


class AccountReport(object):
    def __init__(self, **kwargs):
        self.from_date = kwargs.get('from_date', None)
        self.to_date = kwargs.get('to_date', None)
        self.instance = kwargs.get('instance', None)

    def get_top(self, n):
        '''Returns the top N accounts by number of transactions completed.'''
        filters = {
            "parent_account__isnull": True,
            "stores__customer__transaction_completed": True,
        }
        return Account.objects.filter(**filters) \
            .annotate(Count('stores__customer')) \
            .order_by('-stores__customer__count')[:n]

    def get_size(self):
        '''Returns the total number of accounts.'''
        return Account.objects.filter(parent_account__isnull=True).count()

    def get_request_count(self, **kwargs):
        '''
        Returns the total number of transactions for a given type (i.e. number of quotes requested).
        '''
        request_type = kwargs.get('request_type', None)
        filters = self._get_customer_filters(request_type)
        return Customer.objects.filter(**filters).count()
    
    def get_request_value(self, **kwargs):
        '''
        Returns the total value of transactions for a given type
        (i.e. attainment value of all completed transactions).
        '''
        request_type = kwargs.get('request_type', None)
        filters = self._get_customer_filters(request_type)
        
        result = Customer.objects.filter(**filters) \
            .aggregate(total_jewelry_value=Sum('jewelry_value'))
        
        value = result['total_jewelry_value']
        if value is None:
            value = 0
        return value
    
    def get_request_count_series(self, **kwargs):
        '''
        Returns a series of counts by date for a given request type (i.e. quotes requested).
        Useful for plotting a line chart.
        '''
        request_type = kwargs.get('request_type', None)

        # determine the number of days this series will span
        if self.from_date is not None and self.to_date is not None:
            delta = self.to_date - self.from_date
            num_days = delta.days
        elif self.from_date is not None:
            delta = datetime.date.today() - self.from_date
        else:
            num_days = kwargs.get('num_days', 6)

        # query the database for date/count
        filters = self._get_customer_filters(request_type)
        query_result = Customer.objects.filter(**filters) \
            .extra({"transaction_date": "date(date_created)"}) \
            .values('transaction_date') \
            .annotate(transaction_count=Count('id'))

        # create a mapping from date => count, using iso8601 format for sortability
        date_fmt = "%Y-%m-%d"
        transaction_date_map = dict([
            (t['transaction_date'].strftime(date_fmt), t['transaction_count'])
            for t in query_result
        ])

        # there might be gaps in the date series returned by the database because there's
        # no data for a particular date, so fill the gaps with "0" values
        date_list = get_date_list(num_days, datetime.date.today())
        date_lookup = fill_date_map(date_list, transaction_date_map, date_fmt, 0)
        
        # transform the dictionary into a series of objects containing the date and count
        result = [{
            "date": "{dt:%b} {dt.day}".format(dt=datetime.datetime.strptime(date_str, date_fmt)),
            "count": date_lookup[date_str]            
        } for date_str in sorted(date_lookup.keys())]
        
        return result
    
    def get_request_count_series_all(self):
        '''
        Returns the same thing as get_request_count_series(), except it includes *all* the request types.
        '''
        results = [self.get_request_count_series(request_type=rt) for rt in (QUOTE, PIC, DROP)]
        return [{
            'date': item[0]['date'],
            'quotes': item[0]['count'],
            'emails': item[1]['count'],
            'drops': item[2]['count'],            
        } for item in zip(*results)]    
    
    def _get_customer_account_filter(self):
        filters = {}
        account = self.instance
        if account is not None:
            filters['account__id__in'] = [account.id] + list(account.stores.values_list('id', flat=True))
        return filters

    def _get_customer_filters(self, request_type):
        if request_type is not None and request_type not in REQUEST_TYPES:
            raise Exception('Invalid request_type: %s Must be one of: %s' % (request_type, REQUEST_TYPES))

        filters = {}
        account = self.instance
        if account is not None:
            filters.update(self._get_customer_account_filter())
        if request_type in (QUOTE,PIC):
            filters['quote_requested'] = request_type == QUOTE
            filters['transaction_completed'] = True
        elif request_type == DROP:
            filters['transaction_completed'] = False
        else:
            filters['transaction_completed'] = True
        filters.update(get_date_filter(self.from_date, self.to_date))

        return filters


class StoreReport(AccountReport):
    def __init__(self, **kwargs):
        super(StoreReport, self).__init__(**kwargs)

    def get_top(self, n):
        '''Returns the top N stores by number of transactions completed.''' 
        filters = {
            "parent_account__isnull": False,
            "customer__transaction_completed": True,
        }
        return Account.objects.filter(**filters) \
            .annotate(Count('customer')) \
            .order_by('-customer__count')[:n]

    def get_size(self):
        '''Returns the total number of stores.'''
        return Account.objects.filter(parent_account__isnull=False).count()

    def _get_customer_account_filter(self):
        filters = {}
        account = self.instance
        if account is not None:
            filters['account__id'] = account.id
        return filters

class AssociateReport(object):
    def __init__(self, **kwargs):
        self.from_date = kwargs.get('from_date', None)
        self.to_date = kwargs.get('to_date', None)

    def get_top(self, n):
        '''Returns the top N associates by number of transactions completed.'''
        filters = {"customer__transaction_completed": True}
        return User.objects.filter(**filters) \
            .annotate(Count('customer')) \
            .order_by('-customer__count')[:n]

    def get_size(self):
        '''Returns the total number of associates.'''
        return User.objects.all().count()


class SummaryReport(object):
    def __init__(self, **kwargs):
        self.top_limit = kwargs.get('top_limit', 3)
    
    def get_top_accounts(self):
        return AccountReport().get_top(self.top_limit)
    
    def get_top_stores(self):
        return StoreReport().get_top(self.top_limit)
    
    def get_top_associates(self):
        return AssociateReport().get_top(self.top_limit)
    
    def count_total_accounts(self):
        return AccountReport().get_size()
    
    def count_total_stores(self):
        return StoreReport().get_size()
    
    def count_total_associates(self):
        return AssociateReport().get_size()
    
    def count_total_quotes_today(self):
        return AccountReport(from_date=today_midnight()).get_request_count(request_type=QUOTE)
    
    def count_total_emails_today(self):
        return AccountReport(from_date=today_midnight()).get_request_count(request_type=PIC)
    
    def count_total_drops_today(self):
        return AccountReport(from_date=today_midnight()).get_request_count(request_type=DROP)

    def total_jewelry_value_today(self, ):
        return AccountReport(from_date=today_midnight()).get_request_value()

    def get_num_quotes_by_day(self):
        return AccountReport(to_date=tomorrow_midnight()).get_request_count_series(request_type=QUOTE)

    def get_num_emails_by_day(self):
        return AccountReport(to_date=tomorrow_midnight()).get_request_count_series(request_type=PIC)
    
    def get_num_drops_by_day(self):
        return AccountReport(to_date=tomorrow_midnight()).get_request_count_series(request_type=DROP)

    def get_num_transactions_by_day(self):
        return AccountReport(to_date=tomorrow_midnight()).get_request_count_series_all()

    def get_summary(self):
        return {
            "top_accounts": self.get_top_accounts(),
            "top_stores": self.get_top_stores(),
            "top_associates": self.get_top_associates(),
            "total_accounts": self.count_total_accounts(),
            "total_stores": self.count_total_stores(),
            "total_associates": self.count_total_associates(),
            "total_quotes_today": self.count_total_quotes_today(),
            "total_emails_today": self.count_total_emails_today(),
            "total_drops_today": self.count_total_drops_today(),
            "num_transactions_by_day": self.get_num_transactions_by_day(),
            "total_jewelry_value_today": self.total_jewelry_value_today(),
        }

