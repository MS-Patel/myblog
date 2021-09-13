from django.db.models import query
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, JsonResponse
from blog.forms import NewCommentForm, PostSearchForm
from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
# Create your views here.


def home(request):
    all_posts = Post.newmanager.all()
    return render(request, 'index.html', {'posts': all_posts})


def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')
    allcomments = post.comments.filter(status=True)
    paginator = Paginator(allcomments, 2)  # Show 2 contacts per page.
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()

    return render(
        request,
        'single.html',
        {
            'post': post,
            'comments': user_comment,
            'comments': comments,
            'comment_form': comment_form,
            'allcomments': allcomments,
            'page_obj': page_obj,
        },
    )


class CatListView(ListView):
    template_name = 'category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context


def post_search(request):
    form = PostSearchForm()
    Query = ''
    c = ''
    results = []
    query = Q()

    if request.POST.get("action") == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = Post.newmanager.filter(
                title__contains=search_string)[:3]

            data = serializers.serialize('json', list(
                search_string), fields=('id', 'title', 'slug'))
            
            return JsonResponse({'search_string':data})

    if 'Query' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            Query = form.cleaned_data['Query']
            c = form.cleaned_data['Category']
            if c:
                query &= Q(category=c)
            if Query:
                query &= Q(title__contains=Query)

            results = Post.newmanager.filter(query)

    return render(request, 'search.html',
                  {'form': form,
                   'Query': Query,
                   'c': c,
                   'results': results})
