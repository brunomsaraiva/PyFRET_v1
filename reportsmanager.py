import cellprocessing as cp

class ReportsManager(object):

    def __init__(self, parameters):
        self.keys = cp.stats_format(parameters.cellprocessingparams)
        self.average_G = None
        self.average_cell_E = None
        self.average_septum_E = None

    def generate_report_control(self, image_manager, cells_manager, fret_manager):
        pass

    def generate_report_experiment(self, image_manager, cells_manager, fret_manager):
        pass

    def generate_report(self, setname, image_manager, cells_manager, fret_manager):

        if setname == "Control":
            self.generate_report_control(image_manager, cells_manager, fret_manager)
        elif setname == "Experiment":
            self.generate_report_experiment(image_manager, cells_manager, fret_manager)
