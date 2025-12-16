"""
Image to C-Array Converter (RGB565 format with Byte Swap)
Converts images to RGB565 C-style byte arrays with swapped byte pairs
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import os


class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Image → RGB565 C-Array")
        self.geometry("700x750")
        self.minsize(600, 700)
        
        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.image_path = None
        self.pil_image = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="🖼️ Image to RGB565",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Convert images to RGB565 C arrays (byte-swapped)",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 25))
        
        # Drop zone / Preview area
        self.preview_frame = ctk.CTkFrame(
            self.main_frame,
            height=250,
            corner_radius=15,
            border_width=2,
            border_color="#3b82f6"
        )
        self.preview_frame.pack(fill="x", pady=(0, 20))
        self.preview_frame.pack_propagate(False)
        
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="📂 Click to select an image\n\nSupported: PNG, JPG, BMP, GIF",
            font=ctk.CTkFont(size=16),
            text_color="#64748b"
        )
        self.preview_label.pack(expand=True)
        self.preview_frame.bind("<Button-1>", lambda e: self.select_image())
        self.preview_label.bind("<Button-1>", lambda e: self.select_image())
        
        # File info
        self.info_label = ctk.CTkLabel(
            self.main_frame,
            text="No image selected",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.info_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 20))
        
        # Select button
        self.select_btn = ctk.CTkButton(
            buttons_frame,
            text="📁 Select Image",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            command=self.select_image
        )
        self.select_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # Convert button
        self.convert_btn = ctk.CTkButton(
            buttons_frame,
            text="⚡ Convert & Save",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#10b981",
            hover_color="#059669",
            command=self.convert_and_save,
            state="disabled"
        )
        self.convert_btn.pack(side="right", expand=True, fill="x", padx=(10, 0))
        
        # Options frame
        options_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        options_frame.pack(fill="x", pady=(0, 20))
        
        options_label = ctk.CTkLabel(
            options_frame,
            text="⚙️ Options",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        options_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Bytes per line
        bpl_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        bpl_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            bpl_frame,
            text="Bytes per line:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")
        
        self.bytes_per_line = ctk.CTkEntry(
            bpl_frame,
            width=80,
            height=32,
            placeholder_text="12"
        )
        self.bytes_per_line.insert(0, "12")
        self.bytes_per_line.pack(side="right")
        
        # Array name
        name_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            name_frame,
            text="Array name:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")
        
        self.array_name = ctk.CTkEntry(
            name_frame,
            width=200,
            height=32,
            placeholder_text="picture_data"
        )
        self.array_name.insert(0, "picture_data")
        self.array_name.pack(side="right")
        
        # Invert colors checkbox
        invert_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        invert_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.invert_var = ctk.BooleanVar(value=False)
        self.invert_checkbox = ctk.CTkCheckBox(
            invert_frame,
            text="Invert colors",
            font=ctk.CTkFont(size=13),
            variable=self.invert_var
        )
        self.invert_checkbox.pack(side="left")
        
        # Endianness toggle
        endian_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        endian_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            endian_frame,
            text="Byte order:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")
        
        self.endian_var = ctk.StringVar(value="big")
        self.endian_toggle = ctk.CTkSegmentedButton(
            endian_frame,
            values=["Big Endian", "Little Endian"],
            variable=self.endian_var,
            command=self._on_endian_change
        )
        self.endian_toggle.set("Big Endian")
        self.endian_toggle.pack(side="right")
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready • RGB565 format (16-bit color, byte-swapped)",
            font=ctk.CTkFont(size=11),
            text_color="#64748b"
        )
        self.status_label.pack(side="bottom", pady=(10, 0))
    
    def select_image(self):
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("BMP", "*.bmp"),
            ("All files", "*.*")
        ]
        
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )
        
        if path:
            self.image_path = path
            self._load_preview()
    
    def _load_preview(self):
        try:
            # Load image with PIL
            self.pil_image = Image.open(self.image_path).convert("RGB")
            
            # Calculate output size (always 240x240)
            width, height = self.pil_image.size
            output_bytes = 240 * 240 * 2  # 2 bytes per pixel (RGB565)
            
            # Create preview thumbnail
            preview_img = self.pil_image.copy()
            display_size = (200, 200)
            preview_img.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(preview_img)
            
            # Update preview
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo  # Keep reference
            
            # Update info
            filename = os.path.basename(self.image_path)
            self.info_label.configure(
                text=f"📄 {filename}  •  {width}×{height}px → 240×240px  •  Output: {output_bytes:,} bytes",
                text_color="#10b981"
            )
            
            # Enable convert button
            self.convert_btn.configure(state="normal")
            self.status_label.configure(text=f"Image loaded: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            self.status_label.configure(text="Error loading image")
    
    def _on_endian_change(self, value):
        """Handle endianness toggle change"""
        pass  # Just for UI feedback
    
    def rgb_to_rgb565(self, r, g, b):
        """Convert RGB888 to RGB565"""
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    
    def convert_and_save(self):
        if not self.pil_image:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        
        try:
            # Get options
            bytes_per_line = int(self.bytes_per_line.get() or 12)
            arr_name = self.array_name.get() or "picture_data"
            
            # Resize to 240x240
            img_resized = self.pil_image.resize((240, 240), Image.Resampling.LANCZOS)
            
            # Invert colors if checkbox is checked
            if self.invert_var.get():
                img_resized = ImageOps.invert(img_resized)
            
            width, height = img_resized.size
            pixels = img_resized.load()
            
            # Convert to RGB565 with byte swap
            swapped = []
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    rgb565 = self.rgb_to_rgb565(r, g, b)
                    
                    # Split into 2 bytes
                    high_byte = (rgb565 >> 8) & 0xFF
                    low_byte = rgb565 & 0xFF
                    
                    # Byte order based on endianness setting
                    if self.endian_toggle.get() == "Big Endian":
                        swapped.append(high_byte)
                        swapped.append(low_byte)
                    else:  # Little Endian
                        swapped.append(low_byte)
                        swapped.append(high_byte)
            
            # Generate C array
            c_array = f"// RGB565 format, {width}x{height}px, byte-swapped\n"
            c_array += f"const uint8_t {arr_name}[] = {{\n    "
            line_len = 0
            
            for i, b in enumerate(swapped):
                c_array += f"{b}"
                if i < len(swapped) - 1:
                    c_array += ", "
                line_len += 1
                if line_len >= bytes_per_line and i < len(swapped) - 1:
                    c_array += "\n    "
                    line_len = 0
            
            c_array += "\n};\n"
            c_array += f"\n// Image size: {width}x{height} pixels\n"
            c_array += f"// Data size: {len(swapped)} bytes\n"
            
            # Save file
            default_name = os.path.splitext(os.path.basename(self.image_path))[0] + "_rgb565.txt"
            
            save_path = filedialog.asksaveasfilename(
                title="Save RGB565 C-Array",
                defaultextension=".txt",
                initialfile=default_name,
                filetypes=[("Text files", "*.txt"), ("Header files", "*.h"), ("All files", "*.*")]
            )
            
            if save_path:
                with open(save_path, "w") as f:
                    f.write(c_array)
                
                self.status_label.configure(text=f"✅ Saved to: {os.path.basename(save_path)}")
                messagebox.showinfo(
                    "Success", 
                    f"RGB565 C-Array saved!\n\n"
                    f"File: {save_path}\n"
                    f"Image: {width}×{height}px\n"
                    f"Size: {len(swapped):,} bytes"
                )
        
        except ValueError:
            messagebox.showerror("Error", "Invalid 'Bytes per line' value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")
            self.status_label.configure(text="Error during conversion")


if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()
