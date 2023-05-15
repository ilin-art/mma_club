import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fight_club.settings')
django.setup()


from faker import Faker
from users.models import User
from django.utils import timezone
from tasks.models import Task

fake = Faker()

for _ in range(1000):
    email = fake.email()
    phone_number = fake.phone_number()
    User.objects.create_user(full_name=email, email=email, phoneNumber=phone_number)
    user = User.objects.get(full_name=email)
    user.save()
    task = Task.objects.get(user=user)
    # task = user.task_set.first()
    # task = Task(user=user, relevance=True, signal_date=timezone.now())
    task.relevance = True
    task.signal_date = timezone.now()
    task.save()
    task.save()
    