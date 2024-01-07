from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator, ValidationError, MaxLengthValidator
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.contrib.auth import password_validation

# Create your models here.


# role based model
class MassRoleDetailModel(models.Model):
    role_num = models.CharField(max_length=15)
    role_desc = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.role_desc
    
    
# Registration model
class RegistrationModel(models.Model):
    role_type = models.ForeignKey(MassRoleDetailModel, on_delete=models.DO_NOTHING, related_name='role_tye')
    email = models.EmailField(validators=[EmailValidator()], blank=False, null=False)
    password = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(8, message="Password must be at least 8 characters long."),
            RegexValidator(r'[A-Z]', message="Password must contain at least one uppercase letter."),
            RegexValidator(r'[a-z]', message="Password must contain at least one lowercase letter."),
            password_validation.validate_password,
        ],
        blank=False,
        null=False,
    )
    full_name = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z]+\s[a-zA-Z]+$', message="Full name must be in the format 'FirstName LastName'.")], blank=False, null=False)
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message="Phone number must be 10 digits long and contain only numeric characters.")], blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100,  blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$', message="Pincode must be 6 digits long and contain only numeric characters.")], blank=False, null=False)
    
    def __str__(self) -> str:
        return self.full_name
    
    
# Catergory Model
class CategoryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
# Content Model
class ContentModel(models.Model):
    user_type = models.ForeignKey(RegistrationModel, on_delete=models.DO_NOTHING, related_name='user_tye', null=True)
    title = models.CharField(max_length=30, blank=False, null=False)
    body = models.CharField(max_length=300, blank=False, null=False)
    summary = models.CharField(max_length=60, blank=False, null=False)
    document = models.FileField(upload_to='documents/', blank=False, null=False)
    categories = models.ManyToManyField('CategoryModel', related_name='contents')
    
