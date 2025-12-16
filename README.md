# Image to RGB565 C-Array Converter

**Convert images to RGB565 C-arrays for embedded LCD/TFT displays**

> [!TIP]
> **Just include the generated .txt file into your embedded C project — and you're done!**

> One-click image converter for ST7789 SPI displays (and other displays in future). Testet with LVGL on STM32.
> Tested on an ST7789 SPI, 240х240 display.

## Installation

### 🟢 Easy Way (Windows)

1. Go to [Releases](../../releases)
2. Download `ImageToCArray.exe`
3. Run it — done!

> No installation, no Python, no dependencies. Just download and use.

---

### 🔧 From Source (Windows / macOS / Linux)

```bash
# Clone the repo
git clone https://github.com/djeentonic24/image-to-rgb565.git
cd image-to-rgb565

# Install dependencies
pip install -r requirements.txt

# Run
python image_to_carray.py
```

#### Build your own EXE (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "ImageToCArray" image_to_carray.py
```

The executable will be in the `dist/` folder.

## Features

- 🖼️ Convert any image (PNG, JPG, BMP, GIF) to RGB565 format
- 📐 Auto-resize to 240x240 pixels
- 🔄 Byte swap (Big Endian / Little Endian)
- 🎨 Invert colors option
- 💾 Export as .txt file

## Usage

1. Run `image_to_carray.py` or `ImageToCArray.exe` 
2. Click to select an image
3. Configure options
4. Click "Convert & Save"
5. Include the generated `.txt` file in your embedded project

## Output Code Example

```c
// RGB565 format, 240x240px
const uint8_t picture_data[] = {
    248, 31, 248, 31, 0, 0, 7, 224, ...
};

// Image size: 240x240 pixels
// Data size: 115200 bytes
```

Example using in a project with LVGL for a 240x240 screen:

```c
#include "starry_night.txt"  // GENERATED FILE. Has picture_data inside (see lines above)

lv_img_dsc_t picture_from_txt; //lv_img_dsc_t comes from lv_img_buf.h from a standard LVGL library

uint32_t expected_size = 240 * 240 * 2;
picture_from_txt.header.always_zero = 0;
picture_from_txt.header.w = 240;
picture_from_txt.header.h = 240;
picture_from_txt.header.cf = LV_IMG_CF_TRUE_COLOR;  // RGB565 
picture_from_txt.data_size = expected_size;  // 
picture_from_txt.data = (const uint8_t*)picture_data;  // from .txt file
```

Example: full-screen top layer using LVGL

```c
LV_IMG_DECLARE(picture_from_txt);
/*
...
*/
lv_obj_t * top_layer = lv_disp_get_layer_top(NULL);
lv_obj_t * img = lv_img_create(top_layer);
lv_img_set_src(img, &picture_from_txt);
lv_obj_set_size(img, 240, 240);
lv_obj_align(img, LV_ALIGN_CENTER, 0, 0);
lv_obj_move_foreground(img);
```

## Result Example

<img width="400" alt="App Screenshot" src="https://github.com/user-attachments/assets/1c803f46-7088-49f7-a5d9-f5b77ad07c69" />

<img width="500" alt="Display Result" src="https://github.com/user-attachments/assets/8f75fc52-88f3-460c-b0ae-eb71c9fb8fbb" />

## RGB565 Format

RGB565 is a 16-bit color format commonly used in embedded displays:
- Red: 5 bits (0-31)
- Green: 6 bits (0-63)
- Blue: 5 bits (0-31)

## License

MIT License — see [LICENSE](LICENSE) file.

## TODO
- Other resolutions
- Auto-settings for choosen screen

