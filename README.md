# AutoClicker for Games

A program for automating keyboard and mouse clicks in games with support for fullscreen mode. Written in Python using CustomTkinter.

![Icon](icon.png)

## What's New in Version 2.0

### Major Update!

- **Completely redesigned interface** - modern neumorphic UI built with CustomTkinter
- **Custom sequence feature** - create your own key/mouse button sequences with custom delays
- **Enhanced hotkey binding** - easily change function hotkeys through the interface
- **Improved performance** - optimized for lower CPU usage and better reliability

## Features

1. **Spam** - automatically performs a sequence of actions in order:
   - Press Space → Wait 10ms → Release Space → Wait 10ms
   - Press 1 → Wait 10ms → Release 1 → Wait 10ms
   - Press LMB → Wait 10ms → Release LMB → Wait 10ms
   - **For skipping dialogues in Honkai: Star Rail**
2. **LMB** - automatically presses and releases left mouse button with 10ms delays
3. **Custom Sequence** - create your own sequence of keyboard and mouse actions with custom delays
4. **Customizable binds** - ability to assign keys to enable/disable functions
5. **Enable/Disable** - ability to quickly turn the entire program on/off without closing it

## Requirements

- Python 3.7 or higher
- Libraries: customtkinter, pyautogui, pynput, pillow
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
pyinstaller --noconsole --icon=icon.png --noupx autoclicker.py 
```

3. The finished file will be available in the `dist` folder

## Usage

1. Launch the program (EXE file or Python script)
2. The program starts in active mode but with the menu hidden
3. Control the program using hotkeys:
   - **Delete** - show/hide menu
   - **F1** - enable/disable Spam function (can be rebound)
   - **F2** - enable/disable LMB function (can be rebound)
   - **F3** - enable/disable Custom Sequence function (can be rebound)
4. To configure the program, press **Delete** to show the menu
5. Use the "Enable Program" / "Disable Program" button to quickly enable or disable all functions
6. Change key bindings by clicking the "Change" button next to each function
7. Configure custom sequences by clicking the "Configure Sequence" button

## Important to Know

- The program requires administrator rights to work with keyboard hooks
- Functions work even with the menu hidden
- The status in the menu shows whether the program is currently active or disabled
- Custom sequences can be very powerful - experiment with different combinations!

## Warning

Using auto-clickers may violate the rules of some games and lead to account blocking. Use at your own risk.

## License

MIT

## Author

zaaaa