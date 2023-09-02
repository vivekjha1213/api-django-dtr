from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from Departments.models import Department


from .serializers import (
    DepartmentListSerializer,
    DepartmentRegisterSerializer,
    DepartmentSearchSerializer,
    DepartmentUpdateSerializer,
)


class DepartmentRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DepartmentRegisterSerializer(data=request.data)

        # Extract the client_id and department_name from the request
        client_id = request.data.get('client_id')  # Adjust this based on your actual client identification method
        department_name = request.data.get('department_name')

        # Check if a department with the same name already exists for the same client
        existing_department = Department.objects.filter(client_id=client_id, department_name=department_name).first()

        if existing_department:
            return Response({"error": "Department with the same name already exists for this client"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Department added successfully"}, status=status.HTTP_201_CREATED)




class DepartmentListView(APIView):
    def get_queryset(self):
        return Department.objects.all()  # Retrieve all departments

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DepartmentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class DepartmentListByIDView(APIView):
    def get_queryset(self):
        return Department.objects.all()  # Retrieve all departments

    def get(self, request, *args, **kwargs):
        department_id = kwargs.get('department_id')  # Get the department ID from the URL
        if department_id is not None:
            queryset = self.get_queryset().filter(pk=department_id)
            serializer = DepartmentListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Department ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        




class DepartmentUpdateView(APIView):
   def put(self, request, *args, **kwargs):
        return self.update_department(request, kwargs.get('department_id'))
    
   def patch(self, request, *args, **kwargs):
        return self.update_department(request, kwargs.get('department_id'), partial=True)
    
   def update_department(self, request, department_id, partial=False):
        try:
            department = Department.objects.get(department_id=department_id)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentRegisterSerializer(department, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Department updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DepartmentDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        department_id = kwargs.get('department_id')
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        
        department.delete()
        return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class DepartmentTotalView(APIView):
    def get(self, request, *args, **kwargs):
        total_departments = Department.objects.count()
        return Response({"total_departments": total_departments}, status=status.HTTP_200_OK)
    
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
    #@Get Data by Client Id.....
def get_department_by_client_id(client_id):
    return Department.objects.filter(client_id=client_id)

class ClientDepartmentListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        
        if client_id:
            department = get_department_by_client_id(client_id)
            
            if department.exists():
                serializer = DepartmentListSerializer(department, many=True)
                return Response({"Data": serializer.data})
            else:
                return Response({"error": "No department found for the given client_id"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "client_id is missing in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        

   
        
class ClientDepartmentListByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id") 
        
        if not (department_id and client_id):
            return Response({"error": "Both department_id and client_id are required in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        departments = Department.objects.filter(client_id=client_id)
        
        if department_id:
            departments = departments.filter(department_id=department_id)  # Use the 'id' field to filter the department
        
        if not departments.exists():
            return Response({"error": "No departments found for the given criteria"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = DepartmentListSerializer(departments, many=True)
        return Response({"Data": serializer.data})
    



# @get Toatl Count Department api by cliendID 
class TotalDepartmentCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data
        
        if client_id is not None:
            total_count = Department.objects.filter(client_id=client_id).count()
            return Response(
                {"success": True, "total_count": total_count},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"success": False, "message": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
            


        

class ClientDepartmentUpdateIDView(APIView):
    def get_department(self, client_id, department_id):
        try:
            return Department.objects.get(client_id=client_id, department_id=department_id)
        except Department.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")
        
        if not (department_id and client_id):
            return Response({"error": "Both department_id and client_id are required in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        department = self.get_department(client_id, department_id)
        if not department:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentUpdateSerializer(department, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Department updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")
        
        if not (department_id and client_id):
            return Response({"error": "Both department_id and client_id are required in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        department = self.get_department(client_id, department_id)
        if not department:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentUpdateSerializer(department, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Department updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    

class ClientDepartmentDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")
        
        if not (department_id and client_id):
            return Response({"error": "Both department_id and client_id are required in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            department = Department.objects.get(client_id=client_id, department_id=department_id)
            department.delete()
            return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        
 # Search Api...................... by client id and    Department id...
class ClientDepartmentSearchView(APIView):
    def get(self, request):
        search_query = request.GET.get("query")
        client_id = request.GET.get("client_id")
        
        if not search_query or not client_id:
            return Response(
                {"success": False, "message": "Both search query and client_id parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        departments = Department.objects.filter(department_name__icontains=search_query, client_id=client_id)
        
        if not departments.exists():
            return Response(
                {"success": False, "message": "No departments found for the given criteria."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = DepartmentSearchSerializer(departments, many=True)
        response_data = {
            "success": True,
            "count": len(departments),
            "results": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)