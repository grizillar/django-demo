from django.db import models

# Create your models here.


class Campaign(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    cid = models.IntegerField(primary_key=True)
    name = models.TextField(
        db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pid = models.ForeignKey('Platform', models.DO_NOTHING,
                            db_column='pid', blank=True, null=True)
    spending = models.FloatField(blank=True, null=True)
    reach = models.IntegerField(blank=True, null=True)
    impression = models.IntegerField(blank=True, null=True)
    engagement = models.IntegerField(blank=True, null=True)
    objective = models.TextField(
        db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    video_view = models.IntegerField(blank=True, null=True)
    landing_page_view = models.IntegerField(blank=True, null=True)
    product_view = models.IntegerField(blank=True, null=True)
    add_to_cart = models.IntegerField(blank=True, null=True)
    purchase = models.IntegerField(blank=True, null=True)
    dateadded = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Campaign'


class Platform(models.Model):
    pid = models.IntegerField(primary_key=True)
    platform_name = models.TextField(
        db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Platform'


class Sitetraffic(models.Model):
    sid = models.IntegerField(primary_key=True)
    pid = models.ForeignKey(Platform, models.DO_NOTHING,
                            db_column='pid', blank=True, null=True)
    uri = models.TextField(
        db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    all_user = models.IntegerField(blank=True, null=True)
    new_user = models.IntegerField(blank=True, null=True)
    order_count = models.IntegerField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    dateadded = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SiteTraffic'


class Document(models.Model):
    csvfile = models.FileField(upload_to='documents/')
