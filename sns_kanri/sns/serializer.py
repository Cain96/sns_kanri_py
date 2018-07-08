from datetime import datetime

from rest_framework import serializers

from sns_kanri.sns.models import SNS, Record


class SNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNS
        fields = (
            'name',
            'path'
        )


class CustomTimeField(serializers.TimeField):

    def to_representation(self, value):
        return datetime.strftime(value, '%Y-%m-%d %H:%M')


class SNSField(serializers.PrimaryKeyRelatedField):
    queryset = SNS.objects.all()

    def to_representation(self, value):
        return SNS.objects.get(id=value.pk).name


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    sns = SNSField()
    updated = CustomTimeField()

    class Meta:
        model = Record
        fields = (
            'user',
            'sns',
            'date',
            'time',
            'updated'
        )
        read_only_fiedls = (
            'user',
            'updated',
        )
