from rest_framework.views import APIView
from .models import Todo
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from .serializers import (
    RegisterSerializer,
    CategorySerializer,
    TodoSerializer,
    LoginSerializer,
)
from .models import Category


class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CategorySerializer(many=True))
    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)


class CategoryCreate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def post(self, request):
        # context orqali request'ni serializer'ga uzatamiz
        serializer = CategorySerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)


class TodoCreate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=TodoSerializer, responses=TodoSerializer)
    def post(self, request):
        serializer = TodoSerializer(
            data=request.data,
            context={"request": request},  # ← shu qatorni qo'shing
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)


class TodoList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=TodoSerializer(many=True))
    def get(self, request):
        todos = Todo.objects.filter(user=request.user).select_related(
            "category", "user"
        )
        serializer = TodoSerializer(
            todos,
            many=True,
            context={"request": request},  # ← bu yerga ham
        )
        return Response(serializer.data, status=200)


class LoginView(APIView):
    @extend_schema(request=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "success": True,
                "message": "Login is successful",
                "token": token.key,
            },
            status=200,
        )


class RegisterView(APIView):
    @extend_schema(request=RegisterSerializer, responses=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response(
            {
                "success": True,
                "message": "Registered successfully",
                "token": token.key,
            },
            status=201,
        )
