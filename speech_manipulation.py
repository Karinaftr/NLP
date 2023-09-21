from pydub import AudioSegment
import numpy as np
import pytsmod as tsm
import soundfile as sf
from faster_whisper import WhisperModel

dir = 'data'

def playback_speed_changing(file_name:str, cof:float):
    if cof == 50:
        cof = 1
    elif cof > 50: 
        cof = (cof - 50)/100
    else:
        cof = -0.0204 * cof + 2.
        
    sound = AudioSegment.from_wav(f'{dir}/{file_name}')
    resampl_factor = sound.frame_rate / 20
    resampl_factor = 2**round(np.log2(resampl_factor))

    data, samplerate = sf.read(f'{dir}/{file_name}')
    
    sound_new = tsm.phase_vocoder(data, cof, win_size=resampl_factor, syn_hop_size=(int(resampl_factor/2)), phase_lock=True)
    sf.write(f'{dir}/Modified_{file_name}', sound_new, samplerate)


def volume_changing(file_name:str, cof:float):
    sound = AudioSegment.from_wav(f'{dir}/{file_name}')
    sound = sound + cof
    sound.export(f'{dir}/Modified_{file_name}', format='wav')


def speech_to_txt(file_name:str):
    model = WhisperModel('large-v2', device='cpu', compute_type='int8')
    segments, info = model.transcribe(f'{dir}/{file_name}')
    segments = list(segments)
    return segments[0].text



