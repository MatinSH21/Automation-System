# Generated by Django 3.2 on 2023-09-05 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], help_text="Select between 'M', 'F' and 'O'.", max_length=1, verbose_name='gender'),
        ),
    ]