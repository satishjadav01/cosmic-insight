from django.db import models

class NumerologyId(models.Model):

    birth_date = models.DateField(unique=True)

    mind_num = models.PositiveSmallIntegerField()
    heart_num = models.PositiveSmallIntegerField()
    practical_num = models.PositiveSmallIntegerField()

    create_id = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Numerology for {self.birth_date} "

