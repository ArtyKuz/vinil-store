from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profile
from vinilboard.models import Genre, Artist, Album, Comment


class ArtistAddSerializer(serializers.ModelSerializer):
    # albums = serializers.StringRelatedField(many=True)

    class Meta:
        model = Artist
        fields = ('id', 'artist', 'slug')  # 'albums')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'genre', 'slug')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('image',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'profile',)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('content', 'mark', 'user', 'date_create')


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'artist', 'title', 'year', 'label', 'genre', 'price', 'photo', 'comments')


class ArtistSerializer(serializers.ModelSerializer):
    # albums = serializers.StringRelatedField(many=True)
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'artist', 'albums')