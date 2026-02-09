from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Expenses, User, Plan, PlanItems
from .serializers import UserSerializer, ExpensesSerializrer, PlanSerializer, PlanItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from datetime import datetime
from django.utils.timezone import now as timezone_now
from datetime import date
from api import serializers

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    # permission_classes = [IsAuthenticated]


class PlanViewSet(viewsets.ModelViewSet):
    # queryset=Plan.objects.all()
    serializer_class=PlanSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlanItemViewSet(viewsets.ModelViewSet):
    # queryset=PlanItems.objects.all()
    serializer_class=PlanItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        plan_id=self.kwargs.get('plan_pk')
        return PlanItems.objects.filter(plan_id=plan_id)  
    def perform_create(self, serializer):
        plan_id=self.kwargs.get('plan_pk')
        plan=Plan.objects.get(id=plan_id)
        serializer.save(plan=plan) 


class ExpensesViewSet(viewsets.ModelViewSet):
            
            # queryset=Expenses.objects.all()
            serializer_class=ExpensesSerializrer
            permission_classes = [IsAuthenticated]
            def get_queryset(self):
                user = self.request.user
                queryset = Expenses.objects.filter(user=user).order_by('-created_at')

               
                year = self.request.query_params.get('year')
                month = self.request.query_params.get('month')
                day = self.request.query_params.get('day')
                hour = self.request.query_params.get('hour')

                if year:
                    queryset = queryset.filter(created_at__year=int(year))
                if month:
                    queryset = queryset.filter(created_at__month=int(month))
                if day:
                    queryset = queryset.filter(created_at__day=int(day))
                if hour:
                    queryset = queryset.filter(created_at__hour=int(hour))

                return queryset
         
    
            def list(self, request, *args, **kwargs):
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                today = timezone_now().date()
                year = int(request.GET.get('year', today.year))
                month = int(request.GET.get('month', today.month))
                day = int(request.GET.get('day', today.day))
                searched_date = date(year, month, day)
                total_monthly=sum(expense.amount for expense in Expenses.objects.filter(
                    user=request.user,
                    created_at__year=year,
                    created_at__month=month
                ))  
                daily_total=sum(expense.amount for expense in Expenses.objects.filter(
                    user=request.user,
                    created_at__date=searched_date,
                ))

                plan = Plan.objects.filter(
                    user=request.user,
                    # date__gte=searched_date
                    date__year =year,
                    date__month = month
                ).first()

                if plan:
                    if daily_total > plan.target:
                        note = f"you have exceeded your daily target ({plan.target}) with a total of {daily_total} expenses."
                    else:
                        note = f"You are within your daily target ({plan.target}) . Keep it up!"
                else:
                    note = "No plan set for today."

                return Response({
                    "expenses": serializer.data,
                    "total_monthly": total_monthly,
                    "daily_total": daily_total,
                    "note": note,
                    "plan_date": plan.date if plan else None


                })

    

            def perform_create(self, serializer):
                serializer.save(user=self.request.user)
        

class IsExecedThePlanItemsAmount(viewsets.ModelViewSet):
    # queryset=Expenses.objects.all()
        permission_classes = [IsAuthenticated]
        def list(self, request, *args, **kwargs):
            today = timezone_now().date()
            year = int(request.GET.get('year', today.year))
            month = int(request.GET.get('month', today.month))
            category=request.GET.get('category')
            user_plan = Plan.objects.filter(
                user=request.user,
                date__year=year,
                date__month=month
            ).first()

            amout_of_plan_item=PlanItems.objects.filter(
                plan=user_plan,
                category=category
            ).first().amount if user_plan else None

            total_expenses=sum(expense.amount for expense in Expenses.objects.filter(
                user=request.user,
                category=category,
                created_at__year=year,
                created_at__month=month
            ))

            if amout_of_plan_item:
                if total_expenses > amout_of_plan_item:
                    note = f"You have exceeded your plan item amount ({amout_of_plan_item}) for category '{category}' with total expenses of {total_expenses}."
                else:
                    note = f"You are within your plan item amount ({amout_of_plan_item}) for category '{category}'. Keep it up!"
            else:
                note = f"No plan item set for category '{category}'."


           
        










    



