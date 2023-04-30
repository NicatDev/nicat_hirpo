from rest_framework.permissions import BasePermission

class IsCompanyLead(BasePermission):
    message = "besuperuser"
    def has_permission(self, request, view):
        return bool(request.user and request.user.employee.is_systemadmin == True)
    
    

    
    