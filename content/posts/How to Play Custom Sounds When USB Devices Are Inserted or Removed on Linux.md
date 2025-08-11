
If you want a quick and satisfying way to know when a USB device is plugged in or unplugged, why not add custom sounds to those events? Whether for convenience or just for fun, Linux lets you hook into USB device events and play different notification sounds automatically.

In this guide, I’ll walk you through how to play a distinct sound whenever a USB device is inserted or removed using `udev` rules and the PulseAudio sound system.

---

## 🔧 What You'll Achieve

- Play a sound when **a USB device is inserted**
    
- Play a different sound when **a USB device is removed**
    

---

## ✅ What You’ll Need Before Starting

1. A working sound system (PulseAudio or PipeWire works fine).
    
2. The following tools installed:
    

```bash
sudo pacman -S pulseaudio paprefs alsa-utils
```

3. Test that sound playback works by running:
    

```bash
paplay /usr/share/sounds/freedesktop/stereo/device-omni-added.wav
```

You should hear a test sound confirming your setup is good to go.

---

## 🛠️ Step-by-Step Instructions

### 1. Create the Sound Playback Script

First, create a shell script that will be triggered on USB events to play the appropriate sound.

```bash
sudo nano /usr/local/bin/usb-sound.sh
```

Paste the following:

```bash
#!/bin/bash

EVENT_TYPE="$1"

# Log USB event details
echo "[USB $EVENT_TYPE] $(date)" >> /tmp/usb-sound-udev.log
echo "Running as: $(whoami)" >> /tmp/usb-sound-udev.log
echo "Trying to play sound..." >> /tmp/usb-sound-udev.log

# Select sound based on event type
if [[ "$EVENT_TYPE" == "add" ]]; then
  SOUND="/usr/share/sounds/freedesktop/stereo/device-omni-added.wav"
elif [[ "$EVENT_TYPE" == "remove" ]]; then
  SOUND="/usr/share/sounds/freedesktop/stereo/device-omni-removed.wav"
fi

# Play sound if the file exists
if [[ -f "$SOUND" ]]; then
  sudo -E -u yourusername XDG_RUNTIME_DIR="/run/user/$(id -u yourusername)" DISPLAY=":0" paplay "$SOUND" >> /tmp/usb-sound-udev.log 2>&1
  echo "paplay exit status: $?" >> /tmp/usb-sound-udev.log
else
  echo "Sound file not found: $SOUND" >> /tmp/usb-sound-udev.log
fi
```

> **Important:** Replace `yourusername` with your actual Linux username in the script.

Make the script executable:

```bash
sudo chmod +x /usr/local/bin/usb-sound.sh
```

---

### 2. Allow Script to Run `paplay` Without Password

Since `udev` runs scripts as root, and `paplay` needs to run as your user to access PulseAudio, we grant passwordless sudo permission for `paplay`:

```bash
sudo visudo -f /etc/sudoers.d/usb-sound
```

Add the following line (again, replace `yourusername`):

```bash
yourusername ALL=(ALL) NOPASSWD: SETENV: /usr/bin/paplay
```

Save and exit.

---

### 3. Prepare Your Sound Files

Make sure you have the sound files in place:

- `/usr/share/sounds/freedesktop/stereo/device-omni-added.wav`
    
- `/usr/share/sounds/freedesktop/stereo/device-omni-removed.wav`
    

You can use your own `.wav` files by copying them to those locations:

```bash
sudo cp my-added.wav /usr/share/sounds/freedesktop/stereo/device-omni-added.wav
sudo cp my-removed.wav /usr/share/sounds/freedesktop/stereo/device-omni-removed.wav
```

---

### 4. Create Udev Rules to Trigger the Script

Create a udev rules file:

```bash
sudo nano /etc/udev/rules.d/99-usb-sound.rules
```

Paste:

```udev
ACTION=="add", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", RUN+="/usr/local/bin/usb-sound.sh add"
ACTION=="remove", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", RUN+="/usr/local/bin/usb-sound.sh remove"
```

Reload the rules:

```bash
sudo udevadm control --reload-rules
```

(Optional) Test your rule manually:

```bash
udevadm trigger --subsystem-match=usb --action=add
```

---

## ✅ You’re All Set!

### Testing:

- Plug in a USB device → You should hear the “device added” sound.
    
- Unplug the USB device → You should hear the “device removed” sound.
    
- Check logs for troubleshooting:
    

```bash
cat /tmp/usb-sound-udev.log
```

---

## 🧼 Maintenance Tips

- **Change sounds anytime** — just replace the `.wav` files under `/usr/share/sounds/freedesktop/stereo/`.
    
- Keep `/usr/local/bin/usb-sound.sh` owned by root for security.
    
- Monitor `/tmp/usb-sound-udev.log` to debug any issues.
    
- Feel adventurous? Extend your script to detect specific USB vendors or device types using `udevadm info`.
    

---

### Final Thoughts

Adding audio feedback to USB events is a simple yet nifty trick to enhance your Linux experience. It makes plugging in devices a bit more fun and informative without peeking at the screen.

Give it a try, customize your sounds, and let me know how it works for you!

---
