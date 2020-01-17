from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# used for ovveriding the default user model
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# profile feed : import settings to retrieve the AUTH_USER_MODEL
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    # specify some functions in the manager that can be used to manipulate the model
    def create_user(self, email, name, password=None):
        """Create new user profile"""
        if not email:
            raise ValueError('User must have an email addess')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create a new superuser with given details"""
        user = self.create_user(email, name, password)
        # is_superuser is created automatically by PermissionsMixin
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


# this class inherit from AbstractBaseUser & PermissionsMixin
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # ovveride the default username CharField ( it is required by default),
    # we should also customize the UserProfileManager
    USERNAME_FIELD = 'email'
    # additional required field
    REQUIRED_FIELDS = ['name']

    def get_fulll_name(self):
        """Retrieve full name of the user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of the user"""
        return self.name

    def __str__(self):
        """Retrieve string representation of the user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    # best practice : use AUTH_USER_MODEL and not directly UserProfile because if we want to switch out our model and we
    # use the default django auth model ,we should chage manually the name of the model in the foreignKey every where we
    # referenced it, however with this best.p we should only change AUTH_USER_MODEL in settings
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as string"""
        return self.status_text
