from comparator.comparator import Comparator
from gate.and_gate import And
from gate.or_gate import Or


class HazardDetectionUnit:
    def __init__(self, rm_id_ex, rt_id_ex, rt_if_id, rs_if_id, name="HazardDetectionUnit"):
        self.rm_id_ex = rm_id_ex
        self.rt_id_ex = rt_id_ex
        self.rt_if_id = rt_if_id
        self.rs_if_id = rs_if_id

        self.name = name
        self.output = None

        self.build()

    def build(self):
        self.output = And((
            self.rm_id_ex,
            Or((
                Comparator((self.rt_id_ex, self.rs_if_id), 5),
                Comparator((self.rt_id_ex, self.rt_if_id), 5)
            ))
        ))

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        self.output.logic(depend + [self])
        return self.output.output
