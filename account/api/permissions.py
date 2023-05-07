from rest_framework.permissions import BasePermission
from wizard.models import Project
class IsCompanyLead(BasePermission):
    message = "besuperuser"
    def has_permission(self, request, view):
        if Project.objects.filter(companyLeader=request.user).exists():
            return True
        return bool(request.user and request.user.employee.is_systemadmin == True)
    
    

    
    