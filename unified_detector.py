import sounddevice as sd
import numpy as np
from scipy.io import wavfile    
from scipy import signal            
import threading

class UnifiedDetector:
    def __init__(self, generation, shiny_threshold, battle_threshold,
                 device='hw:2,0', sample_rate=48000):

        self.device = device
        self.sample_rate = sample_rate
        self.shiny_threshold = shiny_threshold
        self.battle_threshold = battle_threshold
        self.is_listening_for_battle = False

        # Real-time audio stream
        self.stream = None

        # Thread events
        self.shiny_found_event = threading.Event()
        self.battle_found_event = threading.Event()

        # Load templates
        self._load_shiny_template(generation)
        self._load_battle_template(generation)

        # Buffers for shiny and battle
        self.prev_shiny_buffer = np.zeros(self.shiny_length, dtype=np.float32)
        self.prev_battle_buffer = np.zeros(self.battle_length, dtype=np.float32)

    # -------------------------------------------------------------------------
    # LOAD TEMPLATES
    # -------------------------------------------------------------------------
    def _load_shiny_template(self, generation):
        """Load shiny template based on the generation setting."""
        file_map = {
            '3': 'shiny_gen_3.wav',
            '4': 'shiny_gen_4.wav',
            '5': 'shiny_gen_5.wav'
        }

        filename = file_map[generation]
        samplerate, template = wavfile.read(filename)

        if samplerate != self.sample_rate:
            raise ValueError(
                f"Shiny template sample rate mismatch: {samplerate} vs {self.sample_rate}"
            )

        print(f"Loaded shiny template '{filename}'")

        if template.ndim > 1:
            template = template.mean(axis=1)

        template = template.astype(np.float32)
        template /= np.max(np.abs(template))

        self.shiny_template = template
        self.shiny_length = len(template)

    def _load_battle_template(self, generation):
        """Loads the 3-second battle intro music."""
        file_map = {
            '3': 'battle_gen_3.wav',
            '4': 'battle_gen_4.wav',
            '5': 'battle_gen_5.wav'
        }

        filename = file_map[generation]
        samplerate, template = wavfile.read(filename)

        if samplerate != self.sample_rate:
            raise ValueError(
                f"Battle template sample rate mismatch: {samplerate} vs {self.sample_rate}"
            )

        print(f"Loaded battle template '{filename}'")

        if template.ndim > 1:
            template = template.mean(axis=1)

        template = template.astype(np.float32)
        template /= np.max(np.abs(template))

        self.battle_template = template
        self.battle_length = len(template)

    # -------------------------------------------------------------------------
    # AUDIO CALLBACK
    # -------------------------------------------------------------------------
    def _audio_callback(self, indata, frames, time_info, status):
        """Single unified callback that detects shiny or battle."""

        mono_chunk = indata.flatten().astype(np.float32)

        # Normalize variance a bit
        if np.std(mono_chunk) > 1e-6:
            mono_chunk /= (np.std(mono_chunk) + 1e-6)

        # -----------------------
        # SHINY DETECTION
        # -----------------------
        shiny_audio = np.concatenate((self.prev_shiny_buffer, mono_chunk))
        shiny_corr = signal.fftconvolve(
            shiny_audio, self.shiny_template[::-1], mode='valid'
        )
        shiny_peak = np.max(np.abs(shiny_corr))
        self.prev_shiny_buffer = mono_chunk[-self.shiny_length:]
        
        if shiny_peak > self.shiny_threshold:
            self.shiny_found_event.set()

        # -----------------------
        # BATTLE DETECTION
        # -----------------------
        if self.is_listening_for_battle:
            battle_audio = np.concatenate((self.prev_battle_buffer, mono_chunk))
            battle_corr = signal.fftconvolve(
                battle_audio, self.battle_template[::-1], mode='valid'
            )
            battle_peak = np.max(np.abs(battle_corr))
            self.prev_battle_buffer = mono_chunk[-self.battle_length:]
            
            if battle_peak > self.battle_threshold:
                self.battle_found_event.set()
        else:
            # When not listening, just keep the buffer fresh
            self.prev_battle_buffer = mono_chunk[-self.battle_length:]

    # -------------------------------------------------------------------------
    # STREAM CONTROL
    # -------------------------------------------------------------------------
    def start(self):
        """Starts the microphone stream once."""
        if self.stream:
            return

        print("Starting unified audio detector...")
        self.chunk_size = self.shiny_length * 3
        self.hop_size = self.chunk_size // 2 

        try:
            self.stream = sd.InputStream(
                device=self.device,
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.hop_size,
                callback=self._audio_callback,
                dtype='float32'
            )
            self.stream.start()
        except Exception as e:
            print(f"Error starting audio stream: {e}")
            raise

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    # -------------------------------------------------------------------------
    # DETECTION CONTROL
    # -------------------------------------------------------------------------
    def start_battle_detection(self):
        """Allow the audio callback to start detecting battles."""
        self.is_listening_for_battle = True

    def stop_battle_detection(self):
        """Prevent the audio callback from detecting battles."""
        self.is_listening_for_battle = False

    # -------------------------------------------------------------------------
    # WAIT FUNCTIONS
    # -------------------------------------------------------------------------
    def wait_for_shiny(self, timeout=8):
        self.shiny_found_event.clear()
        return self.shiny_found_event.wait(timeout=timeout)

    def wait_for_battle(self, timeout=1.0):
        return self.battle_found_event.wait(timeout=timeout)