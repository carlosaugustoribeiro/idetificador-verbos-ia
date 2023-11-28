document.addEventListener('DOMContentLoaded', () => {
    let mediaRecorder;
    let audioChunks = [];
    let audioPlayer = document.getElementById('audioPlayer');
    let startRecordButton = document.getElementById('startRecord');
    let stopRecordButton = document.getElementById('stopRecord');
    let sendAudioButton = document.getElementById('sendAudio');
    let resultTextDiv = document.getElementById('resultText');
    let resultVerbsDiv = document.getElementById('resultVerbs');
    let resultTextSpanContent = document.getElementById('resultTextContent');
    let resultVerbsSpanContent = document.getElementById('resultVerbsContent');

    // Solicitar permissão para acessar o microfone
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                let audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioPlayer.src = URL.createObjectURL(audioBlob);
                sendAudioButton.disabled = false;
            };

            startRecordButton.addEventListener('click', () => {
                mediaRecorder.start();
                audioChunks = [];
                startRecordButton.disabled = true;
                stopRecordButton.disabled = false;
                sendAudioButton.disabled = true;
            });

            stopRecordButton.addEventListener('click', () => {
                mediaRecorder.stop();
                startRecordButton.disabled = false;
                stopRecordButton.disabled = true;
            });

            sendAudioButton.addEventListener('click', () => {
                if (audioChunks.length > 0) {
                    sendAudio(audioChunks);
                }
            });
        })
        .catch(error => console.error('Erro ao acessar o microfone:', error));

    function sendAudio(audioChunks) {
        loadingIndicator.style.visibility = 'visible';
        startRecordButton.disabled = true;
        stopRecordButton.disabled = true;
        sendAudioButton.disabled = true;

        let audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        let formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');

        fetch('/upload-audio', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Resposta do servidor:', data);
            sendAudioButton.disabled = false;
            startRecordButton.disabled = false;
            loadingIndicator.style.visibility = 'hidden';
            resultTextSpanContent.textContent = data.message.targetText;
            resultVerbsSpanContent.textContent = data.message.verbs;
            resultTextDiv.style.display = 'block';
            resultVerbsDiv.style.display = 'block';
        })
        .catch(error => {
            sendAudioButton.disabled = false;
            startRecordButton.disabled = false;
            loadingIndicator.style.display = 'none';
            console.error('Erro ao enviar áudio:', error)
        });
    }
});
