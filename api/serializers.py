# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Todo
from django.contrib.auth import authenticate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        # unique_together ni serializer darajasida tekshirish
        user = self.context["request"].user
        qs = Category.objects.filter(name=value, user=user)
        # Update paytida o'zini hisobga olmaslik uchun
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Sizda bu nomli kategoriya allaqachon mavjud"
            )
        return value


class TodoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        # queryset'ni dinamik qilamiz — pastda __init__ da
        queryset=Category.objects.none(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "description",
            "is_done",
            "priority",
            "deadline",
            "created_at",
            "updated_at",
            "category",
            "category_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # category_id ning queryset'ini faqat shu user kategoriyalari bilan cheklash
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["category_id"].queryset = Category.objects.filter(
                user=request.user
            )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=6, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]
        extra_kwargs = {
            "first_name": {"required": True},
            "email": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get('username'),
            password=attrs.get('password'),
        )
        if not user:
            raise serializers.ValidationError("Username or password error")
        attrs['user'] = user
        return attrs
