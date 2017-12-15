from cellpicker import CellPicker


class FRETManager(object):

    def __init__(self):
        self.wt_cells = []
        self.donor_cells = []
        self.acceptor_cells = []
        self.both_cells = []

        self.autofluorescence_donor = None
        self.autofluorescence_acceptor = None
        self.autofluorescence_fret = None

        self.fret_a = None
        self.fret_b = None
        self.fret_c = None
        self.fret_d = None

        self.fret_fc = None
        self.fret_g = None

        self.fret_heatmap = None

    def start_channel_picker(self, image_manager, cells_manager):
        picker = CellPicker(image_manager, cells_manager)
        picker.main_window.mainloop()

        for key in cells_manager.cells.keys():
            if cells_manager.cells[key].channel == "donor":
                self.donor_cells.append(key)
            elif cells_manager.cells[key].channel == "wt":
                self.wt_cells.append(key)
            elif cells_manager.cells[key].channel == "acceptor":
                self.acceptor_cells.append(key)
            elif cells_manager.cells[key].channel == "both":
                self.both_cells.append(key)

    def compute_autofluorescence(self, image_manager, cells_manager):
        pass

    def compute_correction_factors(self, image_manager, cells_manager):
        pass

    def compute_g(self, image_manager, cells_manager):
        pass

    def compute_fret_efficiency(self, image_manager, cells_manager):
        # TODO create heatmap here
        
        pass
