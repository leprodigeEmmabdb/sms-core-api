#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv as load_env

# Charger les variables d'environnement depuis le fichier .env
load_env()

def main():
    """Run administrative tasks."""
    if os.getenv("DJANGO_ENV") == "prod":

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.prod')
        print(f"Running in production mode {os.getenv('DJANGO_ENV')}")
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
        print(f"Running in production mode {os.getenv('DJANGO_ENV')}")

    try:
            from django.core.management import execute_from_command_line
    except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
