from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #user registration url
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #/music/<id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #/music/album/add
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    #/music/album/song/add
    url(r'album/(?P<album_id>[0-9]+)/song/add/$', views.SongFormView.as_view(), name='song-add'),
    #/music/album/2/
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    url(r'album/(?P<album_id>[0-9]+)/favorite_album/$', views.AlbumFavoriteView.as_view(), name='favorite_album'),
    #/music/album/2/delete/
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
]
