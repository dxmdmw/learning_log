from django.contrib import admin
from . import models
# Register your models here.
from learning_logs.models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(models.ExampleModel)
