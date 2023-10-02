from rest_framework import serializers
from .models import Post, User, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.first_name")
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post    
        fields = ["title", "blog", "pub_date", "author", "comments"]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "country", "birth_date"]
    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            country=validated_data["country"],
            birth_date=validated_data["birth_date"],
        )
        password = validated_data.get("password")
        if password:
            user.set_password(password)
        user.save()
        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "country",
            "birth_date",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data["email"],
                password=validated_data["password"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                country=validated_data["country"],
                birth_date=validated_data["birth_date"],
            )
            return user


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="author.first_name", read_only=True)

    class Meta:
        model = Comment
        fields = ["username", "commentblog", "comment", "comment_date"]

        def create(self, validated_data):
            cm = Comment.objects.create_user(
                comment=validated_data["comment"],
            )
            return cm
