from Components.branch_prediction.two_bit_saturating_counter import TwoBitSaturatingCounter


class BranchPredictionUnit:
    def __init__(self, branch_status, clock, name="branch_prediction_unit"):
        self.clock = clock
        self.name = name
        self.branch_status = branch_status  # branch state in second stage
        self.output = None
        self.build()

    def build(self):
        self.output = TwoBitSaturatingCounter(self.branch_status, self.clock)

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        self.output.logic(depend + [self])
        return self.output.get_output()

    def get_output(self):
        return self.output.get_output()
