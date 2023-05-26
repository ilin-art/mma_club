import os
import django
from datetime import date
from django.utils import timezone
from tasks.models import Task

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.chdir(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fight_club.settings")

import django
django.setup()

from django.core.management import call_command


from faker import Faker
from users.models import User

fake = Faker()

for _ in range(1000):
    email = fake.email()
    phone_number = fake.phone_number()
    User.objects.create_user(full_name=email, email=email, phoneNumber=phone_number, signal_date=date.today(), is_staff=True)
    user = User.objects.get(full_name=email)
    user.save()
    task = Task(user=user, relevance=True, signal_date=timezone.now())
    task.save()
