from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa

# Load processor and model
processor = Wav2Vec2Processor.from_pretrained("oyqiz/uzbek_stt")
model = Wav2Vec2ForCTC.from_pretrained("oyqiz/uzbek_stt")

# Function to load and preprocess audio using librosa
def load_audio(input_audio_path):
    waveform, sample_rate = librosa.load(input_audio_path, sr=None)
    return waveform, sample_rate

# Function to transcribe audio
def transcribe(input_audio_path):
    # Load and preprocess the audio
    waveform, sample_rate = load_audio(input_audio_path)

    # If the sample rate is not what the model expects, resample
    if sample_rate != processor.feature_extractor.sampling_rate:
        waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=processor.feature_extractor.sampling_rate)
        sample_rate = processor.feature_extractor.sampling_rate

    # Process the audio
    inputs = processor(waveform, sampling_rate=sample_rate, return_tensors="pt", padding=True)

    # Get the logits from the model
    with torch.no_grad():
        logits = model(**inputs).logits

    # Decode the logits to text
    predicted_ids = torch.argmax(logits, dim=-1)
    predicted_text = processor.batch_decode(predicted_ids)

    return predicted_text[0]

