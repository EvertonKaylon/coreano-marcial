"""
Views for serving audio files.
"""
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import AudioFile


@login_required
def serve_audio(request, audio_id):
    """
    Serve audio file to authenticated users only.
    Sets appropriate Content-Type and Cache-Control headers.
    """
    audio_file = get_object_or_404(AudioFile, id=audio_id)
    
    try:
        response = FileResponse(audio_file.audio_file.open('rb'))
        
        file_ext = audio_file.audio_file.name.split('.')[-1].lower()
        content_types = {
            'mp3': 'audio/mpeg',
            'ogg': 'audio/ogg',
            'opus': 'audio/opus',
        }
        response['Content-Type'] = content_types.get(file_ext, 'audio/mpeg')
        
        response['Cache-Control'] = 'public, max-age=604800'
        
        return response
    except FileNotFoundError:
        raise Http404('Arquivo de áudio não encontrado.')
