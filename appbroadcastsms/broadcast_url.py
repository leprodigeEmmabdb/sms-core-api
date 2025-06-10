from django.urls import path, include
from appbroadcastsms.vues.client.v_client import ClientViewSet
from appbroadcastsms.vues.smpp.v_smpp import SmppViewSet
from appbroadcastsms.vues.sms.v_sms import SmsViewSet
from rest_framework_nested import routers # type: ignore

router = routers.DefaultRouter()
router.register('client', ClientViewSet, basename="client")
router.register('sms', SmsViewSet, basename="sms")
router.register('send-message', SmsViewSet, basename="send-message")
#


urlpatterns = [
    path('', include(router.urls)),
    # path('recommand/<int:media_id>', Recommandation),
    # path('recommand_accueil/<int:compte_id>', Recommandation_page_accueil)
    
]
