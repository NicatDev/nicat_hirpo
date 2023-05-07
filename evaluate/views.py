from rest_framework import generics
from rest_framework.views import APIView
from wizard.api.serializers import *
from rest_framework.response import Response
import os

from wizard.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.views import LogoutView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.utils.timezone import localtime
today = localtime().date()

class ProjectsApiView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializerr
    
    
    def get_queryset(self):
        data=self.request.user.id
        if data:
            if Project.objects.filter(companyLeader=data).exists():
                project=Project.objects.filter(companyLeader=data)
            else:
                project = Project.objects.filter(employee = self.request.user.employee.id)
            return project
        
class Frequencies(generics.ListAPIView):
    queryset = Evaluation_frequency.objects.all()
    serializer_class = Evaluation_ffrequencySerializer
    
    
    def get_queryset(self):
        queryset = Evaluation_frequency.objects.all()
        data=self.request.user.id
 
        if data:
            if Project.objects.filter(companyLeader=data).exists():
                project_id=Project.objects.get(companyLeader=data).id
             
            else:
                project_id = Project.objects.get(employee = self.request.user.employee.id).id
       
            return queryset.filter(period__project_id = project_id)
        
class AddPeriodApiView(generics.CreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PerioddSerializer
    
    
class AddFrequencyApiView(APIView):

    def post(self,request):
        data=request.data
        serializer = Evaluation_frequencySerializer(data=data) 
        serializer.is_valid(raise_exception=True)
        eva = serializer.save()

        for dep in ProjectDepartment.objects.filter(project=eva.period.project.id):
            print(dep.id)
            for emp in Employee.objects.filter(position__department=dep.id):
                print(emp.position.department.id)
                for rater in Employee.objects.filter(position__department=emp.position.department.id):
                    print(rater.position.department.id)
                    Scoreserializer = AllScoresPostSerializer(data={'employee':emp.id,'rater':rater.id,'evaluation_frequency':eva.id})
                    Scoreserializer.is_valid(raise_exception=True)
                    score = Scoreserializer.save()
               
                    for skill in MainSkill.objects.filter(position=emp.position.id):
                        pointserializer = UserSkillSerializer(data={'card':score.id,'skill':skill.id})
                        pointserializer.is_valid(raise_exception=True)
                        pointserializer.save()
        
    
        
        return Response({'message':'success'})
    
class EvaluationList(generics.ListAPIView):
    serializer_class = AllScoressSerializer

    def get_queryset(self):
        queryset = []
        existt = Employee.objects.filter(user = self.request.user).exists()
        print(existt)
        if existt:
            queryset = AllScores.objects.filter(rater = self.request.user.employee.id)
            print(queryset)
        for x in queryset:
            if x.evaluation_frequency.start_date <= today <= x.evaluation_frequency.end_date:
                pass
            else:
                queryset=queryset.exclude(id=x.id)
        print(queryset)
        return queryset
                
            
        
    
class EmployeeListForScores(generics.ListAPIView):
    serializer_class = employeeSerializer
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        queryset = Employee.objects.all()
        data=self.request.user.id
        
        if data:
            project=Project.objects.get(companyLeader=data,id=id)
            return queryset.filter(project=project.id)
        

class EvaluateComptencyList(generics.RetrieveAPIView):
    serializer_class = AllScoresForEvaluateSerializer
    queryset = AllScores.objects.all()
    lookup_field = 'id'
    
class PerformCardUpdateView(generics.UpdateAPIView):
    def put(self, request):
        data = request.data
        print(data)
        myserializer = AllScoreUpdateSerializer
        for key,value in data.items():
            field_name, object_id = key.split('-')
            
            score = UserSkill.objects.get(id=object_id)
            serializer = myserializer(score,data={field_name:value})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({'message': 'success'})
   
class EmployeePerformance(generics.ListAPIView):
    serializer_class = EmployeeSerializerForUserPerformance
    
    def get_queryset(self):
        if Employee.objects.filter(project__companyLeader = self.request.user.id).exists():
            
            instance = Employee.objects.filter(project__companyLeader = self.request.user.id)
        else:
            instance = Employee.objects.filter(project = self.request.user.employee.project.id)
        return instance


