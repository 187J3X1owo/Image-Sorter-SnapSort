import json
import sys, os, shutil
from pathlib import Path

from PIL import Image, ImageQt

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog,
    QHBoxLayout, QVBoxLayout, QMessageBox, QLineEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

IMAGE_EXTS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp",
    ".heic", ".heif"
}
SETTINGS_FILE = Path(__file__).with_name("image_viewer_settings.json")

def is_image(p: Path):
    return p.suffix.lower() in IMAGE_EXTS

def load_settings():
    if not SETTINGS_FILE.exists():
        return {}
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_settings(data):
    SETTINGS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Inspector")
        self.images = []
        self.index = 0
        self.current_folder = None
        self.dest_folder = None
        self.settings = load_settings()

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        left_col = QVBoxLayout()
        self.img_label = QLabel("No image")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setFixedSize(800, 600)
        left_col.addWidget(self.img_label)

        nav_row = QHBoxLayout()
        self.prev_btn = QPushButton("◀ Prev (K)")
        self.next_btn = QPushButton("Next (J) ▶")
        self.move_btn = QPushButton("Copy (E)")
        self.delete_btn = QPushButton("Delete (T)")
        self.select_folder_btn = QPushButton("Select Folder")
        nav_row.addWidget(self.prev_btn)
        nav_row.addWidget(self.next_btn)
        nav_row.addWidget(self.move_btn)
        nav_row.addWidget(self.delete_btn)
        nav_row.addWidget(self.select_folder_btn)
        left_col.addLayout(nav_row)

        self.status_line = QLineEdit()
        self.status_line.setReadOnly(True)
        left_col.addWidget(self.status_line)

        main_layout.addLayout(left_col)

        right_col = QVBoxLayout()
        right_col.setSpacing(6)
        right_col.setContentsMargins(6, 0, 0, 0)
        right_col.addWidget(QLabel("Image Details"))
        self.details = QLabel("")
        self.details.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.details.setWordWrap(True)
        self.details.setFixedWidth(260)
        right_col.addWidget(self.details)
        right_col.addStretch()
        main_layout.addLayout(right_col)

        self.prev_btn.clicked.connect(self.show_prev)
        self.next_btn.clicked.connect(self.show_next)
        self.move_btn.clicked.connect(self.copy_current)
        self.delete_btn.clicked.connect(self.delete_current)
        self.select_folder_btn.clicked.connect(self.select_folder)

        self.restore_saved_state()
        self.update_ui()

    def restore_saved_state(self):
        saved_folder = self.settings.get("current_folder")
        if saved_folder and Path(saved_folder).is_dir():
            self.current_folder = Path(saved_folder)
            self.images = sorted([p for p in self.current_folder.iterdir() if p.is_file() and is_image(p)])
            saved_image = self.settings.get("last_image_path")
            if saved_image and Path(saved_image).is_file() and is_image(Path(saved_image)):
                saved_path = Path(saved_image)
                if saved_path.parent == self.current_folder and saved_path in self.images:
                    self.index = self.images.index(saved_path)
                else:
                    self.index = 0
            else:
                self.index = 0
            self.show_image()

        saved_dest = self.settings.get("dest_folder")
        if saved_dest and Path(saved_dest).is_dir():
            self.dest_folder = Path(saved_dest)

    def save_state(self):
        data = {}
        if self.current_folder is not None:
            data["current_folder"] = str(self.current_folder)
        if self.dest_folder is not None:
            data["dest_folder"] = str(self.dest_folder)
        if self.images and 0 <= self.index < len(self.images):
            data["last_image_path"] = str(self.images[self.index])
        save_settings(data)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select folder to browse", os.path.expanduser("~"))
        if folder:
            self.current_folder = Path(folder)
            self.images = sorted([p for p in self.current_folder.iterdir() if p.is_file() and is_image(p)])
            saved_image = self.settings.get("last_image_path")
            if saved_image and Path(saved_image).is_file() and Path(saved_image).parent == self.current_folder and is_image(Path(saved_image)):
                self.index = self.images.index(Path(saved_image)) if Path(saved_image) in self.images else 0
            else:
                self.index = 0
            if not self.images:
                QMessageBox.information(self, "No images", "No image files found in that folder.")
            self.save_state()
            self.update_ui()
            self.show_image()

    def update_ui(self):
        total = len(self.images)
        self.status_line.setText(
            f"Folder: {self.current_folder or 'None'}  —  {self.index+1 if total else 0}/{total}"
        )
        self.details.setText(self._details_text() if total else "")

    def _details_text(self):
        if not self.images:
            return ""
        p = self.images[self.index]
        try:
            im = Image.open(p)
            fmt = im.format
            w, h = im.size
            im.close()
        except Exception:
            fmt = "Unknown"
            w = h = "?"
        size = p.stat().st_size
        copied = "Yes" if self.dest_folder and (self.dest_folder / p.name).exists() else "No"
        return (
            f"Name: {p.name}\n"
            f"Path: {p}\n"
            f"Format: {fmt}\n"
            f"Dimensions: {w} x {h}\n"
            f"Size: {size} bytes\n"
            f"Copied: {copied}"
        )

    def show_image(self):
        if not self.images:
            self.img_label.setText("No image")
            self.save_state()
            return
        p = self.images[self.index]
        pix = None

        try:
            with Image.open(p) as img:
                img.load()
                if img.mode not in ("RGB", "RGBA", "L"):
                    img = img.convert("RGBA")
                qimage = ImageQt.ImageQt(img)
                pix = QPixmap.fromImage(qimage)
        except Exception:
            pix = QPixmap(str(p))

        if pix is None or pix.isNull():
            self.img_label.setText("Cannot load image")
            self.save_state()
            return

        scaled = pix.scaled(
            self.img_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.img_label.setPixmap(scaled)
        self.save_state()
        self.update_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.show_image()

    def show_prev(self):
        if not self.images: return
        self.index = (self.index - 1) % len(self.images)
        self.show_image()

    def show_next(self):
        if not self.images: return
        self.index = (self.index + 1) % len(self.images)
        self.show_image()

    def copy_current(self):
        if not self.images:
            return
        if not self.dest_folder:
            folder = QFileDialog.getExistingDirectory(self, "Select destination folder", os.path.expanduser("~"))
            if not folder:
                return
            self.dest_folder = Path(folder)
            self.save_state()
        src = self.images[self.index]
        dst = self.dest_folder / src.name
        try:
            shutil.copy2(str(src), str(dst))
        except Exception as e:
            QMessageBox.critical(self, "Error copying file", str(e))
            return
        self.save_state()
        self.update_ui()

    def delete_current(self):
        if not self.images:
            return
        p = self.images[self.index]
        reply = QMessageBox.question(
            self,
            "Delete image",
            f"Delete {p.name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        try:
            p.unlink()
        except Exception as e:
            QMessageBox.critical(self, "Error deleting file", str(e))
            return
        del self.images[self.index]
        if self.index >= len(self.images) and self.images:
            self.index = len(self.images) - 1
        if not self.images:
            self.img_label.clear()
            self.img_label.setText("No image")
        self.save_state()
        self.update_ui()
        self.show_image()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_J:
            self.show_prev()
        elif key == Qt.Key.Key_L:
            self.show_next()
        elif key == Qt.Key.Key_E:
            self.copy_current()
        elif key == Qt.Key.Key_T:
            self.delete_current()
        elif key == Qt.Key.Key_O:
            self.select_folder()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageViewer()
    w.resize(1100, 700)
    w.show()
    sys.exit(app.exec())