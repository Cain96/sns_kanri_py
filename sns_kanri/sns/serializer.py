from rest_framework import serializers

from sns_kanri.sns.models import SNS, Record


class SNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNS
        fields = (
            'name',
        )


class RecordSerializer(serializers.ModelSerializer):
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
