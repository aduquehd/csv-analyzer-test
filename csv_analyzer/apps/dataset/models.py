# Django
from django.db import models
import django.db.models.options as options

# Utils
from csv_analyzer.utils.models import BaseModel

# Models
from csv_analyzer.apps.users.models import User

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('using',)


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


class DataSetWearerData(BaseModel):
    air_pressure_9am = models.DecimalField(decimal_places=10, max_digits=20)
    air_temp_9am = models.DecimalField(decimal_places=10, max_digits=20)
    avg_wind_direction_9am = models.DecimalField(decimal_places=10, max_digits=20)
    avg_wind_speed_9am = models.DecimalField(decimal_places=10, max_digits=20)
    max_wind_direction_9am = models.DecimalField(decimal_places=10, max_digits=20)
    max_wind_speed_9am = models.DecimalField(decimal_places=10, max_digits=20)
    rain_accumulation_9am = models.DecimalField(decimal_places=10, max_digits=20)
    rain_duration_9am = models.DecimalField(decimal_places=10, max_digits=20)
    relative_humidity_9am = models.DecimalField(decimal_places=10, max_digits=20)
    relative_humidity_3pm = models.DecimalField(decimal_places=10, max_digits=20)

    data_set = models.ForeignKey(DataSet, on_delete=models.PROTECT)

    class Meta:
        db_table = 'data_set_wearer_data'
        using = 'mongodb'


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        db_table = 'blog'
        using = 'mongodb'
