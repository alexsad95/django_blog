from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Post, Tag
from .forms import TagForm, PostForm
from .utils import *


# home page, output all posts and tags, also search
def post_list(request):
    # processing requests with parameter for searching and displaying tags
    search_query = request.GET.get('search', '')
    tag_query = request.GET.get('tag', '')

    # string with parameter request
    string_url = None

    # request for posts data, depending on the GET parameters
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )
        string_url = '?search='+search_query
    elif tag_query:
        posts = Post.objects.filter(tags__slug__contains=tag_query)
        string_url = '?tag='+tag_query
    else:
        posts = Post.objects.all()

    tags = Tag.objects.all()

    # creating objects for pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    # processing links for pagination
    if page.has_previous():
        if string_url:
            prev_url = string_url + '&page={}'.format(page.previous_page_number())
        else:
            prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        if string_url:
            next_url = string_url + '&page={}'.format(page.next_page_number())
        else:
            next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'tags': tags,
        'string_url': string_url+'&page=' if string_url else None, # for handle pagination when searching or tags
    }
    return render(request, 'blog/index.html', context=context)


# ------manipulations with posts------------
class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    redirect_url = 'post_list_url'
    raise_exception = True


# ------manipulations with tags------------
class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = 'tags_list_url'
    raise_exception = True
