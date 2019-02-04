from rest_framework import serializers
from datetime import date
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):

    due_date = serializers.DateField()

    class Meta:
        model = Todo
        fields = ('id', 'title', 'state', 'due_date', 'description',)

    def create(self, validated_data):
        """
        create and return a new `Todo` instance.
        :param validated_data:
        :return:
        """
        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        update and returns the existing `Todo` instance
        :param instance:
        :param validated_data:
        :return:
        """
        instance.title = validated_data.get('title', instance.title)
        instance.state = validated_data.get('state', instance.state)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate_due_date(self, due_date):
        today = date.today()
        if due_date <= today:
            raise serializers.ValidationError('Due date can not be less the current date.')
