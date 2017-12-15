from setmanager import SetManager


class PyFRET(object):

    def __init__(self):
        self.sets = {"Control": SetManager(), "Experiment": SetManager()}

    def process_control(self):
        pass

    def process_experiment(self):
        # TODO create heatmap of E on this step
        pass

    def generate_report(self):
        pass
