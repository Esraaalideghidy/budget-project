from .models import User, Expenses, Plan, PlanItems
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    class Meta:
        model=User
        fields=['id','username','email','password','phone']
    def create(self, validated_data):
        validated_data['is_staff']=False
        validated_data['is_superuser']=False
        user=User.objects.create_user(**validated_data)
        return user
    
class ExpensesSerializrer(serializers.ModelSerializer):
    # note = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField()
    class Meta:
        model=Expenses
        fields=['id','user','category','amount','created_at']
        read_only_fields = ['user','created_at']


    def get_user(self, obj):
        return obj.user.username
class PlanSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # plan=PlanItemSerializer(many=True,read_only=True,source='planitems_set')
    class Meta:
        model=Plan
        fields=['id','user','target','date']
        read_only_fields = ['user']

    def get_user(self, obj):
        return obj.user.username

class PlanItemSerializer(serializers.ModelSerializer):
    plan=PlanSerializer(read_only=True)
    class Meta:
        model=PlanItems
        fields=['id','plan','category','amount']


