import Tkinter as tk
import matplotlib.cm as cm
import tkMessageBox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import pyplot as plt


class CellPicker(object):

    def __init__(self, image_manager, cells_manager):
        self.image_manager = image_manager
        self.cells_manager = cells_manager

        self.wt_cells = []
        self.donor_cells = []
        self.acceptor_cells = []
        self.both_cells = []
        self.septum_cells = []

        self.current_index = 0
        self.cells_id = sorted(self.cells_manager.cells.keys())

        # GUI
        self.main_window = tk.Tk()
        self.main_window.wm_title("Cellpicker")

        self.top_frame = tk.Frame(self.main_window)
        self.top_frame.pack(fill="x")

        self.middle_frame = tk.Frame(self.main_window)
        self.middle_frame.pack(fill="x")

        self.bottom_frame = tk.Frame(self.main_window)
        self.bottom_frame.pack(fill="x")

        self.previous_button = tk.Button(self.top_frame,
                                         text="Back",
                                         command=self.previous_cell)
        self.previous_button.pack(side="right")

        self.no_septum_frame = tk.Frame(self.bottom_frame)
        self.no_septum_frame.pack(side="top", fill="x")

        self.ns_label = tk.Label(self.no_septum_frame, text="No Septum:")
        self.ns_label.pack(side="left", fill="x")

        self.ns_wt_button = tk.Button(self.no_septum_frame, text="wt (Q)", command=lambda: self.select_channel("wt", False))
        self.ns_wt_button.pack(side="left")

        self.ns_dd_button = tk.Button(self.no_septum_frame, text="Donor (W)", command=lambda: self.select_channel("donor", False))
        self.ns_dd_button.pack(side="left")

        self.ns_aa_button = tk.Button(self.no_septum_frame, text="Acceptor (E)", command=lambda: self.select_channel("acceptor", False))
        self.ns_aa_button.pack(side="left")

        self.ns_both_button = tk.Button(self.no_septum_frame, text="Both (R)", command=lambda: self.select_channel("both", False))
        self.ns_both_button.pack(side="left")

        self.septum_frame = tk.Frame(self.bottom_frame)
        self.septum_frame.pack(side="top", fill="x")

        self.se_label = tk.Label(self.septum_frame, text="Has Septum:")
        self.se_label.pack(side="left", fill="x")

        self.se_wt_button = tk.Button(self.septum_frame, text="wt (A)", command=lambda: self.select_channel("wt", True))
        self.se_wt_button.pack(side="left")
        
        self.se_donor_button = tk.Button(self.septum_frame, text="Donor (S)", command=lambda: self.select_channel("donor", True))
        self.se_donor_button.pack(side="left")

        self.se_acceptor_button = tk.Button(self.septum_frame, text="Acceptor (D)", command=lambda: self.select_channel("acceptor", True))
        self.se_acceptor_button.pack(side="left")

        self.se_both_button = tk.Button(self.septum_frame, text="Both (F)", command=lambda: self.select_channel("both", True))
        self.se_both_button.pack(side="left")

        self.discard_button = tk.Button(self.bottom_frame, text="Discard Cell (X)", command=lambda: self.select_channel("discard", False))
        self.discard_button.pack(side="left")

        self.label_text = tk.StringVar()
        self.label_text.set("No Cells Selected")
        self.number_of_cells_label = tk.Label(
            self.top_frame, textvariable=self.label_text)
        self.number_of_cells_label.pack()

        # creates the figure canvas
        self.fig = plt.figure(figsize=(12, 8), frameon=True)
        self.canvas = FigureCanvasTkAgg(self.fig, self.middle_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side="top")

        self.ax = plt.subplot(111)
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.ax.axis("off")
        plt.autoscale(False)
        
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.middle_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(fill="both")
        
        self.ax.format_coord = self.show_nothing

        self.main_window.bind("<Key>", self.key)

        self.show_image()

    def key(self, event):
        if event.char == "q":
            self.select_channel("wt", False)
        elif event.char == "w":
            self.select_channel("donor", False)
        elif event.char == "e":
            self.select_channel("acceptor", False)
        elif event.char == "r":
            self.select_channel("both", False)
        elif event.char == "a":
            self.select_channel("wt", True)
        elif event.char == "s":
            self.select_channel("donor", True)
        elif event.char == "d":
            self.select_channel("acceptor", True)
        elif event.char == "f":
            self.select_channel("both", True)
        elif event.char == "x":
            self.select_channel("discard", False)
        elif event.char == "b":
            self.previous_cell()

    def show_nothing(self, x, y):
        
        return ""

    def previous_cell(self):

        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
        else:
            pass

    def select_channel(self, channel, has_septum):
        
        self.cells_manager.cells[self.cells_id[self.current_index]].channel = channel
        self.cells_manager.cells[self.cells_id[self.current_index]].has_septum = has_septum

        if self.current_index < len(self.cells_id)-1:
            self.current_index += 1
            self.show_image()

        else:
            if tkMessageBox.askokcancel("Quit", "Last cell, generate report?"):
                self.main_window.destroy()
            else:
                self.show_image()

    def show_image(self):
        
        self.ax.cla()

        current_image = self.cells_manager.cells[self.cells_id[self.current_index]].donacc_image

        self.ax.imshow(current_image, cmap=cm.gray)
        self.label_text.set(str(self.current_index+1) + " of " + str(len(self.cells_id)) + " total")
        self.canvas.show()
