import datetime as dt

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, transaction


class CustomerManager(BaseUserManager):
    def create(self, email, password, first_name, last_name, dob):
        """
        Creates and saves a Customer with the given
        name, email and password.
        """
        today = dt.datetime.now()
        email = email
        with transaction.atomic():
            user = self.model(
                email=email,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                date_joined=today,
                is_admin=False,
            )
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password,
        first_name="",
        last_name="",
    ):
        user = self.create(
            email,
            password,
            first_name,
            last_name,
            dob=None,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    dob = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        default=dt.datetime.now,
    )

    USERNAME_FIELD = "email"

    objects = CustomerManager()

    def has_perm(self, *_args, **_kwargs):
        # Is required else admin won't work
        # Handle whether the user has a specific permission?"
        return self.is_admin

    def has_module_perms(self, *_args, **_kwargs):
        # Is required else admin won't work
        # Handle whether the user has permissions to view the app `app_label`?"
        return self.is_admin


class Policy(models.Model):
    # choice for state
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, help_text="Customer for this quote"
    )
    type = models.CharField(
        max_length=50,
        help_text="Type of quote (e.g. Personal, Accident, etc.)",
    )
    premium = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Premium for this quote"
    )
    cover = models.DecimalField(
        max_digits=15, decimal_places=2, help_text="Cover for this quote"
    )
    state = models.CharField(
        default="New", max_length=50, help_text="State for this quote"
    )

    def __str__(self):
        return self.customer.first_name + ": " + str(self.type)
