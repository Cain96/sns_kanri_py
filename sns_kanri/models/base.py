from django.db import models


class BaseManager(models.Manager):
    def get_or_none(self, **kwargs):
        """
        検索にヒットすればそのモデルを、しなければNoneを返します。
        """
        try:
            return self.get_queryset().get(**kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):
    """
    ベースとなるModel
    """

    class Meta:
        abstract = True

    objects = BaseManager()

    created = models.DateTimeField("作成日時", auto_now_add=True)
    updated = models.DateTimeField("更新日時", auto_now=True)
    enabled = models.BooleanField("有効", default=True)
