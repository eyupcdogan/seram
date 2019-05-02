from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles =Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})

    articles = Article.objects.all()#tüm makaleleri alıcak ve listeye atıcak

    return render(request,"articles.html",{"articles":articles})

def index(request):
    context = {
        "numbers":[1,2,3,4,5]
    }
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")
@login_required(login_url = "user:login")
def dashboard(request):
    articles =Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }

    return render(request,"dashboard.html",context)
@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        """
        article objesini oluşturuyor.
        bizim articleyi oluştur ama save yapma onu ben yapıcam demek lazım
        article.save() yapıyor
        """
        messages.success(request,"Makale başarıyla oluşturuldu.")
        return redirect("index")

    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    #article = Article.objects.filter(id = id).first()
    article =  get_object_or_404(Article,id = id)

    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})
@login_required(login_url = "user:login")
def update(request,id):

    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        """
        article objesini oluşturuyor.
        bizim articleyi oluştur ama save yapma onu ben yapıcam demek lazım
        article.save() yapıyor
        """
        messages.success(request,"Makale başarıyla güncellendi.")
        return redirect("index")
    
    return render(request,"update.html",{"form":form})
@login_required(login_url = "user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)

    article.delete()

    messages.success(request,"Makale Başarıyla Silindi")

    return redirect("index")
def addComment(request,id):
    article = get_object_or_404(Article,id = id)
    
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author = comment_author,comment_content = comment_content)

        newComment.article = article

        newComment.save()

    return redirect(reverse("article:detail",kwargs={"id":id}))#Dinamik url yapısı reverse fonksiyonuyla daha iyi olur

def serabilgi(request):
    API_KEY = '4e2761ccf40b420ceb4a0e566fc14376'#api key her bi kullanıcıya özel
    url = 'https://iothook.com/api/latest/datas/?data=first&api_key=' + API_KEY#sunucuya bağlantı linki
    response = requests.get(url)
    data = response.json()#veriyi json formatında okuma
    data2=data["data"]
    data3=['my first value']
    data4=['my second chance']
    for value in data2.values():#data içinde döner
        for value2 in value.items():#data idlerini gezer ve value_3 
                if value2[0]=="value_3":
                    data3.append(value2[1])
                if value2[0]=="pub_date":#oluşturulma tarihi
                    data4.append(value2[1])
    context = {
        "data":data3[99],
        "data2":data3[98],
        "data3":data3[97],
        "data4":data3[96],
        "data5":data3[95],
        "data6":data3[94],
        "data7":data4[99][11:19],
        "data8":data4[98][11:19],
        "data9":data4[97][11:19],
        "data10":data4[96][11:19],
        "data11":data4[95][11:19],
        "data12":data4[94][11:19],
        "data13":data4[99][0:10],
    }
    return render(request,"serabilgi.html",context)