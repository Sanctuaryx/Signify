from TTS.api import TTS

class TTSConverter:
    def __init__(self, model_name: str):
        """
        Initialize the TTS model once.

        Args:
            model_name (str): The name of the TTS model to use.
        """
        self.tts = TTS(model_name)
        print(f'TTS model "{model_name}" initialized successfully.')

    def convert_text_to_audio(self, text: str, output_file: str, speaker_idx: int = None, language: str = None):
        """
        Convert text to audio using the initialized TTS model.

        Args:
            text (str): Text to convert to speech.
            output_file (str): Path to the output audio file (typically ending in `.wav`).
            speaker_idx (int, optional): The ID of the specific speaker to use for synthesis.
        """
        # Check for a specified speaker index and generate speech accordingly
        if speaker_idx is not None and language is not None:
            self.tts.tts_to_file(text=text, file_path=output_file, speaker=speaker_idx, language=language)
        else:
            self.tts.tts_to_file(text=text, file_path=output_file)
