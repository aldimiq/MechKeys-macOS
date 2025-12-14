import rumps
import sys
import os
import pygame
from pynput import keyboard
import json
import random
from AppKit import NSApplication, NSApplicationActivationPolicyAccessory

APP_VERSION = "2.0"

# --- Configuration & Persistence ---
class ConfigManager:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.mechkeys.json")
        self.default_config = {
            "sound_pack": None,
            "volume": 0.5,
            "is_enabled": True,
            "audio_mode": "Stereo"  # Options: Mono, Stereo, 3D
        }
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            return self.default_config.copy()
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()

    def save(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.data.get(key, self.default_config.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()

# --- Key Mapping for Stereo Panning ---
# Maps key characters/names to a horizontal position from 0.0 (Left) to 1.0 (Right)
# 0.5 is Center.
KEY_PAN_MAP = {
    # Row 1 (Numbers)
    '`': 0.05, '1': 0.1, '2': 0.15, '3': 0.2, '4': 0.25, '5': 0.3, 
    '6': 0.5, '7': 0.7, '8': 0.75, '9': 0.8, '0': 0.85, '-': 0.9, '=': 0.95,
    
    # Row 2 (QWERTY)
    'q': 0.1, 'w': 0.15, 'e': 0.2, 'r': 0.25, 't': 0.3, 
    'y': 0.5, 'u': 0.7, 'i': 0.75, 'o': 0.8, 'p': 0.85, '[': 0.9, ']': 0.95, '\\': 0.95,
    
    # Row 3 (ASDF)
    'a': 0.1, 's': 0.15, 'd': 0.2, 'f': 0.25, 'g': 0.3, 
    'h': 0.5, 'j': 0.7, 'k': 0.75, 'l': 0.8, ';': 0.85, "'": 0.9,
    
    # Row 4 (ZXCV)
    'z': 0.15, 'x': 0.2, 'c': 0.25, 'v': 0.3, 
    'b': 0.5, 'n': 0.7, 'm': 0.75, ',': 0.8, '.': 0.85, '/': 0.9,
    
    # Special
    'space': 0.5,
    'enter': 0.9,
    'backspace': 0.9,
    'tab': 0.05,
    'shift': 0.05,
    'shift_r': 0.95,
    'ctrl_l': 0.0,
    'ctrl_r': 1.0,
    'alt_l': 0.1,
    'alt_r': 0.9,
    'cmd': 0.2,
    'cmd_r': 0.8
}

class SoundPack:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.sounds = []
        self.config = {}
        
        # Load config to get the display name if possible
        config_path = os.path.join(path, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                    self.name = self.config.get("name", self.name)
            except Exception as e:
                print(f"Error reading config for {self.name}: {e}")

    def load(self):
        """Loads and slices the sound file."""
        if self.sounds:
            return # Already loaded

        ogg_path = os.path.join(self.path, "sound.ogg")
        if not os.path.exists(ogg_path):
            print(f"Missing sound.ogg in {self.path}")
            return

        try:
            print(f"Loading sound pack: {self.name}...")
            full_sound = pygame.mixer.Sound(ogg_path)
            raw_data = full_sound.get_raw()
            
            # Mixer settings
            freq, size, channels = pygame.mixer.get_init()
            bytes_per_sample = abs(size) // 8
            bytes_per_ms = (freq * bytes_per_sample * channels) / 1000.0
            
            defines = self.config.get("defines", {})
            
            loaded_sounds = []
            
            for key_code, (offset_ms, duration_ms) in defines.items():
                start_byte = int(offset_ms * bytes_per_ms)
                length_byte = int(duration_ms * bytes_per_ms)
                
                # Ensure alignment
                block_align = bytes_per_sample * channels
                start_byte -= start_byte % block_align
                length_byte -= length_byte % block_align
                
                if start_byte + length_byte > len(raw_data):
                    continue
                    
                sound_bytes = raw_data[start_byte : start_byte + length_byte]
                if not sound_bytes:
                    continue
                    
                try:
                    s = pygame.mixer.Sound(buffer=sound_bytes)
                    loaded_sounds.append(s)
                except Exception as e:
                    print(f"Failed to create slice for key {key_code}: {e}")
            
            if not loaded_sounds:
                print("No slices created, using full sound as fallback.")
                loaded_sounds.append(full_sound)
                
            self.sounds = loaded_sounds
            print(f"Loaded {len(self.sounds)} sound slices for {self.name}")
            
        except Exception as e:
            print(f"Error loading audio for {self.name}: {e}")

    def play_random(self, pan=0.5, master_volume=1.0):
        if self.sounds:
            try:
                sound = random.choice(self.sounds)
                channel = sound.play()
                if channel:
                    # Calculate Left/Right volume based on pan (0.0 to 1.0)
                    # Pan 0.5 = 1.0 Left, 1.0 Right
                    
                    # Humanization: Random volume variance (+- 5%)
                    variance = random.uniform(0.95, 1.05)
                    
                    # Simple Linear Panning
                    left_vol = (1.0 - pan) * 2
                    right_vol = pan * 2
                    
                    # Clamp to 1.0 max per channel before applying master volume
                    left_vol = min(1.0, left_vol) * master_volume * variance
                    right_vol = min(1.0, right_vol) * master_volume * variance
                    
                    channel.set_volume(left_vol, right_vol)
            except Exception as e:
                print(f"Error playing sound: {e}")

class MechKeysApp(rumps.App):
    def __init__(self):
        super(MechKeysApp, self).__init__("MechKeys", title="", quit_button=None)
        
        # 1. Hide Dock Icon
        NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        
        self.icon = "menubar_icon_Template.png"
        self.template = True
        
        # 2. Config
        self.config = ConfigManager()
        self.is_enabled = self.config.get("is_enabled")
        self.master_volume = self.config.get("volume")
        self.audio_mode = self.config.get("audio_mode")
        
        # 3. Init Audio
        try:
            # Frequency 44.1kHz, 16bit, 2 channels (Stereo), buffer 512
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.init()
            # Allocate enough channels for rapid typing
            pygame.mixer.set_num_channels(32)
        except Exception as e:
            print(f"Failed to init pygame mixer: {e}")

        self.sound_packs = []
        self.current_pack = None
        self.held_keys = set()
        
        self.load_sound_packs()
        self.build_menu()
        
        # 4. Listener
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.daemon = True
        self.listener.start()

    def load_sound_packs(self):
        base_path = ""
        if getattr(sys, 'frozen', False):
            base_path = os.environ['RESOURCEPATH']
        else:
            base_path = os.path.dirname(__file__)
            
        sound_dir = os.path.join(base_path, "sound")
        
        if not os.path.exists(sound_dir):
            return

        for name in os.listdir(sound_dir):
            pack_path = os.path.join(sound_dir, name)
            if os.path.isdir(pack_path):
                pack = SoundPack(pack_path)
                self.sound_packs.append(pack)
        
        self.sound_packs.sort(key=lambda x: x.name)
        
        # Restore saved pack or default
        saved_pack_name = self.config.get("sound_pack")
        default_pack = None
        
        if saved_pack_name:
            default_pack = next((p for p in self.sound_packs if p.name == saved_pack_name), None)
            
        if not default_pack:
            # Default logic: Black ABS -> Black -> First
            default_pack = next((p for p in self.sound_packs if "Black" in p.name and "ABS" in p.name), None)
            if not default_pack:
                default_pack = next((p for p in self.sound_packs if "Black" in p.name), self.sound_packs[0] if self.sound_packs else None)
        
        if default_pack:
            self.set_pack(default_pack)

    def build_menu(self):
        # Sound Pack Menu
        pack_menu = rumps.MenuItem("Sound Pack")
        for pack in self.sound_packs:
            item = rumps.MenuItem(pack.name, callback=self.change_pack)
            item.state = 1 if self.current_pack and self.current_pack == pack else 0
            pack_menu.add(item)
            
        # Audio Mode Menu
        mode_menu = rumps.MenuItem("Audio Mode")
        for mode in ["Mono", "Stereo", "3D"]:
            item = rumps.MenuItem(mode, callback=self.change_mode)
            item.state = 1 if self.audio_mode == mode else 0
            mode_menu.add(item)

        # Volume Menu
        vol_menu = rumps.MenuItem("Volume")
        for v in [0.25, 0.5, 0.75, 1.0]:
            name = f"{int(v*100)}%"
            item = rumps.MenuItem(name, callback=self.change_volume)
            item.value = v 
            item.state = 1 if self.master_volume == v else 0
            vol_menu.add(item)

        self.menu = [
            pack_menu,
            mode_menu,
            vol_menu,
            rumps.separator,
            rumps.MenuItem("Enable Sounds", callback=self.toggle_sounds),
            rumps.separator,
            rumps.MenuItem(f"MechKeys v{APP_VERSION}"),
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        
        # Initialize Enable state
        self.menu["Enable Sounds"].state = 1 if self.is_enabled else 0

    def change_pack(self, sender):
        selected_pack = next((p for p in self.sound_packs if p.name == sender.title), None)
        if selected_pack:
            self.set_pack(selected_pack)
            # Update menu UI
            for item in self.menu["Sound Pack"]:
                self.menu["Sound Pack"][item].state = 1 if item == sender.title else 0
            
            # Save persistence
            self.config.set("sound_pack", selected_pack.name)

    def set_pack(self, pack):
        print(f"Switching to pack: {pack.name}")
        pack.load()
        self.current_pack = pack

    def change_mode(self, sender):
        self.audio_mode = sender.title
        self.config.set("audio_mode", self.audio_mode)
        
        for item in self.menu["Audio Mode"]:
            self.menu["Audio Mode"][item].state = 1 if item == sender.title else 0

    def change_volume(self, sender):
        try:
            val = int(sender.title.replace('%','')) / 100.0
        except:
            val = 0.5
            
        self.master_volume = val
        self.config.set("volume", val)
        
        for item in self.menu["Volume"]:
            self.menu["Volume"][item].state = 1 if item == sender.title else 0

    def toggle_sounds(self, sender):
        self.is_enabled = not self.is_enabled
        sender.state = 1 if self.is_enabled else 0
        self.config.set("is_enabled", self.is_enabled)

    def quit_app(self, _):
        if self.listener:
            try:
                self.listener.stop()
            except:
                pass
        os._exit(0)

    def on_press(self, key):
        if key in self.held_keys:
            return
        
        self.held_keys.add(key)
        
        if self.is_enabled and self.current_pack:
            # Default to Center/Mono
            pan = 0.5
            key_name = None
            
            try:
                if hasattr(key, 'char') and key.char:
                    key_name = key.char.lower()
                elif hasattr(key, 'name'):
                    key_name = key.name
            except:
                pass

            # Determine Pan based on Mode
            if self.audio_mode == "Mono":
                pan = 0.5
            else:
                # Stereo or 3D
                if key_name in KEY_PAN_MAP:
                    pan = KEY_PAN_MAP[key_name]
            
            # Play Sound with Mode adjustments
            final_vol = self.master_volume
            
            if self.audio_mode == "3D":
                # 1. Distance Attenuation: Keys further from center (0.5) are quieter
                distance = abs(0.5 - pan) # 0.0 to 0.5
                attenuation = 1.0 - (distance * 0.4) # Max 20% quietness at edges
                final_vol *= attenuation
                
                # 2. Thock Boost: Space and Enter are louder/bassier implies prominence
                if key_name in ['space', 'enter', 'backspace', 'shift_r']:
                    final_vol *= 1.15 # 15% boost for big keys

            self.current_pack.play_random(pan, final_vol)

    def on_release(self, key):
        if key in self.held_keys:
            self.held_keys.remove(key)

if __name__ == "__main__":
    app = MechKeysApp()
    app.run()