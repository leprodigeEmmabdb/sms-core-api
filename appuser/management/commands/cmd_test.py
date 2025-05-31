from functools import reduce
from operator import or_

from django.core.management.base import BaseCommand

from django.db.models import Q, Sum

from appuser.models import User
from twilio.rest import Client



class Command(BaseCommand):
    help = 'Update slug'

    def dynmatic(self):
        filters = {f'{x}__icontains': 'admin' for x in ['name', 'nom']}
        print(filters)
        q_list = [Q(**{k: v}) for k, v in filters.items()]
        print(q_list)
        reducers = reduce(or_, q_list)
        print(reducers)
        query = User.objects.filter(reducers)
        #
        print(query.query)
        print(query.values())

    # def check_instance(self):
    #     x = dict(a=1)
    #     y = dict(b=2)
    #     z = {**x, **y}
    #
    #     print(z)
    #
    #     req = JsonResponse(dict(d=4))
    #     print(type(req))
    #
    #     result = not isinstance(req, JsonResponse)
    #
    #     print(result)

    def send_sms(self, phone):
        account_sid = "ACb0b7a81a78273c509a61df7005b5adfb"
        auth_token = "40c0d595a42b4ed44a8f4c67b5f120c2"
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body="Welcome to PESA Sango TEST",
            from_='PESASANGO',
            to=phone
        )

        print(message.sid)

    def handle(self, *args, **options):
        # print(timezone.get_current_timezone())
        # print(User.objects.values())
        # print(User.objects.using('mysql').values())
        # for phone in ['+243814191009', '+243898900119', '+243898900274']:
        for phone in ['+243898900384', "+243853010697"]:
            self.send_sms(phone)
        # from pyffmpeg import FFmpeg
        # path = os.path.join(BASE_DIR, 'media', 'data.m4v')
        # dest_path = os.path.join(BASE_DIR, 'media', 'thumb.jpg')
        # ff = FFmpeg()
        # ff.convert(path, dest_path)
        # print('test')
