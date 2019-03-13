from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment


# from IPython import embed
# Create your views here.


def article_list(request):
    context = {}
    articles = Article.objects.all()
    context['articles'] = articles
    return render(request, 'board/list.html', context=context)


def article_detail(request, article_id):
    context = {}
    article = get_object_or_404(Article, id=article_id)

    context['article'] = article

    return render(request, 'board/detail.html', context=context)


def create_article(request):
    if request.method == 'GET':
        return render(request, 'board/new.html')
    else:
        article = Article()

        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()

    return redirect('board:article_list')


def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'GET':
        return redirect('board:article_detail', article_id)
    elif request.method == 'POST':
        article.delete()
        return redirect('board:article_list')


def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'GET':
        context = {}
        context['article'] = article
        return render(request, 'board/edit.html', context=context)
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')

        article.title = title
        article.content = content
        article.save()

        return redirect('board:article_detail', article_id)
