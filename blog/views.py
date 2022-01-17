from django.shortcuts import render, get_object_or_404
from django.core.paginator import Page, Paginator,EmptyPage,PageNotAnInteger
import os
import sys

#emails
from django.core.mail import send_mail
from django.conf import settings

from .forms import EmailPostForm,CommentForm,SearchForm
from .models import Post,Comment
from django.db.models import Count
from django.views.generic import ListView

# tagit
from taggit.models import Tag
# postgres
from django.db.models import Q
from django.db.models.functions import Greatest
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity

# Create your views here.

# class base view of post list. This code is so short but does the same thing as the function based view
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

# function based view of post list
def post_list(request, tag_slug = None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,3)# 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver the last page of result
        posts = paginator.page(paginator.num_pages) 
    return render(request, 'blog/post/list.html',{'posts':posts,'tag':tag,'page':page})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    
    # list of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        # A new post was added 
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            # create a new comment object but don't save to the database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # print(similar_posts)
    # annotate is like give me every distinct value in this queryset
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]



    return render(request, 'blog/post/detail.html',{'post':post,
                                                    'comments':comments,
                                                    'new_comment':new_comment,
                                                    'comment_form':comment_form,
                                                    'similar_posts':similar_posts})

def post_share(request,post_id):
    #retrieve post by id
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            # # send mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            name = cd['name']
            receiver = cd['to']

            send_mail(
                subject=f"{name} recommends you read {post.title}",
                message=f"Read {post.title} at <a href='{post_url}'>this link<a> <br><br>" \
                            f"{cd['name']}\'s comments: {cd['comments']}",
                content_subtype = "html",
                from_email= settings.DEFAULT_FROM_EMAIL,
                recipient_list=[receiver,]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        # Search according to 
        if form.is_valid():
            query = form.cleaned_data['query']
        try:
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.01).order_by('-rank')
            if results < 1:
                raise Exception("NotEnough")
        except:
            results = Post.published.filter(Q(title__icontains=query)|Q(body__icontains=query)).reverse()
        
        paginator = Paginator(results,3)# 3 posts in each page
        page = request.GET.get('page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            #if page is not an integer deliver the first page
            results = paginator.page(1)
        except EmptyPage:
            #if page is out of range deliver the last page of result
            results = paginator.page(paginator.num_pages)
    return render(request,'blog/post/search.html',{'form':form,'query':query,'results':results,})
