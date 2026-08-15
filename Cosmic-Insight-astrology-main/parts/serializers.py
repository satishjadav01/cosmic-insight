from rest_framework import serializers
from .models import signup

class UserSignupSerializer(serializers.Serializer):
    class Meta:
        model = signup
        field = ['name','mobile','password']
        extra_kwags = {'password':{'write_onle':True}}

class MarriageScoreSerializer(serializers.Serializer):
    dob_male = serializers.DateTimeField(format="%Y-%m-%d")
    dob_female = serializers.DateTimeField(format="%Y-%m-%d")

    def to_representation(self, instance):
        return {
            "compatibility_score":instance.get('points'),
            "male_data":{
                "mulank":instance.get('malemulank'),
                "bhagyank":instance.get('malebhagiyank'),
                "matrix":instance.get('male_matrix')
            },
            "female_data":{
                "mulank":instance.get('femalemulank'),
                "bhagyank":instance.get('femalebhagiyank'),
                "matrix":instance.get('female_matrix')
            }
        }