# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import email
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.utils import timezone
from django_countries.fields import CountryField


class UserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        """create and save new user"""
        if not name:
            raise ValueError('Users must have a username')

        user = self.model(name=name, **extra_fields)
        if user.email:
            user.email = self.normalize_email(user.email)
        user.created_at = timezone.now()
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, password):
        """create and save new superuser"""
        user = self.create_user(name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (("abonne", "abonne"),
                    ("census", "census"))
    """custom user Model"""
    name = models.CharField(max_length=255, unique=True, null=True)
    phone = models.CharField(max_length=255, unique=True, null=True)

    email = models.EmailField(max_length=255, unique=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    postnom = models.CharField(max_length=255, blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    pseudo = models.CharField(max_length=255, blank=True, null=True)

    role = models.CharField(max_length=255, blank=True, null=True, choices=ROLE_CHOICES, default="abonne")

    province = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    longtd = models.CharField(max_length=255, blank=True, null=True)
    latd = models.CharField(max_length=255, blank=True, null=True)

    network_id = models.CharField(max_length=255, blank=True, null=True)
    network_source = models.CharField(max_length=255, blank=True, null=True)
    network_photo = models.CharField(max_length=255, blank=True, null=True)

    iso3Code = models.CharField(max_length=5, blank=True, null=True, default='COD')
    # isoCode = models.CharField(max_length=5, blank=True, null=True, default='CD')
    isoCode = CountryField(max_length=5, blank=True, null=True, default='CD')
    phoneCode = models.CharField(max_length=10, blank=True, null=True, default='243')
    country = models.CharField(max_length=255, blank=True, null=True, default='Congo, the Democratic Republic of the')
    # country = CountryField(max_length=255, blank=True, null=True, default='Congo, the Democratic Republic of the')

    reset_pwd_code = models.CharField(max_length=255, blank=True, null=True)
    can_reset = models.BooleanField(default=False)
    reset_code_valid = models.BooleanField(default=False)
    reset_retry = models.IntegerField(default=0)
    reset_at = models.DateTimeField(null=True, blank=True)
    reset_confirmed_at = models.DateTimeField(null=True, blank=True)
    reset_expired_at = models.DateTimeField(null=True, blank=True)

    confirm_code = models.CharField(max_length=255, blank=True, null=True)
    confirm_retry = models.IntegerField(default=0)
    confirm_expired_at = models.DateTimeField(null=True, blank=True)
    # confirmed_at = models.DateTimeField(null=True, blank=True)

    is_test = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    is_teacher = models.BooleanField(default=False)

    genre = models.CharField(max_length=20, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    EMAIL_FIELD = "email"

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = 'tb_user'


class Configurations(models.Model):
    field = models.CharField(max_length=255, blank=True, null=True, unique=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    edit_user = models.IntegerField(default=0, blank=True, null=True)
    add_user = models.IntegerField(default=0, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'tb_configurations'


"""
Types:
SANGO
GROUP
USER
"""


class UsersAttachments(models.Model):
    filename = models.CharField(max_length=255, blank=True, null=True)
    media = models.ImageField(upload_to='users/', max_length=255)
    thumb = models.ImageField(upload_to='thumb/', max_length=255, null=True)

    temp_path = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=False, null=True)

    parent = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    size = models.DecimalField(max_digits=60, decimal_places=2, default=0, null=True, blank=True)

    expired_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.filename

    class Meta:
        db_table = 'tb_users_attachments'


class ConnexionsUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    is_active = models.BooleanField(default=True)
    channel = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    app_version = models.CharField(max_length=255, blank=True, null=True)
    os_version = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'tb_connexions_users'


class ContactMessages(models.Model):
    message = models.TextField(blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tb_contact_messages'


class AppNotifications(models.Model):
    key = models.CharField(max_length=255, blank=True, null=True)
    command = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    id_data = models.IntegerField(default=0, blank=True, null=True)
    id_sango = models.IntegerField(default=0, blank=True, null=True)
    id_msg = models.IntegerField(default=0, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(blank=True)

    class Meta:
        db_table = 'tb_app_notifications'


class MessagesPortail(models.Model):
    nom = models.CharField(max_length=255, blank=True, null=True)
    postnom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    objet = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tb_messages_portail'


class SmsSend(models.Model):
    phone = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    motif = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'tb_sms_send'
