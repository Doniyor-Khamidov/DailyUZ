from django.contrib import admin
from django.urls import path
from main.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_details'),
    path('404/', FailPageView.as_view(), name='404'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('contact/', contact_view, name='contact'),
]
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)