# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):

    RATING_CHOICES = (
        (5, 'Excelent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Not Good'),
        (1, 'Bad'),
    )

    reviewer = models.ForeignKey(User, related_name='reviewer', null=True)
    company_name = models.CharField(max_length=250)
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=250)
    submission_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(default='127.0.0.1')
    summary = models.TextField(max_length=1000)

    def __unicode__(self):
        return u'{0}-{1}'.format(self.company_name, self.title)