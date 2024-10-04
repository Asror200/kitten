from rest_framework import serializers
from .models import Cat, Breed, Image, Video, Comment


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['image']
        extra_kwargs = {'id': {'read_only': True},
                        'cat': {'read_only': True}}

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if obj.image else None


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video']
        extra_kwargs = {'id': {'read_only': True},
                        'cat': {'read_only': True}, }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'rating', 'text', 'user', 'cat']


class CatDetailSerializer(serializers.ModelSerializer):
    breed = BreedSerializer()
    images = ImageSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    average_rating = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    get_age = serializers.CharField(read_only=True)

    class Meta:
        model = Cat
        fields = ['id', 'user', 'get_age', 'name', 'color', 'average_rating', 'images', 'videos', 'about', 'breed',
                  'comments']


class CatCreateUpdateSerializer(serializers.ModelSerializer):
    get_age = serializers.CharField(read_only=True)
    date_of_birth = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = Cat
        fields = ['name', 'get_age', 'breed', 'about', 'color', 'date_of_birth']
        read_only_fields = ['user', 'get_age']
        extra_kwargs = {'date_of_birth': {'write_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        cat = Cat.objects.create(user=user, **validated_data)
        return cat


class CatSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Cat
        fields = ['id', 'name', 'images', 'get_age', 'about', 'color', 'average_rating']


class BreedDetailSerializer(serializers.ModelSerializer):
    cats = CatSerializer(many=True, read_only=True)

    class Meta:
        model = Breed
        fields = ['id', 'name', 'cats']
