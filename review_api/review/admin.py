# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'title', 'company_name', 'rating', 'submission_date',)