# Generated by Django 5.1.4 on 2024-12-26 18:42

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_store_category_store_description_store_owneremail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_email', models.EmailField(max_length=254)),
                ('order_no', models.CharField(editable=False, max_length=8, unique=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='store.batch')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.product')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]