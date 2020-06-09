from django.shortcuts import render
from .models import Article, Author
from django.contrib.auth.models import User

def homepage(request):
    articles = Article.objects.all()
    return render(request, "article/homepage.html", 
        {"articles": articles}
        )


def authors(request):
    authors = Authors.objects.all()
    return render(request, "article/authors.html",
    {"authors": authors},
    )

def users(request):
    context = {}
    context["users_all"] = User.objects.all()
    # context["authors"] = authors
    return render(request, "article/users.html", context)