from datetime import datetime

from rest_framework import serializers

from sns_kanri.sns.models import SNS, Record


class SNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNS
        fields = (
            'id',
            'name',
            'color'
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

    updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Record
        fields = (
            'id',
            'user',
            'sns',
            'date',
            'time',
            'updated'
        )


class StatisticSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    sns = serializers.ListField(read_only=True)
