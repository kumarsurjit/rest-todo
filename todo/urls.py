from django.urls import path
from .views import TodoList, TodoDetails, TodoDelete


urlpatterns = [
    path('', TodoList.as_view()),
    path('<int:id>', TodoDetails.as_view()),
    path('delete', TodoDelete.as_view())
]
