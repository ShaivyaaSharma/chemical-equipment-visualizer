import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visualizer.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Superuser 'admin' created successfully with password 'admin'.")
    else:
        print("Superuser 'admin' already exists.")

if __name__ == "__main__":
    create_superuser()
