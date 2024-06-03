# /main/speech_file_manager.py

import os
import simpleaudio as sa
import threading


class SpeechFileManager:
    def __init__(self, file_path: str = 'resources/audioResources/audioTracks/audio.wav'):
        """
        Initialize the SpeechFileManager class with the default file path.

        Args:
            file_path (str): The path to the `.wav` file to be managed.
        """
        self.playback_thread = None
        self.file_path = file_path
        
        print('File manager initialized successfully.')


    def delete_speech_file(self):
        """
        Deletes the `.wav` file if it exists.
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def _play_audio(self):
        """
        Play a `.wav` audio file.

        """
        try:
            # Load the `.wav` file into a wave object
            wave_obj = sa.WaveObject.from_wave_file(self.file_path)

            # Play the wave object
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait until playback is finished
            
            self.delete_speech_file()

        except FileNotFoundError:
            print(f'Error: The file "{self.file_path}" was not found.')
        except sa.simpleaudio.AudioPlaybackError as e:
            print(f'Error playing audio: {e}')
            
    def play_speech_file(self):
        # Start a new thread for audio playback
        self._play_audio()
