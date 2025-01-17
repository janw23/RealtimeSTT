from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    colorama.init()

    full_sentences = []
    displayed_text = ""

    def clear_console():
        os.system('clear' if os.name == 'posix' else 'cls')

    def text_detected(text):
        global displayed_text
        sentences_with_style = [
            f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
            for i, sentence in enumerate(full_sentences)
        ]
        new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

        if new_text != displayed_text:
            displayed_text = new_text
            clear_console()
            print(displayed_text, end="", flush=True)

    # def text_detected(text):
    #     global displayed_text
    #     clear_console()
    #     print(text)
        # sentences_with_style = [
        #     f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
        #     for i, sentence in enumerate(full_sentences)
        # ]
        # new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

        # if new_text != displayed_text:
        #     displayed_text = new_text
        #     clear_console()
        #     print(displayed_text, end="", flush=True)

    def process_text(text):
        full_sentences.append(text)
        text_detected("")
    
    def on_vad_detect_stop():
        print("<|voice detected|>", end="", flush=True)

    recorder_config = {
        'spinner': False,
        # 'model': 'large-v2',
        'model': 'large-v3', # "medium" fits 2GB VRAM if used with "int8_float16" compute type
        'device': 'cpu', # "cuda"
        'compute_type': 'float32',
        'language': 'pl',
        'silero_sensitivity': 0.6, # the higher the more eager to detect speech but prone to misdetection
        'silero_use_onnx': True,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0.4,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.2,
        'realtime_model_type': 'small',
        'realtime_device': 'cuda',
        'realtime_compute_type': 'float16',
        'on_realtime_transcription_update': text_detected, 
        #'on_realtime_transcription_stabilized': text_detected,
        'on_vad_detect_stop': on_vad_detect_stop,
    }

    recorder = AudioToTextRecorder(**recorder_config)

    clear_console()
    print("Say something...", end="", flush=True)

    while True:
        recorder.text(process_text)
