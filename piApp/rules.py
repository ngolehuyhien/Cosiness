class Rules(object):
    def __init__(self):
        self.rule_weight = 1
        self.antecedent = []
        self.combinations = []
        self.parent = ""
        self.consequence_val = []
        self.matching_degree = None
        self.activation_weight = None
