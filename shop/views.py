from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Yarn, Category, Manufacturer, Tag, Comment
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.

def new_comment(request, pk):
    if request.user.is_authenticated :
        yarn = get_object_or_404(Yarn, pk=pk)
        if request.method == 'POST' :
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid() :
                comment = comment_form.save(commit=False)
                comment.yarn = yarn
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else :
            return redirect(yarn.get_absolute_url())
    else :
        raise PermissionDenied


class YarnList(ListView) :
    model = Yarn
    ordering = 'pk'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(YarnList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_yarn_count'] = Yarn.objects.filter(category=None).count()
        return context

class YarnDetail(DetailView) :
    model = Yarn

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(YarnDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_yarn_count'] = Yarn.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context

class YarnCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView) :
    model = Yarn
    fields = ['name', 'manufacturer', 'use_season', 'use_needle_size', 'content', 'image', 'category']

    def test_func(self):
        return (self.request.user.is_superuser or self.request.user.is_staff)

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(YarnCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created :
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else :
            return redirect('/shop/')

class YarnUpdate(LoginRequiredMixin, UpdateView):
    model = Yarn
    fields = ['name', 'manufacturer', 'use_season', 'use_needle_size', 'content', 'image', 'category']

    template_name = 'shop/yarn_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser :
            return super(YarnUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(YarnUpdate, self).get_context_data()
        if self.object.tags.exists() :
            tags_str_list = list()
            for t in self.object.tags.all() :
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def form_valid(self, form):
        response = super(YarnUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

class YarnSearch(YarnList) :
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        yarn_list = Yarn.objects.filter(
            Q(name__contains=q) | Q(tags__name__contains=q)
        ).distinct()

        return yarn_list

    def get_context_data(self, **kwargs):
        context = super(YarnSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'검색 결과 : {q}({self.get_queryset().count()})'

        return context


def category_page(request, slug) :
    if slug == 'no_category' :
        category = '미분류'

    else :
        category = Category.objects.get(slug=slug)

    return render(request, 'shop/yarn_list.html',
                  {
                      'yarn_list' : Yarn.objects.filter(category=category),
                      'categories' : Category.objects.all(),
                      'no_category_yarn_count' : Yarn.objects.filter(category=None).count(),
                      'category' : category
                  })

def tag_page(request, slug) :
    tag = Tag.objects.get(slug=slug)
    yarn_list = tag.yarn_set.all() # Post.objects.filter(tags=tag) <- 오류 코드

    return render(request, 'shop/yarn_list.html',
                  {
                      'yarn_list' : yarn_list,
                      'categories' : Category.objects.all(),
                      'no_category_yarn_count' : Yarn.objects.filter(category=None).count(),
                      'tag' : tag
                  })