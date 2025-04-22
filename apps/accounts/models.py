import uuid
from datetime import timedelta
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('E-mail address must be provided.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group, related_name='customuser_set')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'accounts_user'

    def clean(self):
        super().clean()
    
    def has_perm(self, perm, obj=None):
        if getattr(self, 'is_admin', False):
            return True
        
        app_label, codename = perm.split('.') if '.' in perm else (None, perm)
        if app_label:
            return any(
                group.permissions.filter(
                    content_type__app_label=app_label,
                    codename=codename
                ).exists()
                for group in self.groups.all()
            )
        else:
            return any(perm in group.get_all_permissions() for group in self.groups.all())
        
class CustomUserInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    token = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invitations_sent')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    class Meta:
        db_table = 'accounts_user_invitation'
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        
        if not self.expire_at:
            self.expire_at = timezone.now() + timedelta(hours=48)
            
        return super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expire_at