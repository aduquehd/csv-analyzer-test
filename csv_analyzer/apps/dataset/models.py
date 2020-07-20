# Django
from django.db import models
import django.db.models.options as options

# Utils
from csv_analyzer.utils.models import BaseModel

# Models
from csv_analyzer.apps.users.models import User


class DataSet(BaseModel):
    name = models.CharField(max_length=255)
    is_analyzed = models.BooleanField(default=False)

    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'data_set'
        unique_together = ('name', 'owner')


class DataSetFiles(BaseModel):
    file = models.FileField()
    data_set = models.ForeignKey(DataSet, on_delete=models.PROTECT, related_name='files')
    is_analyzed = models.BooleanField(default=False)
