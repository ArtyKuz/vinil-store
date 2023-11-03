from rest_framework import serializers

from vinilboard.models import Genre, Artist, Album


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='artist', queryset=Artist.objects.all())
    genre = serializers.SlugRelatedField(slug_field='genre', queryset=Genre.objects.all())

    class Meta:
        model = Album
        fields = ('id', 'artist', 'title', 'year', 'label', 'genre', 'price', 'photo')


class ArtistSerializer(serializers.ModelSerializer):
    # albums = serializers.StringRelatedField(many=True)
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'artist', 'albums')


class ArtistAddSerializer(serializers.ModelSerializer):
    # albums = serializers.StringRelatedField(many=True)

    class Meta:
        model = Artist
        fields = ('id', 'artist', 'slug')  # 'albums')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'genre', 'slug')
