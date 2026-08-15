from django.db import models

class signup(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirmPassword = models.CharField(max_length=255)
    is_admine = models.BooleanField(default=False)


class login(models.Model):
    mobile = models.CharField(max_length=10)
    datetime = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'login'
        verbose_name = 'User Login'
        verbose_name_plural = 'User Logins'


    def __str__(self):
        return f"Login by {self.mobile} at {self.datetime}"

