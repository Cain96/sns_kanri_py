from datetime import datetime

from rest_framework import serializers

from sns_kanri.sns.models import SNS, Record


class SNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNS
        fields = (
            'id',
            'name',
            'color',
            'enabled'
        )


class RecordOutputSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    sns = SNSSerializer(read_only=True)

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

        read_only = (
            'id',
            'user',
            'sns',
            'date',
            'time',
            'updated'
        )


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

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


class RateSerializer(serializers.Serializer):
    sns = SNSSerializer(read_only=True)
    num = serializers.FloatField(read_only=True)


class TimeSerializer(serializers.Serializer):
    day = serializers.FloatField(read_only=True)
    week = serializers.FloatField(read_only=True)
    month = serializers.FloatField(read_only=True)
