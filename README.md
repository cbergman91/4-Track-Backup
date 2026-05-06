# 4-Track-Backup

A user-friendly program for Raspberry Pi that records audio from multiple USB ports simultaneously as WAV files, provides a GUI dashboard for playback with controls, and displays track information on an e-ink hat.

## Features

- Simultaneous recording from USB audio devices
- WAV file recording
- GUI dashboard with play, stop, mute, solo, volume controls
- Playback of individual tracks or all together
- Export functionality
- E-ink display for track status

## Requirements

- Raspberry Pi with USB audio devices
- E-ink hat (compatible with waveshare-epd library, e.g., 2.13inch V2 - adjust import in main.py if using a different model)
- Python 3

## Installation

1. Ensure Python 3 and venv are installed:
   ```
   sudo apt update
   sudo apt install python3 python3-venv python3-pip portaudio19-dev
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. (Optional) Install Waveshare e-Paper library for e-ink display:
   ```
   git clone https://github.com/waveshare/e-Paper.git
   cd e-Paper/RaspberryPi_JetsonNano/python
   python setup.py install
   ```
   Note: If waveshare-epd is not installed, the program will run without e-ink display functionality.

4. Ensure USB audio devices are connected and recognized.

5. Run the program:
   ```
   python main.py
   ```

Note: Always activate the virtual environment (`source venv/bin/activate`) before running the program.
   python main.py
   ```

## Usage

- Launch the program to open the GUI dashboard.
- Click "Record All" to start recording from all detected USB devices.
- Click "Stop Recording" to stop.
- Use play/stop buttons for each track.
- Adjust volume, mute, or solo tracks.
- "Play All" to play all tracks together.
- "Export" to save WAV files to a selected folder.

Track information is displayed on the e-ink hat.