# 4-Track-Backup

A user-friendly program for Raspberry Pi that records audio from multiple USB ports simultaneously as WAV files, provides a GUI dashboard for playback with controls, and displays track information on an e-ink hat.

## Features

- Simultaneous recording from up to 4 USB audio devices (automatically mapped to physical ports)
- WAV file recording
- GUI dashboard with controls for each track:
  - **Monitor**: Real-time audio monitoring of input
  - **Play/Stop**: Playback of recorded tracks
  - **Mute/Solo**: Audio controls
  - **Volume**: Adjustable playback volume
- Playback of individual tracks or all together
- Export functionality
- E-ink display for track status (optional)

## USB Port Mapping

The program automatically detects USB audio devices and maps them to tracks numbered clockwise from the top-left USB port:

- Track 1: Top-Left USB port
- Track 2: Top-Right USB port  
- Track 3: Bottom-Right USB port
- Track 4: Bottom-Left USB port

Only USB devices with input capabilities are used.

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

5. Ensure USB audio devices are connected and recognized.

6. Run the program:
   ```
   python main.py
   ```

Note: Always activate the virtual environment (`source venv/bin/activate`) before running the program.

## Auto-start on Boot

To start the GUI automatically after boot on Raspberry Pi desktop:

1. Copy the `.desktop` file into the autostart folder:
   ```bash
   mkdir -p ~/.config/autostart
   cp 4-track-backup.desktop ~/.config/autostart/
   ```

2. Make sure `run.sh` is executable:
   ```bash
   chmod +x ./run.sh
   ```

3. Update the `Exec=` line in `4-track-backup.desktop` if your repository is not in `/home/pi/4-Track-Backup`.
   For example, if the project lives in `/home/weatherbelle/4-Track-Backup`, use:
   ```ini
   Exec=/usr/bin/env bash /home/weatherbelle/4-Track-Backup/run.sh
   ```

4. Reboot the Pi:
   ```bash
   sudo reboot
   ```

The program should open automatically when the Raspberry Pi desktop session starts.
## Usage

- Launch the program to open the GUI dashboard.
- Click "Record All" to start recording from all detected USB devices.
- Click "Stop Recording" to stop.
- Use play/stop buttons for each track.
- Adjust volume, mute, or solo tracks.
- "Play All" to play all tracks together.
- "Export" to save WAV files to a selected folder.

Track information is displayed on the e-ink hat.