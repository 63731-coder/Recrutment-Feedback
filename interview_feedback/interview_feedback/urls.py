
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # 2. On délègue tout ce qui commence par 'feedback/' à ta nouvelle app
    path('', include('feedback_portal.urls')),
]
