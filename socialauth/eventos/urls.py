from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socialauth.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^listado/$', login_required(views.EventosView.as_view()), name='listado'),
    url(r'^evento/(?P<pk>\d+)/$', login_required(views.DetallesView.as_view()), name='evento'),
    url(r'^evento/(?P<pk>\d+)/registrar$', views.registrar, name='registrar'),
)
