import tkinter as tk
from PIL import Image, ImageTk
import os
# from utils.rounded_button import RoundedButton


class ImageViewer:
    def __init__(self, master, images):
        self.root = master
        self.images = images
        self.current_index = 0

        self.label = tk.Label(self.root)
        self.label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.prev_button = tk.Button(
            self.root, text="<<", command=self.show_previous_image, state="disabled", bg='cyan', fg='white', borderwidth=2, relief="raised")
        self.prev_button.grid(row=1, column=0, padx=10, pady=10)

        self.quit_button = tk.Button(
            self.root, text="Exit", command=self.root.quit, bg='red', fg='white', borderwidth=2, relief="raised")
        self.quit_button.grid(row=1, column=1, padx=10, pady=10)

        self.next_button = tk.Button(
            self.root, text=">>", command=self.show_next_image, bg='cyan', fg='white', borderwidth=2, relief="raised")
        self.next_button.grid(row=1, column=2, padx=10, pady=10)

        self.show_image()

        self.status = tk.Label(
            root, text=f"{self.current_index + 1} of {len(self.images)}", bd=1, relief=tk.SUNKEN, anchor=tk.E)
        self.status.grid(row=2, columns=3, padx=20,)  # sticky=tk.E+tk.W)

    def show_image(self):
        if self.images:  # Check if images list is not empty
            image_path = self.images[self.current_index]
            original_image = Image.open(image_path)
            # Define the desired width and height
            desired_width = 780  # Replace with your desired width
            desired_height = 520  # Replace with your desired height
            # Resize the image
            resized_image = original_image.resize(
                (desired_width, desired_height))
            photo = ImageTk.PhotoImage(resized_image)
            self.label.configure(image=photo)
            self.label.image = photo
        else:
            self.label.configure(
                text="No Image in gallery", font=('Arial', 20))
            self.next_button.configure(state="disabled")

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
            self.next_button.configure(state="normal")
            if self.current_index == 0:
                self.prev_button.configure(state="disabled")
            self.status.configure(
                text=f"{self.current_index + 1} of {len(self.images)}")

    def show_next_image(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.show_image()
            self.prev_button.configure(state="normal")
            if self.current_index == len(self.images) - 1:
                self.next_button.configure(state="disabled")
            self.status.configure(
                text=f"{self.current_index + 1} of {len(self.images)}")


path_to_images = "images/"
images = [os.path.join(path_to_images, file) for file in os.listdir(
    path_to_images) if file.endswith(('.png', '.jpg', '.jpeg'))]

# Cerate tkinter root
root = tk.Tk()
root.title('Gallery')
root.geometry('800x650')

# # Load the icon file
# icon_path = '/home/timihack/Documents/Python/Tkinter_TUT/icons/viewer-icon.jpg'
# icon = tk.PhotoImage(file=icon_path)

# # Set the window icon
# root.iconphoto(False, icon)

# Create the image viewer app
image_viewer = ImageViewer(root, images)

# Run the Tkinter main loop
root.mainloop()
