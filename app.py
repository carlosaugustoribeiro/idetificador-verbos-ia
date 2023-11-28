import logging
from flask import Flask, render_template, request, jsonify
from audio_utils import save_audio_file, delete_audios
from transcriber_utils import audio_to_text
from phrases_utils import calc_verbs


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# Configurando o sistema de logs
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    app.logger.info('Acessou a rota /')
    return render_template('index.html')


@app.route('/deleteAll')
def delete_all_files():
    delete_audios('./uploads/*.wav')
    return jsonify({'msg': 'audios apagados'}), 200


@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        audio_file = request.files['audio']

        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        audio_saved = save_audio_file(audio_file)

        target_text = audio_to_text(audio_saved)
        app.logger.info(target_text)
        identified_verbs = calc_verbs(target_text)

        response = {
            'targetText': target_text,
            'verbs': identified_verbs
        }

        delete_audios(f"./uploads/{audio_saved['filename']}")

        if audio_saved['saved']:
            return {'status': 'success', 'message': response}
        else:
            return {'status': 'error', 'message': 'Falha ao salvar o arquivo de áudio.'}

    except Exception as e:
        app.logger.error(e)
        return {'status': 'error', 'message': str(e)}


delete_audios('./uploads/*.wav')


if __name__ == '__main__':
    app.run(debug=True)
