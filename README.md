# Image to RGB565 C-Array Converter

A simple GUI tool to convert images to RGB565 format C arrays for embedded displays (LCD, TFT, etc.).

## Features

- 🖼️ Convert any image (PNG, JPG, BMP, GIF) to RGB565 format
- 📐 Auto-resize to 240x240 pixels
- 🔄 Byte swap (Big Endian / Little Endian)
- 🎨 Invert colors option
- 💾 Export as C header file (.h) or text file

## Download

Get the latest release from the [Releases](../../releases) page — no Python installation required!

## Usage

1. Run `ImageToCArray.exe`
2. Click to select an image
3. Configure options (array name, bytes per line, etc.)
4. Click "Convert & Save"
5. Include the generated `.h` file in your embedded project

## Output Example

```c
// RGB565 format, 240x240px, byte-swapped
const uint8_t picture_data[] = {
    248, 31, 248, 31, 0, 0, 7, 224, ...
};

// Image size: 240x240 pixels
// Data size: 115200 bytes
```

## Build from Source

### Requirements

- Python 3.8+
- Dependencies: `pip install -r requirements.txt`

### Run

```bash
python image_to_carray.py
```

### Build EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "ImageToCArray" image_to_carray.py
```

The executable will be in the `dist/` folder.

## RGB565 Format

RGB565 is a 16-bit color format commonly used in embedded displays:
- Red: 5 bits (0-31)
- Green: 6 bits (0-63)
- Blue: 5 bits (0-31)

## License

MIT License — see [LICENSE](LICENSE) file.

