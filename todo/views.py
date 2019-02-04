from rest_framework.views import APIView
from .serializers import TodoSerializer
from django.http import JsonResponse, Http404
from rest_framework import status
from datetime import datetime
from .models import Todo


class ResponseWrapper:
    @staticmethod
    def get_response(response, status=True, status_code=status.HTTP_200_OK):
        return JsonResponse({
            'status': status,
            'response': response
        }, status=status_code)


class TodoList(APIView, ):
    def get(self, request):
        try:
            snippets = Todo.objects.all()
            if request.GET.get('state'):
                snippets = snippets.filter(state__exact=request.GET.get('state'))
            if request.GET.get('due_date') and self.valid_date():
                due_date = self.valid_date()
                snippets = snippets.filter(due_date__year=due_date.year,
                                           due_date__month=due_date.month,
                                           due_date__day=due_date.day)
            serializer = TodoSerializer(snippets, many=True)
            return ResponseWrapper.get_response(serializer.data)
        except ValueError as e:
            return ResponseWrapper.get_response(str(e), False, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return ResponseWrapper.get_response(str(e), False, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseWrapper.get_response(serializer.data, True, status.HTTP_201_CREATED)
        return ResponseWrapper.get_response(serializer.errors, False, status.HTTP_400_BAD_REQUEST)

    def valid_date(self):
        if self.request.query_params.get('due_date', None) is None:
            return False
        try:
            return datetime.strptime(self.request.query_params.get('due_date'), '%Y-%m-%d')
        except ValueError:
            raise ValueError('Incorrect date format, should be YYYY-MM-DD.')


class TodoDetails(APIView):
    def get_todo(self, id):
        try:
            return Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, id):
        todo = self.get_todo(id)
        serializer = TodoSerializer(todo)
        return ResponseWrapper.get_response(serializer.data)

    def put(self, request, id):
        todo = self.get_todo(id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseWrapper.get_response(serializer.data)
        return ResponseWrapper.get_response(serializer.errors, False, status.HTTP_400_BAD_REQUEST)


class TodoDelete(APIView):

    def delete(self, request):
        Todo.objects.filter(id__in=request.data['delete']).delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
