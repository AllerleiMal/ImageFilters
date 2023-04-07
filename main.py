import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2

class App:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing App")
        self.initial_image = None

        self.image_path = ""
        self.image = None

        self.sigma = tk.DoubleVar()
        self.sigma.set(1.0)
        self.threshold = tk.DoubleVar()
        self.threshold.set(127)
        self.block_size = tk.IntVar()
        self.block_size.set(11)
        self.constant = tk.DoubleVar()
        self.constant.set(2)
        self.width = 0
        self.height = 0

        self.create_widgets()

    def resize_image(self, image):
        return image.resize((int(self.width), int(self.height)))

    def create_widgets(self):
        # Frame for image display
        self.image_frame = tk.Frame(self.master, width=512, height=512)
        self.image_frame.pack(side=tk.TOP, padx=5, pady=5, expand=False)

        # Image display
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(expand=False)

        # Frame for filter controls
        self.filter_frame = tk.Frame(self.master)
        self.filter_frame.pack(side=tk.TOP, padx=5, pady=5)

        # High-pass filter control
        self.highpass_label = tk.Label(self.filter_frame, text="High-pass Filter")
        self.highpass_label.grid(row=0, column=0, sticky=tk.W)
        self.highpass_button = tk.Button(self.filter_frame, text="Apply", command=self.highpass_filter)
        self.highpass_button.grid(row=0, column=1, padx=5)

        # Thresholding controls
        self.threshold_label = tk.Label(self.filter_frame, text="Thresholding")
        self.threshold_label.grid(row=2, column=0, sticky=tk.W)
        self.threshold_button = tk.Button(self.filter_frame, text="Apply", command=self.thresholding)
        self.threshold_button.grid(row=2, column=1, padx=5)
        self.threshold_slider = tk.Scale(self.filter_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200, label="Threshold", variable=self.threshold)
        self.threshold_slider.grid(row=2, column=2, padx=5)

        # Adaptive thresholding controls
        self.adaptive_label = tk.Label(self.filter_frame, text="Adaptive Thresholding")
        self.adaptive_label.grid(row=3, column=0, sticky=tk.W)
        self.adaptive_button = tk.Button(self.filter_frame, text="Apply", command=self.adaptive_thresholding)
        self.adaptive_button.grid(row=3, column=1, padx=5)
        self.adaptive_block_size_entry = tk.Entry(self.filter_frame, width=5, textvariable=self.block_size)
        self.adaptive_block_size_entry.grid(row=3, column=2, padx=5)
        self.adaptive_block_size_label = tk.Label(self.filter_frame, text="Block Size")
        self.adaptive_block_size_label.grid(row=3, column=3)
        self.adaptive_constant_entry = tk.Entry(self.filter_frame, width=5, textvariable=self.constant)
        self.adaptive_constant_entry.grid(row=3, column=4, padx=5)
        self.adaptive_constant_label = tk.Label(self.filter_frame, text="Constant")
        self.adaptive_constant_label.grid(row=3, column=5)

        # Frame for file controls
        self.file_frame = tk.Frame(self.master)
        self.file_frame.pack(side=tk.TOP, padx=5, pady=5)

        # File selection control
        self.file_label = tk.Label(self.file_frame, text="Select Image")
        self.file_label.grid(row=0, column=0)
        self.file_button = tk.Button(self.file_frame, text="Browse", command=self.open_file)
        self.file_button.grid(row=0, column=1, padx=5)
        self.filename_label = tk.Label(self.file_frame, text="")
        self.filename_label.grid(row=0, column=2)

    def open_file(self):
        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        self.image = Image.open(self.image_path)
        width = self.image.size[0]
        height = self.image.size[1]
        if width > height:
            self.width = 512
            self.height = height * (1.0 * self.width / width)
        else:
            self.height = 512
            self.width = width * (1.0 * self.height / height)
        self.image = self.resize_image(self.image)
        self.image = self.image.convert("L") # convert to grayscale
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.image)
        self.filename_label.config(text=self.image_path)

    def highpass_filter(self):
        if self.image is not None:
            img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            filtered_img = cv2.filter2D(img, -1, kernel)
            filtered_img = Image.fromarray(filtered_img)
            filtered_img = self.resize_image(filtered_img)
            filtered_img = ImageTk.PhotoImage(filtered_img)
            self.image_label.config(image=filtered_img)
            self.image_label.image = filtered_img

    def thresholding(self):
        if self.image is not None:
            img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            threshold = self.threshold.get()
            _, filtered_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            filtered_img = Image.fromarray(filtered_img)
            filtered_img = self.resize_image(filtered_img)
            filtered_img = ImageTk.PhotoImage(filtered_img)
            self.image_label.config(image=filtered_img)
            self.image_label.image = filtered_img

    def adaptive_thresholding(self):
        if self.image is not None:
            img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            block_size = self.block_size.get()
            constant = self.constant.get()
            filtered_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, constant)
            filtered_img = Image.fromarray(filtered_img)
            filtered_img = self.resize_image(filtered_img)
            filtered_img = ImageTk.PhotoImage(filtered_img)
            self.image_label.config(image=filtered_img)
            self.image_label.image = filtered_img

root = tk.Tk()
app = App(root)
root.mainloop()
