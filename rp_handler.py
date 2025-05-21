import runpod, tempfile, os, requests
import nemo.collections.asr as nemo_asr
from pydub import AudioSegment                # converts mp3 → wav

# load the speech-to-text model once per GPU worker
MODEL = nemo_asr.models.ASRModel.from_pretrained(
    model_name="nvidia/parakeet-tdt-0.6b-v2"
).cuda()

def _to_wav(url: str) -> str:
    """Download the audio and convert to 16 kHz mono WAV (required)."""
    raw_file = tempfile.NamedTemporaryFile(delete=False)
    raw_file.write(requests.get(url, timeout=30).content); raw_file.close()

    wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    AudioSegment.from_file(raw_file.name).set_frame_rate(16000)\
                .set_channels(1).export(wav_file.name, format="wav")
    os.unlink(raw_file.name)
    return wav_file.name

def handler(job):
    audio_url = job["input"].get("audio_url")
    if not audio_url:
        return {"error": "Please pass audio_url in the input."}

    wav_path = _to_wav(audio_url)
    text = MODEL.transcribe([wav_path])[0]
    os.unlink(wav_path)
    return {"transcription": text}

runpod.serverless.start({"handler": handler})
