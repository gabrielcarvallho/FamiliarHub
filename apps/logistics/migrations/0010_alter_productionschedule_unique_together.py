# Generated by Django 5.1.7 on 2025-06-09 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0009_productionschedule_order'),
        ('orders', '0012_order_payment_due_days'),
        ('products', '0006_alter_product_batch_packages_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productionschedule',
            unique_together={('product', 'order', 'production_date')},
        ),
    ]
