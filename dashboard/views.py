import csv
import json

from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse

from learlight.utils import StreamBuffer
from learlight.models import Customer, Account, Associate
from dashboard.reports import SummaryReport

@login_required()
def index(request):
    context = {}
    summary_report = SummaryReport(top_limit=3)
    summary_context = summary_report.get_summary()
    context.update(summary_context)
    context.update({
        'javascript_context': json.dumps({
            'total_quotes_today': summary_context['total_quotes_today'],
            'total_emails_today': summary_context['total_emails_today'],
            'total_drops_today': summary_context['total_drops_today'],
            'num_transactions_by_day': summary_context['num_transactions_by_day'],
        }),
    })
    return render(request, 'dashboard/index.html', context)

@login_required()
def accounts(request):
    return render(request, 'dashboard/accounts.html', {})

@login_required()
def acme(request):
    return render(request, 'dashboard/acme.html', {})

@login_required()
def burlington(request):
    return render(request, 'dashboard/burlington.html', {})

@login_required()
def leads_and_quotes(request):
    return render(request, 'dashboard/leads_and_quotes.html', {})

@login_required()
def export_transaction_data(request):
    rows = [(
        'Jeweler Name',
        'Jeweler ID',
        'LearLabs CRM Account',
        'Associate ID',
        'Associate First Name',
        'Associate Last Name',
        'Quote Requested',
        'Transaction Date',
        'Transaction Time',
        'LearLabsCRM Unique Transaction ID',
        'LearLabsCRM Unique Quote ID',
        'Customer Purchase ID',
        'Customer First Name',
        'Customer Last Name',
        'Cusotmer Email',
        'Customer Address',
        'Customer City',
        'Customer County',
        'Customer State',
        'Customer Zip',
        'Customer Country',
        'Customer Phone Number',
        'Item Type',
        'Item Photo',
        'Receipt Photo',
        'Item Estimated Value'
    )]
    for customer in Customer.objects.filter(email__isnull=False):
        account = customer.account
        associate = customer.associate
        rows.append((
            account.name,
            account.external_id,
            account.internal_id,
            associate.associate.associate_id,
            associate.first_name,
            associate.last_name,
            customer.quote_requested,
            customer.date_created.strftime('%-m/%-d/%Y'),
            customer.date_created.strftime('%-H:%M'),
            customer.formatted_transaction_id,
            customer.quote_id,
            customer.purchase_id,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.address,
            customer.city,
            customer.county,
            customer.state,
            customer.postal_code,
            customer.country,
            customer.phone_number,
            customer.jewelry_type,
            customer.jewelry_image_url,
            customer.receipt_image_url,
            customer.jewelry_value
        ))
    writer = csv.writer(StreamBuffer())
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    header = 'attachment; filename="learlabscrm_transaction_data_%s.csv"' % datetime.now().strftime('%Y%m%d')
    response['Content-Disposition'] = header
    return response
