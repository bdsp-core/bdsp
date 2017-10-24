from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    """
    Manager object with methods to create
    User instances.
    """
    def create_user(self, email, password, is_active=True):
        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    The user authentication model
    """
    email = models.EmailField(max_length=255, unique=True, primary_key=True)
    join_date = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Mandatory fields for the default authentication backend
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    # For createsuperuser. Don't include USERNAME_FIELD or password
    # REQUIRED_FIELDS = ['username']

    # Mandatory methods for default authentication backend
    def get_full_name(self):
        if self.profile.middle_names:
            return ' '.join([self.profile.first_name, self.profile.middle_names,
                           self.profile.last_name])
        else:
            return ' '.join([self.profile.first_name, self.profile.last_name])

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    objects = UserManager()

    # Mandatory attributes for using the admin panel
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Profile(models.Model):
    """
    Class storing profile information which is
    not directly related to account activity
    or authentication.

    This model should contain some fields which help map
    projects to datacite:
    https://schema.datacite.org/
    https://schema.datacite.org/meta/kernel-4.0/doc/DataCite-MetadataKernel_v4.0.pdf
    """
    user = models.OneToOneField('user.User', related_name='profile')

    first_name = models.CharField(max_length=30)
    middle_names = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=30)
    url = models.URLField(default='', blank=True, null=True)
    identity_verification_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """
    The receiver function for receiving post_save signals of User objects.
    Creates and attaches an empty Profile when a User object is created.
    """
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.save()


class AssociatedEmail(models.Model):
    """
    An email the user associates with their account
    """
    user = models.ForeignKey('user.User', related_name='associated_emails')
    email = models.EmailField(max_length=255, unique=True)
    verification_date = models.DateTimeField(null=True)
    is_primary_email = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_backup_email = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_associated_email(sender, **kwargs):
    """
    Creates and attaches an unverified AssociatedEmail when a User object is created.
    """
    user = kwargs["instance"]
    if kwargs["created"]:
        email = AssociatedEmail(user=user, email=user.email, is_primary_email=True)
        email.save()


class BaseAffiliation(models.Model):
    """
    Base class inherited by profile affiliations and static snapshot
    affiliation info.
    """
    order = models.SmallIntegerField(default=0)
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    
    class Meta:
        abstract = True

class Affiliation(BaseAffiliation):
    """
    Affiliations belonging to a profile.
    """
    profile = models.ForeignKey('user.Profile', related_name='affiliations')



