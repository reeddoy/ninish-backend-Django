from rest_framework import serializers
from quizzes.models import Quiz,Option,ConductingTime,Category

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        # fields= "__all__"
        exclude = ['isCorrect']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields= "__all__"
        exclude = ['id']

class QuizSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Quiz
        fields= "__all__"
        # exclude = ['category']

class ConductingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConductingTime
        # fields= ["start","end",]
        exclude = ['id',]