from django.urls import path
from .views import TodoList, LoginView , RegisterView, TodoCreate, CategoryCreate, CategoryList

urlpatterns = [
    # auth
    path('auth/register' , RegisterView.as_view() , name = "register"),
    path('auth/login/', LoginView.as_view(), name='login'),
    # path('auth/logout/', LogoutView.as_view(), name='logout'),

    # todos
    path('todo/list/', TodoList.as_view(), name='todo-list'),
    path('todo/create/', TodoCreate.as_view(), name='todo-create'),

    # category
    path('category/list/', CategoryList.as_view(), name='category-list'),
    path('category/create/', CategoryCreate.as_view(), name='category-create'),



]
