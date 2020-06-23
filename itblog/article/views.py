from django.shortcuts import render, redirect
from .models import Article, Author
from django.contrib.auth.models import User
from .forms import *

def homepage(request):
    articles = Article.objects.filter(active=True).order_by("-likes") #"-likes"[:3]
    # article = Article.objects.raw("SELECT * FROM article_article WHERE active = 1") нужно соблюдать меры от инъекций 
    if request.method == "POST":
        key = request.POST.get("key_word")
        articles = Article.objects.filter(active=True).filter(
            title__contains=key) | Article.objects.filter(active=True).filter(
                text__contains=key) | Article.objects.filter(active=True).filter(
                    tag__name__contains=key) | Article.objects.filter(active=True).filter(
                        author__name__contains=key) | Article.objects.filter(active=True).filter(
                            comments__text__contains=key)
    else:
        articles = Article.objects.filter(active=True).order_by("-likes")
    
    return render(request, "article/homepage.html", 
        {"articles": articles})

def article(request, pk):
    article = Article.objects.get(id=pk) #первое id это атрибут объекта Article, к-е джанго создает самостоят, а второе см urls.py
    article.views += 1
    user = request.user
    if not user.is_anonymous:
        article.readers.add(user)
    article.save()
    if request.method == "POST":
        if "delete_btn" in request.POST:
            article.active = False
            article.save()
            return rediect(homepage)
        elif "comment_btn" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(user=request.user, article=article, text=form.cleaned_data["text"]) #cleaned_data берет данные по ключу, так как form берет данные в request.POST, к-й является словарем. типа get
                comment.save() #создали объект класса, прописали атрибуты класса. в БД это запись в таблице и 2 значения это FK
        

    context = {}
    context["article"] = article #атрибут id = переменной id
    context["form"] = CommentForm()
    return render(request, "article/article.html", context)

def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "success.html")
        # article = Article()
        # article.title = request.POST.get("title")
        # article.text = request.POST.get("text")
        # author_id = request.POST.get("author")
        # author = Author.objects.get(id=author_id)
        # article.author = author
        # article.save()
        # return render(request, "success.html")

    form = ArticleForm()
    return render(request, "article/add_article.html", {"form": form})

def edit_article(request, id):
    article = Article.objects.get(id=id)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

    form = ArticleForm(instance=article) 
    return render(request, "article/add_article.html", {"form": form})

def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html",
    {"authors": authors})

def profile(request, pk):
    author = Author.objects.get(id=pk) #get как запрос в базу данных
    return render(request, "article/profile.html", {"author": author})

def add_author(request):
    if request.method == "GET": #get как http запрос
        form = AuthorForm()
        context = {}
        context["form"] = form
        return render(request, "article/add_author.html", context)

    elif request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

        # name = request.POST.get("name") #get для получения данных по ключу
        # user_id  = request.POST.get("user")
        # user = User.objects.get(id=user_id)
        # author = Author(name=name, user=user)
        # author.save()
        # return render(request, "success.html")


def users(request):
    context = {}
    context["users_all"] = User.objects.all()
    return render(request, "article/users.html", context)


def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == "POST":
        form = CommentForm(request, instance=comment)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

    form = CommentForm(instance=comment)
    return render(request, "article/comment_form.html", {"form": form})

def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    return render(request, "success.html")
    