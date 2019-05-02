from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from article import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name = "index"),
    path('about/',views.about,name = "about"),
    path('articles/',include("article.urls")),
    #article görülürse articles.urlse bak
    path('user/',include("user.urls")),
    #user/register veya login veya logoutta user.urlse git
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)