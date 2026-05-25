import simpleaudio as sa
from pydub import AudioSegment
import asyncio
import os

class Speakers:
    """
    A class for playing audio files. Supports WAV files natively, and can decode and play other formats with FFmpeg installed.
    """
    def __init__(self, path: str, starts_looped: bool = False):
        self._is_looping = starts_looped
        self.file = path
        self.audio_data = None 
    
    def decode(self, file_type: str = "mp3"):
        """
        Decodes any of the file formats listed below so play() can use it.
        Supported file formats (requires FFmpeg installed):
        - MP3 (.mp3)
        - MP4 (.mp4)
        - WAV (.wav)
        - AAC / M4A (.aac, .m4a)
        - OGG (.ogg)
        - FLAC (.flac)
        - WMA (.wma)
        """
        self.audio_data = AudioSegment.from_file(self.file, format=file_type)
        return self.audio_data
    
    def play(self):
        """
        Plays WAV files natively, or plays any decoded format if decode() was called first.
        """
        if self.audio_data is not None:
            play_obj = sa.play_buffer(
                self.audio_data.raw_data,
                num_channels=self.audio_data.channels,
                bytes_per_sample=self.audio_data.sample_width,
                sample_rate=self.audio_data.frame_rate
            )
            return play_obj
        
        elif self.file.lower().endswith('.wav'):
            wave_obj = sa.WaveObject.from_wave_file(self.file)
            return wave_obj.play()
        
        else:
            raise ValueError("File must be a .wav or decoded first using decode().")
    
    def loop(self):
        """
        Starts a blocking playback loop.
        """
        self._is_looping = True
        while self._is_looping:
            play_obj = self.play()
            play_obj.wait_done()

    def stop_loop(self):
        """
        Stops any active playback loop.
        """
        self._is_looping = False
    
    def start_loop(self):
        """
        Resets the loop state and starts looping.
        """
        self.loop()
    
    async def playIntegrated(self):
        """
        Asynchronously plays the audio file using the system's integrated music player.
        """
        if not os.path.exists(self.file):
            raise FileNotFoundError(f"[ERR] File {self.file} wasn't found.")

        import sys
        if sys.platform.startswith('win32'):
            cmd = f'start "" "{os.path.abspath(self.file)}"'
            process = await asyncio.create_subprocess_shell(cmd)
        elif sys.platform.startswith('darwin'):
            process = await asyncio.create_subprocess_exec('open', self.file)
        else:
            process = await asyncio.create_subprocess_exec('xdg-open', self.file)
        
        await process.communicate()
