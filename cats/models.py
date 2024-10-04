from users.models import User
from django.db import models
from datetime import datetime


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Breed(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cat(BaseModel):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField(default=datetime.now)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='cats')
    about = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')

    @property
    def average_rating(self):
        return self.comments.aggregate(
            average_rating=models.Avg('rating'))['average_rating'] or 0

    @property
    def get_age(self):
        birth_date = self.date_of_birth
        today = datetime.today()
        return (f'Year: {today.year - birth_date.year}  month: {today.month - birth_date.month},'
                f' day: {today.day - birth_date.day}')

    def __str__(self):
        return self.name


class Image(BaseModel):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.cat.name}, {self.image}'


class Video(BaseModel):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return f'{self.cat.name}, {self.video}'


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value)
    text = models.TextField()
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    def get_replies(self):
        return self.replies.all()

    def __str__(self):
        return f'{self.cat.name}, {self.text}'
