from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_emailotp_id"),
    ]

    operations = [
        migrations.DeleteModel(name="EmailOTP"),
    ]
