from django.db import models

class Codal(models.Model):

    Symbol = models.CharField(max_length=60)
    Name = models.CharField(max_length=60)
    PublishDateTime         = models.CharField(max_length=40)

    def __str__(self):
        return self.Symbol
