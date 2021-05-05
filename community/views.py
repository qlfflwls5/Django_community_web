from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe, require_http_methods
from .models import Review, Comment, Hashtag
from .forms import ReviewForm, CommentForm
from django.urls import resolve
from django.core.paginator import Paginator

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReviewListSerializer, ReviewSerializer


@require_safe
def index(request):
    reviews = Review.objects.order_by('-pk')

    # pagination 
    paginator = Paginator(reviews, 3) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews': reviews,
        'page_obj': page_obj,
    }
    return render(request, 'community/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            print(review.rank)
            review.rank = 0
            review.save()
            # 해쉬태그 생성 혹은 가져오기
            for word in review.content.split():
                if word.startswith('#'):
                    # 없으면 생성, 있으면 가져오기
                    # hashtag에는 해시태그가 담기고 created에는 생성인지의 여부인 bool값이 담긴다.(새로 생성이면 True, 기존 것을 가져오면 False)
                    hashtag, created = Hashtag.objects.get_or_create(content=word)
                    review.hashtags.add(hashtag)
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'community/create.html', context)


@require_safe
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.order_by('-pk')
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments
    }
    return render(request, 'community/detail.html', context)


@require_POST
def delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    return redirect('community:detail', review.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                #1. 해당 review에 달려있는 모든 hashtag clear
                review.hashtags.clear()

                #2.나머지는 create 과정과 동일
                for word in review.content.split():
                    if word.startswith('#'):
                        # 만약 word가 있으면 그걸 가져오고(get) 없다면 생성(create)
                        hashtag, created = Hashtag.objects.get_or_create(content=word)
                        review.hashtags.add(hashtag)
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('community:index')
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'community/update.html', context)


@require_POST
def comments_create(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('community:detail', review.pk)
        context = {
            'comment_form': comment_form,
            'review': review,
        }
        return render(request, 'community/detail.html', context)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', review_pk)


@require_POST
def likes(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        # 이 게시글에 좋아요를 눌렀었다면
        if review.like_users.filter(pk=request.user.pk).exists():
            # 좋아요 취소
            review.like_users.remove(request.user)
        else:
            # 좋아요
            review.like_users.add(request.user)
        # current_url = resolve(request.path_info).url_name
        # return redirect(current_url)
        
        #print(request.resolver_match.url_name)
        
        # if request.resolver_match.url_name == 'community:index':
        #     return redirect('community:index')
        # else:
        return redirect('community:detail', review.pk)
    return redirect('accounts:login')


@require_POST
def likes_index(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        # 이 게시글에 좋아요를 눌렀었다면
        if review.like_users.filter(pk=request.user.pk).exists():
            # 좋아요 취소
            review.like_users.remove(request.user)
        else:
            # 좋아요
            review.like_users.add(request.user)
        return redirect('community:index')
    return redirect('accounts:login')


@login_required
def hashtag(reqeust, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    reviews = hashtag.reviews.order_by('-pk')
    context = {
        'hashtag': hashtag,
        'reviews': reviews,
    }
    return render(reqeust, 'community/hashtag.html', context)


# REST API
# 전체 리뷰
@api_view(['GET'])
def review_list(request):
    reviews = get_list_or_404(Review)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)


# 단일 리뷰
@api_view(['GET'])
def review_detail(reqeust, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)