"""
Database setup script for TrackMyTCG.
This script creates the hardcoded user and default settings.

Run this script after running migrations:
python setup_database.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.settings_app.models import UserSettings


def create_hardcoded_user():
    """Create the hardcoded user for MVP"""
    print("Creating hardcoded user...")

    # Check if user already exists
    if User.objects.filter(username='tcguser').exists():
        print("User 'tcguser' already exists.")
        user = User.objects.get(username='tcguser')
    else:
        user = User.objects.create_user(
            username='tcguser',
            email='user@trackmytcg.com',
            password='password123',
            first_name='TCG',
            last_name='User'
        )
        print(f"Created user: {user.username}")

    # Create default settings for user
    settings, created = UserSettings.objects.get_or_create(user=user)
    if created:
        print(f"Created default settings for user: {user.username}")
    else:
        print(f"Settings already exist for user: {user.username}")

    return user


if __name__ == '__main__':
    print("=" * 50)
    print("TrackMyTCG Database Setup")
    print("=" * 50)

    user = create_hardcoded_user()

    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print(f"\nUser credentials:")
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Password: password123")
    print(f"\nYou can now start the Django server:")
    print(f"  python manage.py runserver")
    print("=" * 50)
