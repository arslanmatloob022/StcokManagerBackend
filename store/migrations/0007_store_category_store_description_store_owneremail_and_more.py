# Generated by Django 5.1.4 on 2024-12-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='ownerEmail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='ownerPhone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]