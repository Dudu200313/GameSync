# Generated by Django 5.1.5 on 2025-03-11 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameSync_app', '0002_remove_review_user_logview_delete_log_delete_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logview',
            old_name='review_date',
            new_name='logview_date',
        ),
    ]
