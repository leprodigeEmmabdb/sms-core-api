from django.core.management.base import BaseCommand
from django.utils import timezone

from appuser.models import User
from root.utilss import check_exists, get_random_string


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-n', '--number', type=str,
                            help='change phone'
                            )

        # Named (optional) arguments
        parser.add_argument(
            "-p",
            '--pseudo', type=str,
            help='change pseudo',
        )

    def handle(self, *args, **options):
        phone = options.get('number')
        pseudo = options.get('pseudo')
        self.stdout.write(self.style.WARNING('[+] Start Change...'))

        if phone and phone != 'none':
            self.stdout.write(self.style.NOTICE(f'[.] Changing Phone: {phone} ...'))
            st, user = check_exists(User, {'phone__iexact': phone})
            if st:
                data = user.first()
                code = get_random_string(5).upper()
                nw_phone = f"{code}_{data.phone}"
                self.stdout.write(self.style.SUCCESS(f'[.] New Phone: {nw_phone}'))
                user.update(phone=nw_phone, name=nw_phone, updated_at=timezone.now())
            else:
                self.stdout.write(self.style.WARNING(f'[!] Phone {phone} not found'))

        if pseudo and pseudo != 'none':
            st, user = check_exists(User, {'pseudo__iexact': pseudo})
            self.stdout.write(self.style.NOTICE(f'[.] Changing Pseudo: {pseudo}...'))
            if st:
                data = user.first()
                code = get_random_string(5).upper()
                nw_pseudo = f"{code}_{data.pseudo}"
                self.stdout.write(self.style.SUCCESS(f'[.] New Pseudo: {nw_pseudo}'))
                user.update(pseudo=nw_pseudo, updated_at=timezone.now())
            else:
                self.stdout.write(self.style.WARNING(f'[!] Pseudo {pseudo} not found'))

        self.stdout.write(self.style.WARNING('[+] End Change'))
