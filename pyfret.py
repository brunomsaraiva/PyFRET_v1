from setmanager import SetManager


class PyFRET(object):

    def __init__(self):
        self.sets = {"Control": SetManager(), "Experiment": SetManager()}

    def process_control(self):
        pass

    def import_g(self):
        value = 0  # TODO

        self.sets["Experiment"].fret_manager.fret_g = value

    def process_experiment(self):
        # TODO create heatmap of E on this step
        pass

    def generate_report(self):
        pass
