from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.

# 제조사 모델
class Manufacturer(models.Model) :
    id = models.IntegerField(primary_key = True) # 기본키로 사용할 id(추가1)
    name = models.CharField(max_length=50, unique=True) # 제조사명
    zip_code = models.CharField(max_length=10) # 우편번호(추가2)
    address = models.TextField() # 주소
    contact = models.CharField(max_length=20) # 연락처

    def __str__(self):
        return self.name


# 카테고리 모델
class Category(models.Model) :
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self) :
        return self.name

    def get_absolute_url(self):
        return f'/shop/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model) :
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/tag/{self.slug}'


# 상품(실) 모델
class Yarn(models.Model) :
    name = models.CharField(max_length=30)  # 상품명(title)
    content = MarkdownxField(null=True)  # 간단한 설명

    weight = models.IntegerField(null=True) # 실 무게 (추가1)
    length = models.IntegerField(null=True) # 실 길이 (추가2)
    use_season = models.CharField(max_length=10, null=True)  # 주로 사용되는 계절(추가3)
    use_needle_size = models.FloatField(null=True)  # 주로 사용되는 바늘사이즈(추가4)

    image = models.ImageField(upload_to='shop/images/%Y/%m/%d/', blank=True) # 상품 이미지
    price = models.IntegerField()  # 상품 가격

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL)  # 제조사(명), 외래키
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # 카테고리, 외래키
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.name}'

    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)



class Comment(models.Model):
    yarn = models.ForeignKey(Yarn, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.yarn.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists() :
            return self.author.socialaccount_set.first().get_avatar_url()

        else :
            return f'https://doitdjango.com/avatar/id/410/611d774d3917b5cd/svg/{self.author.email}/'