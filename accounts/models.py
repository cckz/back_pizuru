from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.get('username')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('e-mail'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class AccountInfoModel(models.Model):
    user = models.ForeignKey(User, verbose_name='Профиль', related_name='profile', on_delete=models.CASCADE)
    title_org = models.CharField(max_length=100, verbose_name='Организация', blank=True)
    phone = models.CharField(max_length=9, verbose_name='Контактный телефон', blank=True)
    city = models.CharField(max_length=30, verbose_name='Город', blank=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', blank=True)
    more_info = models.TextField(verbose_name='Дополнительная информация', blank=True)
    domain = models.CharField(max_length=30, verbose_name='Домен', blank=True)
    domain_active = models.BooleanField(verbose_name='Включить на обслуживание', default=False)
    news_blog = models.BooleanField(verbose_name='Новости / Блог', default=False)
    stock_discounts = models.BooleanField(verbose_name='Акции / Скидки', default=False)

    class Meta:
        db_table = 'profile_info'
        ordering = ['title_org']
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __unicode__(self):
        if self.title_org:
            return self.title_org
        else:
            return self.user.email

    def __str__(self):
        if self.title_org:
            return self.title_org
        else:
            return self.user.email

class WorkerAccountModel(models.Model):
    to_user = models.ForeignKey(User,
                                  verbose_name='Профиль',
                                  related_name='workers',
                                  on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Сотрудник')
    password = models.CharField(max_length=255, verbose_name='Пароль')

    class Meta:
        db_table = 'workers'
        verbose_name = 'Рабочий'
        verbose_name_plural = 'Рабочие'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name