import datetime

from django.db import models

from sns_kanri.master.models import User
from sns_kanri.models import BaseModel


class SNS(BaseModel):
    class Meta:
        verbose_name = verbose_name_plural = "SNS"
        ordering = [
            "created",
        ]

    name = models.CharField("名称", max_length=256)
    color = models.CharField("カラー", max_length=7, blank=True)

    def __str__(self):
        return self.name


class Record(BaseModel):
    class Meta:
        verbose_name = verbose_name_plural = "記録"
        ordering = [
            "-created",
        ]

    user = models.ForeignKey(User, verbose_name="ユーザ", on_delete=models.PROTECT)
    sns = models.ForeignKey(SNS, verbose_name="SNS", on_delete=models.PROTECT)
    date = models.DateField("日付")
    time = models.TimeField("時間")

    def __str__(self):
        return str(self.id)

class Statistic(object):
    def __init__(self, date: datetime.date, sns: list):
        self.date = date
        self.sns = sns
