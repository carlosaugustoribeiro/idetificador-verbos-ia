from datetime import datetime
import os
import glob


def save_audio_file(audio_file):
    # Gerar um nome de arquivo único usando um timestamp
    timestamp = datetime.now().timestamp() * 1000
    filename = f'audio_{timestamp}.wav'

    # Salvar o arquivo no diretório 'uploads' com o novo nome
    save_path = f'uploads/{filename}'
    audio_file.save(save_path)

    audio_saved = {'filename': filename, 'saved': False}
    if save_path:
        audio_saved['saved'] = True

    return audio_saved


def delete_audios(pattern):
    files = glob.glob(pattern)
    for f in files:
        os.remove(f)
