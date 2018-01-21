from setmanager import SetManager
from reportsmanager import ReportsManager
from parameters import ParametersManager


class PyFRET(object):

    def __init__(self):
        self.sets = {"Control": SetManager(), "Experiment": SetManager()}
        self.parameters = ParametersManager()
        self.reports_manager = ReportsManager(self.parameters)

    def process_control(self):
        self.sets["Control"].load_phase_image()
        self.sets["Control"].compute_mask()
        self.sets["Control"].load_fluor_image("Donor")
        self.sets["Control"].load_fluor_image("Acceptor")
        self.sets["Control"].load_fluor_image("FRET")
        self.sets["Control"].compute_segments()
        self.sets["Control"].compute_cells()
        self.sets["Control"].process_cells()
        self.sets["Control"].pick_channel()
        self.sets["Control"].compute_autofluorescence()
        self.sets["Control"].compute_correction_factors()
        self.sets["Control"].compute_g()
        self.generate_report("Control", self.sets["Control"])

    def process_experiment(self):
        self.sets["Experiment"].load_phase_image()
        self.sets["Experiment"].compute_mask()
        self.sets["Experiment"].load_fluor_image("Donor")
        self.sets["Experiment"].load_fluor_image("Acceptor")
        self.sets["Experiment"].load_fluor_image("FRET")
        self.sets["Experiment"].compute_segments()
        self.sets["Experiment"].compute_cells()
        self.sets["Experiment"].process_cells()
        self.sets["Experiment"].pick_channel()
        self.sets["Experiment"].compute_autofluorescence()
        self.sets["Experiment"].compute_correction_factors()
        self.sets["Experiment"].compute_fret_efficiency()
        self.generate_report("Experiment", self.sets["Experiment"])

    def generate_report(self, setname, set_manager):
        self.reports_manager.generate_report(setname, set_manager)
