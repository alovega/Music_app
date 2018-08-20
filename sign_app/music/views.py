from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from .models import Album
from .forms import UserForm,SongForm


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album', 'genre', 'album_logo']



class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongFormView(View):
    form_class = SongForm
    template_name = 'music/song_form.html'

    def get(self, request,album_id):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self,request,album_id):
        form = self.form_class(request.POST, request.FILES)
        album = get_object_or_404(Album, pk=album_id)

        if form.is_valid():
            albums_songs = album.song_set.all()
            for s in albums_songs:
                if s.song_title == form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'music/create_song.html', context)

            song = form.save(commit=False)
            song.album = album
            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'music/create_song.html', context)

            song.save()
            return render(request, 'music/detail.html', {'album': album})


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    #displays a blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    #process form data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #cleaned data- data formatted properly
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns user object if credentials are given are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form':form})


class AlbumFavoriteView(View):

    def favorite_album(request, album_id):
        album = get_object_or_404(Album, pk=album_id)
        try:
            if album.is_favorite:
                album.is_favorite = False
            else:
                album.is_favorite = True
            album.save()
        except (KeyError, Album.DoesNotExist):
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': True})
