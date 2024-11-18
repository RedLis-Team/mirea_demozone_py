import torch
from TTS.api import TTS
import soundfile as sf

def ttss(text_value: str, audio_path):

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("CUDA is not available. Using CPU.")
    
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=(device == "cuda"))

    # speaker_wav_path : str = './data/files/answer.wav'
    # sf.write(speaker_wav_path, audio_path[1], audio_path[0])

    tts.tts_to_file(
        text=text_value,
        file_path="./data/files/answer.wav",
        speaker_wav='./data/files/input.wav',
        language="ru"
    )
    
    # return "output_tts.wav"
