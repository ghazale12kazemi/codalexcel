from django.db import models

class Codal(models.Model):

    symbol = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    publish_date_time = models.DateTimeField()

    def __str__(self):
        return self.Symbol
