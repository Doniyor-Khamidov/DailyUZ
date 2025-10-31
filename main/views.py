from urllib import request
from main.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView


from main.models import Article, Newsletter


class HomeView(View):
    def get(self, request):
        q = request.GET.get('q')
        if q:
            articles = Article.objects.filter(title__icontains=q).order_by('-created_at')
            return render(request, 'search_result.html', context={'articles': articles})

        important_article = get_object_or_404(Article, important=True)
        top_articles = Article.objects.filter(important=False).order_by('-views')[:10]
        latest_articles = Article.objects.order_by('-created_at')[:10]
        categories = Category.objects.all()
        tags = Tag.objects.all()
        important_article1 = Article.objects.filter(category__name='Jahon').order_by('-created_at').first()
        important_article2 = Article.objects.filter(category__name='Avto').order_by('-created_at').first()
        important_article3 = Article.objects.filter(category__name='Texnologiya').order_by('-created_at').first()
        important_article4 = Article.objects.filter(category__name='Iqtisodiyot').order_by('-created_at').first()

        context = {
            'important_article': important_article,
            'top_articles': top_articles,
            'latest_articles': latest_articles,
            'categories': categories,
            'tags': tags,
            'important_article1': important_article1,
            'important_article2': important_article2,
            'important_article3': important_article3,
            'important_article4': important_article4,
        }

        return render(request, 'index.html', context)


    def post(self, request):
        Newsletter.objects.create(email=request.POST['email'])
        return redirect('home')


class ArticleDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        contexts = Context.objects.filter(article=article)
        categories = Category.objects.all()
        tags = Tag.objects.all()

        context = {
            'article': article,
            'contexts': contexts,
            'categories': categories,
            'tags': tags,
        }

        return render(request, 'detail-page.html', context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        Comment.objects.create(
            article=article,
            name=request.POST['name'],
            email=request.POST['email'],
            text=request.POST['text'],
                               )
        return redirect('article_details', slug=slug)

class FailPageView(View):
    def get(self, request):


        return render(request, '404.html')

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category).order_by('-views')

    context = {
        'category': category,
        'articles': articles,
    }
    return render(request, 'category_detail.html', context)


def contact_view(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )

        return redirect('contact')
    return render(request, 'contact.html')

# def base_view(request):
#     if request.method == 'POST':
#