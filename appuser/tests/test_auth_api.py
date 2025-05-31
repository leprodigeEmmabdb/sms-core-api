import json

import pytest
from django.urls import reverse

from appuser.models import User


pytestmark = pytest.mark.django_db


def test_cree_compte_avec_tous_les_champs_doit_retourner_vrai(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201



def test_cree_compte_sans_donnees_doit_retourne_faux(client):
    data={
    "name": "",
    "password": "",
    "email": "",
    "isoCode": "",
    "prenom": "",
    "postnom": "",
    "phone": ""
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  400

def test_cree_compte_omettant_un_champ_obligatoiredoit_retourner_faux(client):
    data={
   "name": "dolvasam",
    "password": "",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  400

def test_cree_compte_mettre_mauvais_format_mail_doit_retourner_faux(client):
    data={
   "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvabgmailcom",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  400

def test_cree_compte_mettre_mauvais_format_telephone_doit_retourner_faux(client):
    data={
   "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "fkfkkdfkdfkdf"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  400


def test_verify_utilisateur_recement_cree_est_inactif_doit_retourner_faux(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201

    res = json.loads(reponse.content)
    print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    assert user.is_active == 0


def test_confirmation_code_correct_doit_retourner_vrai(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":user.confirm_code})
    assert reponseact.status_code ==  204

def test_confirmation_code_incorrect_doit_retourner_faux(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    print("res===", res)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":"225455445"})
    assert reponseact.status_code ==  400
  



def test_confirmation_verifier_utilisateur_confirme_actif(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    #print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    print(user.confirm_code)
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":user.confirm_code})
   
    assert reponseact.status_code ==  204
    user=User.objects.get(id=id_user)
   
    #print("res===", resact)
    assert user.is_active ==True
 



def test_login_identifiant_correct(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":user.confirm_code})
    assert reponseact.status_code ==  204

    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
     }
    urlLogin= "/auth/jwt/create/"
    reponseLogin = client.post(path=urlLogin, data=data)
    assert reponseLogin.status_code ==  200

def test_login_identifiant_incorrect(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":user.confirm_code})
    assert reponseact.status_code ==  204

    data={
    "name": "dolvasam",
    "password": "g@d",
     }
    urlLogin= "/auth/jwt/create/"
    reponseLogin = client.post(path=urlLogin, data=data)
    assert reponseLogin.status_code ==  401


def test_login_avec_champs_vides(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":user.confirm_code})
    assert reponseact.status_code ==  204

    data={
   
     }
    urlLogin= "/auth/jwt/create/"
    reponseLogin = client.post(path=urlLogin, data=data)
    assert reponseLogin.status_code ==  400



def test_login_sans_envoyer_donnes(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":user.confirm_code})
    assert reponseact.status_code ==  204

    data={
    "name": "",
    "password": "",
     }
    urlLogin= "/auth/jwt/create/"
    reponseLogin = client.post(path=urlLogin, data=data)
    assert reponseLogin.status_code ==  400



def test_login_sans_envoyer_mot_de_passe(client):
    data={
    "name": "dolvasam",
    "password": "sam123456789@d",
    "email": "dolvab@gmail.com",
    "isoCode": "CD",
    "prenom": "sam",
    "postnom": "sam",
    "phone": "0827565888"
}
    url = "/auth/users/"
    reponse = client.post(path=url, data=data)
    assert reponse.status_code ==  201
    res = json.loads(reponse.content)
    print("res===", res)
    id_user=res['id']
    user=User.objects.get(id=id_user)
    #assert res['status'], "Hiring"
    #assert res['application_link'] ==""
    urlact = "/auth/users/activation/"
    reponseact = client.post(path=urlact, data={"confirm_code":user.confirm_code})
    assert reponseact.status_code ==  204

    data={
    "name": "dolvasam",
    "password": "",
     }
    urlLogin= "/auth/jwt/create/"
    reponseLogin = client.post(path=urlLogin, data=data)
    assert reponseLogin.status_code ==  400
