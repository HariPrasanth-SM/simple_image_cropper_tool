import os
import argparse
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button, TextBox
import imageio.v2 as imageio

class ImageCropper:
    def __init__(self, image_path, save_dir="crops"):
        self.image_path = image_path
        # Load grayscale image properly
        self.image = imageio.imread(image_path)
        if self.image.ndim == 2:  # grayscale
            pass  # already grayscale
        else:
            raise ValueError("Image is not grayscale as expected.")

        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

        # plot setup
        self.fig, (self.ax_img, self.ax_crop) = plt.subplots(1, 2, figsize=(10, 5))
        self.ax_img.imshow(self.image, cmap='gray')
        self.ax_img.set_title("Original Image")
        self.ax_crop.set_title("Cropped Region")
        self.ax_crop.axis("off")

        # selector (API updated, no drawtype)
        self.selector = RectangleSelector(
            self.ax_img,
            self.onselect,
            useblit=True,
            button=[1],  # left mouse only
            minspanx=5,
            minspany=5,
            spancoords='pixels',
            interactive=True
        )

        # text box for filename
        axbox = plt.axes([0.25, 0.02, 0.15, 0.05])
        self.text_box = TextBox(axbox, 'Filename', initial="crop")

        # button
        ax_button = plt.axes([0.45, 0.02, 0.1, 0.05])
        self.button = Button(ax_button, 'Save Crop')
        self.button.on_clicked(self.save_crop)

        # storage
        self.current_crop = None
        self.crop_count = 0

        plt.show()

    def onselect(self, eclick, erelease):
        """Callback when a rectangle is selected."""
        x1, y1 = int(eclick.xdata), int(eclick.ydata)
        x2, y2 = int(erelease.xdata), int(erelease.ydata)
        xmin, xmax = sorted([x1, x2])
        ymin, ymax = sorted([y1, y2])

        self.current_crop = self.image[ymin:ymax, xmin:xmax]
        self.ax_crop.clear()
        self.ax_crop.imshow(self.current_crop, cmap='gray')
        self.ax_crop.set_title("Cropped Region")
        self.ax_crop.axis("off")
        self.fig.canvas.draw()

    def save_crop(self, event):
        if self.current_crop is not None:
            filename = self.text_box.text.strip()
            if filename == "":
                filename = f"crop_{self.crop_count}"

            save_path = os.path.join(self.save_dir, f"{filename}.png")
            imageio.imwrite(save_path, self.current_crop)
            print(f"Saved: {save_path}")
            self.crop_count += 1
        else:
            print("No crop selected yet!")


# Example usage:
# ImageCropper("your_image.tif", save_dir="output_crops")

# Example usage:
if __name__ == "__main__":

    print("Simple Image cropper tool running!!!")

    parser = argparse.ArgumentParser(description='Image Cropper tool')
    parser.add_argument('--image_path', type=str, required=True)
    parser.add_argument('--output_dir', type=str, default="output_dir")

    args = parser.parse_args()

    ImageCropper(args.image_path, save_dir=args.output_dir)