import pyaudio
import wave
import threading
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Try to import e-ink library
try:
    from waveshare_epd import epd2in13_V2
    EPD_AVAILABLE = True
except ImportError:
    EPD_AVAILABLE = False
    print("Warning: waveshare-epd not available. E-ink display will be disabled.")

# Initialize Pygame mixer
pygame.mixer.init()

# E-ink display (only if available)
if EPD_AVAILABLE:
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    # Font for e-ink
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
else:
    epd = None
    font = None

class Track:
    def __init__(self, device_index, name):
        self.device_index = device_index
        self.name = name
        self.filename = f"{name}.wav"
        self.is_recording = False
        self.is_playing = False
        self.is_monitoring = False
        self.muted = False
        self.solo = False
        self.volume = 1.0
        self.sound = None
        self.thread = None
        self.monitor_thread = None

    def start_recording(self):
        if self.is_recording:
            return
        self.is_recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop_recording(self):
        self.is_recording = False
        if self.thread:
            self.thread.join()

    def _record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=self.device_index,
                        frames_per_buffer=CHUNK)

        frames = []

        while self.is_recording:
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Load for playback
        self.sound = pygame.mixer.Sound(self.filename)

    def start_monitoring(self):
        if self.is_monitoring:
            return
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()

    def _monitor(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,  # For monitoring
                        input_device_index=self.device_index,
                        output_device_index=p.get_default_output_device_info()['index'],
                        frames_per_buffer=CHUNK)

        while self.is_monitoring:
            data = stream.read(CHUNK)
            stream.write(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def play(self):
        if self.sound and not self.is_playing:
            self.is_playing = True
            self.sound.play()

    def stop(self):
        if self.sound:
            self.sound.stop()
            self.is_playing = False

    def set_volume(self, vol):
        self.volume = vol
        if self.sound:
            self.sound.set_volume(vol)

    def mute(self):
        self.muted = not self.muted
        if self.sound:
            if self.muted:
                self.sound.set_volume(0)
            else:
                self.sound.set_volume(self.volume)

    def solo(self):
        self.solo = not self.solo
        # Solo logic: if any solo, mute others, but for simplicity, toggle

class AudioRecorder:
    def __init__(self):
        self.tracks = []
        self.available_devices = self.get_available_devices()
        self.select_tracks()

    def get_available_devices(self):
        devices = []
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(numdevices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                devices.append({
                    'index': i,
                    'name': device_info.get('name'),
                    'channels': device_info.get('maxInputChannels')
                })
        p.terminate()
        return devices

    def select_tracks(self):
        # For Raspberry Pi USB ports, assume clockwise numbering:
        # 1: top-left, 2: top-right, 3: bottom-right, 4: bottom-left
        usb_devices = [d for d in self.available_devices if 'USB' in d['name']]
        
        # Map to physical ports (this may need adjustment based on actual hardware)
        port_mapping = {
            0: "Port 1 (Top-Left)",
            1: "Port 2 (Top-Right)", 
            2: "Port 3 (Bottom-Right)",
            3: "Port 4 (Bottom-Left)"
        }
        
        for i, device in enumerate(usb_devices[:4]):  # Limit to 4 tracks
            port_name = port_mapping.get(i, f"Port {i+1}")
            self.tracks.append(Track(device['index'], f"Track_{i+1}_{port_name}"))

    def start_all_recording(self):
        for track in self.tracks:
            track.start_recording()

    def stop_all_recording(self):
        for track in self.tracks:
            track.stop_recording()

class GUI:
    def __init__(self, recorder):
        self.recorder = recorder
        self.root = tk.Tk()
        self.root.title("4-Track Backup")
        self.track_frames = []

        for i, track in enumerate(recorder.tracks):
            frame = tk.Frame(self.root)
            frame.pack(pady=5)

            tk.Label(frame, text=track.name).pack(side=tk.LEFT)

            tk.Button(frame, text="Monitor", command=lambda t=track: self.toggle_monitor(t)).pack(side=tk.LEFT)
            tk.Button(frame, text="Play", command=lambda t=track: t.play()).pack(side=tk.LEFT)
            tk.Button(frame, text="Stop", command=lambda t=track: t.stop()).pack(side=tk.LEFT)
            tk.Button(frame, text="Mute", command=lambda t=track: t.mute()).pack(side=tk.LEFT)
            tk.Button(frame, text="Solo", command=lambda t=track: t.solo()).pack(side=tk.LEFT)

            vol_scale = tk.Scale(frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=lambda v, t=track: t.set_volume(float(v)))
            vol_scale.set(1.0)
            vol_scale.pack(side=tk.LEFT)

            self.track_frames.append(frame)

        tk.Button(self.root, text="Record All", command=self.recorder.start_all_recording).pack()
        tk.Button(self.root, text="Stop Recording", command=self.recorder.stop_all_recording).pack()
        tk.Button(self.root, text="Play All", command=self.play_all).pack()
        tk.Button(self.root, text="Export", command=self.export).pack()

    def toggle_monitor(self, track):
        if track.is_monitoring:
            track.stop_monitoring()
        else:
            track.start_monitoring()

    def play_all(self):
        for track in self.recorder.tracks:
            track.play()

    def export(self):
        # Simple export: copy files to a folder
        folder = filedialog.askdirectory()
        if folder:
            for track in self.recorder.tracks:
                if os.path.exists(track.filename):
                    os.system(f"cp {track.filename} {folder}/")
            messagebox.showinfo("Export", "Tracks exported!")

    def run(self):
        self.root.mainloop()

class EInkDisplay:
    def __init__(self, recorder):
        self.recorder = recorder

    def update(self):
        if not EPD_AVAILABLE or epd is None:
            return
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        y = 0
        for track in self.recorder.tracks:
            status = "Recording" if track.is_recording else "Idle"
            draw.text((0, y), f"{track.name}: {status}", font=font, fill=0)
            y += 15
        epd.display(epd.getbuffer(image))

def main():
    recorder = AudioRecorder()
    display = EInkDisplay(recorder)
    gui = GUI(recorder)

    # Update display periodically
    def update_display():
        display.update()
        gui.root.after(1000, update_display)

    update_display()
    gui.run()

if __name__ == "__main__":
    main()