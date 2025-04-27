# AutoClicker for Games

A program for automating keyboard and mouse clicks in games with support for fullscreen mode. Written in Python using PyAutoGUI and tkinter.

![Icon](icon.png)

## Features

1. **Spam** - automatically presses left mouse button, space and key 1 every 10 ms
2. **LMB** - automatically presses only the left mouse button every 10 ms
3. **Customizable binds** - ability to assign keys to enable/disable functions
4. **Enable/Disable** - ability to quickly turn the entire program on/off without closing it
5. **Desktop interface** - opens on your desktop, not in the game itself

## How It Works

The program runs on your desktop and sends keyboard and mouse inputs to any active window, including games running in fullscreen mode. It doesn't modify game files or inject into game processes, making it safer to use from an anti-cheat perspective.

When you press the **Delete** key, the interface appears on your desktop, allowing you to configure settings while the game is minimized or on another monitor.

## Requirements

- Python 3.7 or higher
- Libraries: pyautogui, pynput, pillow
- Administrator privileges (for global keyboard hooks)

## Installation and Launch

### Option 1: Running the Python script

1. Clone the repository:
```bash
git clone https://github.com/your-username/AutoClickerPy.git
cd AutoClickerPy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python autoclicker.py
```

### Option 2: Using the ready-made EXE file

1. Download the latest version from the [Releases](https://github.com/your-username/AutoClickerPy/releases) section
2. Extract the archive and run `autoclicker.exe`

### Option 3: Creating your own EXE file

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create an EXE file:
```bash
pyinstaller --onefile --windowed --icon=icon.png autoclicker.py
```

3. The finished file will be available in the `dist` folder

## Usage

1. Launch the program (EXE file or Python script)
2. The program starts in active mode but with the menu hidden
3. Control the program using hotkeys:
   - **Delete** - show/hide menu
   - **F1** - enable/disable Spam function (can be rebound)
   - **F2** - enable/disable LMB function (can be rebound)
4. To configure the program, press **Delete** to show the menu
5. Use the "Enable Program" / "Disable Program" button to quickly enable or disable all functions
6. Change key bindings by clicking the "Change" button next to each function

## Important to Know

- The program requires administrator rights to work with keyboard hooks
- The program runs on your desktop, not inside the game - this helps avoid some anti-cheat detections
- To use with games, launch both the game and the AutoClicker, then switch to the game
- Functions work even with the menu hidden
- When the game is in fullscreen, you'll need to alt-tab to your desktop to see the menu
- The status in the menu shows whether the program is currently active or disabled

## Warning

Using auto-clickers may violate the rules of some games and lead to account blocking. Use at your own risk.

## License

MIT

## Author

Your Name 