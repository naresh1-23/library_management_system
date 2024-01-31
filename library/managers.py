from django.contrib.auth.base_user import BaseUserManager

#this is used to modify the default django authentication
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,full_name, password, **extra_fields):
        
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,full_name = full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,full_name = None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,full_name, password, **extra_fields)

    def create_superuser(self, email,full_name,  password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,full_name, password, **extra_fields) 