# Image-Sorter
A tool for inspection and direct filtering or sorting of images from the original folder to another

# 📷 Image Viewer & Filter Tool

A powerful Windows application for quickly browsing, inspecting, and organizing image files using keyboard shortcuts.

## ✨ Features

- **📁 Folder Selection**: Browse and select any folder containing images
- **🖼️ Image Display**: View images with proper scaling and aspect ratio
- **📋 Image Details**: View comprehensive information about each image:
  - File name
  - Dimensions (width × height)
  - File size
  - Image format
  - Color mode
  - File location
- **⌨️ Keyboard Navigation**:
  - `J` → Previous image
  - `L` → Next image
  - `E` → Move/Copy image to destination folder
  - `T` → Delete current image
  - `O` → Select source folder
- **🖱️ Mouse Controls**: Click navigation buttons or use arrow buttons
- **📤 Image Management**: Quickly filter images by moving or deleting them

## 🚀 Installation

### Prerequisites
- Windows OS
- Python 3.6 or higher
- [Anaconda](https://www.anaconda.com/) (recommended) or Python installed

### Step 1: Install Required Package

Open Command Prompt or Terminal and run:

```bash
pip install pillow
```

Or if using Anaconda:

```bash
conda install pillow
```

### Step 2: Download the Application

1. Save the Python script as `image_viewer.pyw`
2. Place it in your desired folder (e.g., `C:\Users\YourName\Desktop\Image Viewer\`)

### Step 3: Run the Application

Simply **double-click** the `image_viewer.pyw` file - it will run without opening a command window!

## How to Use

### 1. Select Source Folder
- Press `O` on your keyboard OR
- Click the **"📁 Select Source"** button
- Browse and select the folder containing your images

### 2. Select Destination Folder (Optional)
- Click the **"📂 Select Dest"** button
- Choose where to move images you want to keep

### 3. Navigate Through Images
- **Previous**: Press `J` or click the **"◀ Previous (J)"** button
- **Next**: Press `L` or click the **"Next (L) ▶"** button

### 4. Manage Images
- **Move/Copy**: Press `E` or click **"📤 Move to Dest (E)"** to move the current image to the destination folder
- **Delete**: Press `T` or click **"🗑️ Delete"** to permanently delete the current image

### 5. View Image Details
The right sidebar displays all relevant information about the currently viewed image.

## ⌨️ Keyboard Shortcuts Summary

| Key | Action |
|-----|--------|
| `J` | Previous image |
| `L` | Next image |
| `E` | Move image to destination folder |
| `T` | Delete current image |
| `O` | Open/Select source folder |
| `←` | Previous image (alternative) |
| `→` | Next image (alternative) |

## 📝 Notes

- **File Types Supported**: JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP, and more
- **Corrupted Files**: The app automatically skips corrupted or invalid image files
- **Performance**: Optimized for large folders with hundreds of images

## 🐛 Troubleshooting

### "Cannot load image" Error
- The image file might be corrupted or in an unsupported format

### Keyboard Shortcuts Not Working
- Make sure the app window has focus (click on it)
- Check that caps lock isn't interfering with shortcuts

## 🛠️ Advanced Setup

### Create a Batch File (Created for you)
Create `run.bat` in the same folder:

```batch
@echo off
start "" pythonw.exe "%~dp0image_viewer.pyw"
exit
```

## 🔧 Development

### Project Structure
```
Image Viewer/
├── image_viewer.pyw    # Main application
└── README.md           # Documentation
```

### Built With
- [Python](https://www.python.org/) - Programming language
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework
- [Pillow (PIL)](https://python-pillow.org/) - Image processing library

## 📄 License

This project is open-source and available for personal and commercial use.

## 🤝 Support

If you encounter any issues or have suggestions:
1. Check the troubleshooting guide
2. Ensure all dependencies are installed
3. Contact your system administrator for permission-related issues

---

**Happy Image Organizing! 🎉**
