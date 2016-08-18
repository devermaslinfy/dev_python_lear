import uuid
import geocoder
import requests

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

from localflavor.us.models import USStateField, USZipCodeField

from learlight import utils


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()

    class Meta:
        abstract = True


class Account(BaseModel):
    name = models.CharField(max_length=30)
    internal_id = models.CharField(max_length=10, default=utils.generate_internal_id, unique=True)
    external_id = models.IntegerField(default=utils.generate_external_id)
    logo_image_url = models.CharField(max_length=1000)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=30)
    state = USStateField()
    postal_code = USZipCodeField()
    parent_account = models.ForeignKey('Account', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='owned_accounts', blank=True, null=True)
    associates = models.ManyToManyField(User)
    stores = models.ManyToManyField('self', symmetrical=False, related_name='store_account', blank=True)

    def __unicode__(self):
        return self.name


class Associate(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    associate_id = models.CharField(max_length=6, unique=True, default=utils.generate_id)
    image_url = models.CharField(max_length=1000, null=True, blank=True)

    @property
    def associate_image_url(self):
        return self.image_url or static('learlight/images/store-associate.png')


class JewelryType(BaseModel):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Customer(BaseModel):
    account = models.ForeignKey(Account)
    associate = models.ForeignKey(User)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_completed = models.BooleanField(default=False)
    purchase_id = models.IntegerField(null=True, blank=True)
    authorized = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, null=True, blank=False)
    last_name = models.CharField(max_length=30, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    address = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    county = models.CharField(max_length=30, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    postal_code = USZipCodeField(null=True, blank=True)
    country = models.CharField(max_length=112, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    quote_requested = models.BooleanField(default=False)
    jewelry_type = models.ForeignKey(JewelryType, null=True, blank=True)
    jewelry_value = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        geocode = 'geocode' in kwargs and kwargs.pop('geocode')
        if geocode and self.postal_code:
            g = geocoder.google(self.postal_code)
            if g.city:
                self.city = g.city
            if g.state:
                self.state = g.state
            if g.county:
                self.county = g.county
            else:
                response = requests.get(settings.COUNTY_LOOKUP_API_URL % (g.lat, g.lng))
                if response.status_code == 200:
                    try:
                        self.county = response.json()['County']['name']
                    except (ValueError, KeyError):
                        pass
            if g.country:
                self.country = g.country
        super(Customer, self).save(*args, **kwargs)

    @property
    def formatted_transaction_id(self):
        return "%s-%s" % (settings.SYSTEM_ID, self.transaction_id)

    @property
    def quote_id(self):
        return "%s-%d" % (settings.SYSTEM_ID, self.id)

    @property
    def jewelry_image_url(self):
        try:
            jewelry_image_url = self.image_set.filter(category=Image.CATEGORY_JEWELRY)[0].url
        except IndexError:
            jewelry_image_url = None

        return jewelry_image_url

    @property
    def jewelry_image_urls(self):
        return [i.url for i in self.image_set.filter(category=Image.CATEGORY_JEWELRY)]

    @property
    def receipt_image_url(self):
        try:
            receipt_image_url = self.image_set.filter(category=Image.CATEGORY_RECEIPT)[0].url
        except IndexError:
            receipt_image_url = None

        return receipt_image_url


class Image(BaseModel):
    CATEGORY_RECEIPT = 'receipt'
    CATEGORY_JEWELRY = 'jewelry'
    CATEGORY_CHOICES = (
        (CATEGORY_RECEIPT, 'Receipt'),
        (CATEGORY_JEWELRY, 'Jewelry')
    )

    customer = models.ForeignKey(Customer)
    url = models.CharField(max_length=1000)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)

    def __unicode__(self):
        return "(%s) %s" % (self.category, self.url)
class LearlightAccountAssociates(models.Model):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)

    class Meta:
        managed = False
        db_table = 'learlight_account_associates'
        unique_together = (('account', 'user'),)
