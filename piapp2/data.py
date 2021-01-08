class Data(object):

    def __init__(self, antecedent_id, antecedent_name,
                 attribute_weight, ref_val, ref_title,
                 parent, is_input, input_val="0"):

        self.name = ""
        self.antecedent_id = antecedent_id
        self.antecedent_name = antecedent_name
        self.attribute_weight = attribute_weight
        self.ref_title = ref_title
        self.ref_val = ref_val
        self.parent = parent
        self.input_val = input_val
        self.transformed_val = [0 for _ in range(len(self.ref_val))]
        self.is_input = is_input
