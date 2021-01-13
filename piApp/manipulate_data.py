from rules import Rules


class RuleBase(object):
    def __init__(self, object_list, parent):
        self.obj_list = object_list
        self.intermediate_ref_val = 0
        self.rule_row_list = list()
        self.parent = parent
        self.con_ref_values = [0 for _ in range(len(self.parent.ref_val))]
        self.combinations = [[]]
        self.combinations2 = [[]]

    '''
    Create initial rule base
    '''

    def create_rule_base(self):
        cons_ref_val_1 = 0
        cons_ref_val_n = 0

        for each in self.obj_list:
            # Calculating the range of consequence values(First and last)
            cons_ref_val_1 += float(float(each.attribute_weight) * float(each.ref_val[0]))
            cons_ref_val_n += float(float(each.attribute_weight) * float(each.ref_val[len(each.ref_val) - 1]))

        self.con_ref_values[0] = cons_ref_val_1
        self.con_ref_values[len(self.con_ref_values) - 1] = cons_ref_val_n

        # Calculating intermediate values within the range.
        intermediate_cons_ref_val_num = len(self.parent.ref_val) - 1
        for i in range(1, intermediate_cons_ref_val_num):
            current_val = float(cons_ref_val_1 * (intermediate_cons_ref_val_num - i)) + float(cons_ref_val_n * i * 1.0)
            current_val /= (i + (intermediate_cons_ref_val_num - i))
            self.con_ref_values[i] = current_val

        # Calculating the number of possible combinations using the length of each referential values.
        array_for_ref_count = [[]]
        result = [[]]

        for each in self.obj_list:
            length = len(each.ref_val)
            temp = list()
            for i in range(length):
                temp.append(i)
            array_for_ref_count.append(temp)

        array = array_for_ref_count[1:]
        pools = [tuple(pool) for pool in array] * 1

        for pool in pools:
            result = [x + [y] for x in result for y in pool]

        for each in result:
            self.combinations.append(each)

        self.combinations = self.combinations[1:]

        y = [0 for _ in range(len(self.combinations))]

        # Calculating the number of possible combinations using the title of each referential values.
        array_for_ref_count2 = [[]]
        result2 = [[]]

        for each in self.obj_list:
            title = each.ref_title
            temp2 = list()
            for i in title:
                temp2.append(i)
            array_for_ref_count2.append(temp2)

        array2 = array_for_ref_count2[1:]
        pools2 = [tuple(pool) for pool in array2]

        for pool in pools2:
            result2 = [x + [y] for x in result2 for y in pool]

        for each in result2:
            self.combinations2.append(each)

        self.combinations2 = self.combinations2[1:]

        # Calculating y for each combination
        for b, each in enumerate(self.combinations):
            for i in range(len(self.obj_list)):
                y[b] += float(float(self.obj_list[i].ref_val[each[i]]) * float(self.obj_list[i].attribute_weight))

        # Distributing consequence values in the range after calculating y for each combination
        for z, each in enumerate(self.combinations2):
            rules = Rules()
            rules.parent = self.parent.antecedent_id
            rules.antecedent = [each.name for each in self.obj_list]
            row_val = [0 for _ in range(len(self.con_ref_values))]

            is_continue = False
            for idx, per in enumerate(self.con_ref_values):
                if per == y[z]:
                    row_val[idx] = 1.0
                    rules.consequence_val = row_val
                    rules.combinations = each
                    self.rule_row_list.append(rules)
                    is_continue = True

            if is_continue:
                continue

            else:
                for idx in range(len(self.con_ref_values) - 1):
                    if (self.con_ref_values[idx] > y[z]) and (y[z] > self.con_ref_values[idx + 1]):
                        row_val[idx + 1] = float((self.con_ref_values[idx] - y[z]) / (self.con_ref_values[idx] - self.con_ref_values[idx + 1]))
                        row_val[idx] = float(1 - row_val[idx + 1])

                rules.consequence_val = [round(each, 2) for each in row_val]
                rules.combinations = each
                self.rule_row_list.append(rules)

        
        return self.rule_row_list

    '''
    Transforming input value in the range of consequent values
    '''

    def input_transformation(self):
        for each in self.obj_list:
            
            try:
                user_input = float(each.input_val)
            except:
                user_input = 0

            if user_input > float(each.ref_val[0]):
                user_input = float(each.ref_val[0])
            elif user_input < float(each.ref_val[len(each.ref_val) - 1]):
                user_input = float(each.ref_val[len(each.ref_val) - 1])

            flag = False
            for i in range(len(each.ref_val)):
                if user_input == float(each.ref_val[i]):
                    each.transformed_val[i] = 1
                    flag = True
                    break

            if not flag:
                for j in range(len(each.ref_val) - 1):
                    if (float(each.ref_val[j]) > user_input) and (user_input > float(each.ref_val[j+1])):
                        val_1 = ((float(each.ref_val[j]) - user_input) / (float(each.ref_val[j]) - float(each.ref_val[j+1])))
                        each.transformed_val[j + 1] = round(val_1, 3)
                        val_2 = 1 - val_1
                        each.transformed_val[j] = round(val_2, 3)

           

    '''
    Calculating activation weight
    '''

    def activation_weight(self):
        matching_degree = list()

        for i, row in enumerate(self.combinations):
            degree = 1.0
            naw = max([float(self.obj_list[idx].attribute_weight) for idx, val in enumerate(row)])
            for idx, val in enumerate(row):
                degree *= float(pow(float(self.obj_list[idx].transformed_val[val]), float(naw)))
            matching_degree.insert(i, degree)

        sum = 0.0
        for k in range(len(self.rule_row_list)):
            current_rule = self.rule_row_list[k]
            current_rule.matching_degree = round(matching_degree[k], 3)
            sum += float(current_rule.rule_weight) * float(current_rule.matching_degree)

        for p in range(len(self.rule_row_list)):
            current_rule = self.rule_row_list[p]
            activation_weight = float((float(current_rule.rule_weight) * float(current_rule.matching_degree)) / sum)
            current_rule.activation_weight = round(activation_weight, 3)

    '''
    Updating rule base
    '''

    def belief_update(self):
        tao = [0 for _ in range(len(self.obj_list))]
        for i in range(len(self.obj_list)):
            try:
                input_val = float(self.obj_list[i].input_val)
            except:
                input_val = 0
            if input_val != 0:
                tao[i] = 1
        total = 0

        for j in range(len(self.obj_list)):
            summation = tao[j] * sum([float(each) for each in self.obj_list[j].transformed_val])     # tao(t,k) * sum(j = 1 to Jt) (ALPHAtj)
            total += summation                          # sum(t = 1 to Tk) sum(j = 1 to Jt) (ALPHAtj)

        if sum([each for each in tao]) <= 0:
            update_value = 1
        else:
            update_value = total / float(sum([each for each in tao]))

        for each in self.rule_row_list:
            new_val_list = []
            for idx, row in enumerate(each.consequence_val):
                new_val = float(row) * update_value
                new_val_list.insert(idx, new_val)
            each.consequence_val = new_val_list
            
            
        '''    
        with open('BRB.txt', 'w') as the_file:
            for each in self.rule_row_list:
                the_file.write(str(each.__dict__))
                the_file.write('\n')
        '''
        

    '''
    Rule aggregation
    '''

    # Using Analytical ER
    def aggregate_rule(self):

        # Get all the consequent value list from rule base
        consequent_array = []
        for i in range(len(self.rule_row_list)):
            row = self.rule_row_list[i]
            consequent_array.insert(i, row.consequence_val)

        # Calculating (WkBjk) ; (k = 1 to L, j = 1 to N) and saving in a 2D array (named mn)
        mn = [[0 for _ in range(len(self.combinations))] for _ in range(len(self.con_ref_values))]
        for i in range(len(self.rule_row_list)):
            for idx, each in enumerate(self.rule_row_list[i].consequence_val):
                mn[idx][i] = float(float(self.rule_row_list[i].activation_weight) * float(each))

        # Calculating (1 - Wk * (sum(j = 1 to N)Bjk)) ; (k = 1 to L) from the consequent array and saving in a 1D array (named md)
        md = [0 for _ in range(len(self.rule_row_list))]
        for j in range(len(consequent_array)):
            total = 0
            for k in range(len(consequent_array[j])):
                total += consequent_array[j][k]     # (sum(j=1 to N)Bjk)
            md[j] = 1 - (float(self.rule_row_list[j].activation_weight) * total)

        # Calculating (sum(j=1 to N)(multiplicative(k = 1 to L)(WkBjk + 1 - Wk * (sum(j = 1 to N)Bjk)))) and saving in total_rowsum
        rowsum = [1 for _ in range(len(self.con_ref_values))]
        for x in range(len(self.con_ref_values)):
            for y in range(len(self.rule_row_list)):
                rowsum[x] *= (mn[x][y] + md[y])     # (multiplicative(k = 1 to L)(WkBjk + (1 - Wk * sum(j=1 to N, Bjk))))
        total_rowsum = sum(rowsum)

        # Calculating (multiplicative(k = 1 to L)(1 - Wk * sum(j=1 to N, Bjk))) and saving in mh
        mh = 1
        for i in range(len(self.rule_row_list)):
            mh *= md[i]

        # Calculating ((sum(j=1 to N)(multiplicative(k = 1 to L)(WkBjk + 1 - Wk * sum(j=1 to N, Bjk)))) - (N-1) * (multiplicative(k = 1 to L)(1 - Wk * sum(j=1 to N, Bjk))))
        kn = total_rowsum - ((len(self.con_ref_values) - 1) * mh)

        # Calculating (meu = 1 / (sum(j=1 to N)(multiplicative(k = 1 to L)(WkBjk + 1 - Wk * sum(j=1 to N, Bjk)))) - (N-1) * (multiplicative(k = 1 to L)(1 - Wk * sum(j=1 to N, Bjk))))
        kn1 = 1 / kn

        # Calculating (meu * (multiplicative(k = 1 to L)(WkBjk + 1 - Wk * sum(j=1 to N)Bjk))) - (multiplicative(k = 1 to L)(1 - Wk * sum(j=1 to N, Bjk)))) and saving in a 1D array (named m)
        m = [0 for _ in range(len(self.con_ref_values))]
        for j in range(len(self.con_ref_values)):
            m[j] = kn1 * (rowsum[j] - mh)

        # Calculating (1 - Wk) ; (k = 1 to L) and saving in a 1D array (named ab)
        ab = [0 for _ in range(len(self.rule_row_list))]
        for i in range(len(self.rule_row_list)):
            ab[i] = 1 - (float(self.rule_row_list[i].activation_weight))

        # Calculating (multiplicative(k = 1 to L)(1 - Wk)) and saving in cd
        cd = 1
        for i in range(len(self.rule_row_list)):
            cd *= ab[i]

        # Calculating (meu * (multiplicative(k = 1 to L)(1 - Wk))) and saving in mhn
        mhn = kn1 * cd

        # Calculating Bj = (meu * (multiplicative(k = 1 to L)(WkBjk + 1 - Wk * sum(j=1 to N)Bjk))) - (multiplicative(k = 1 to L)(1 - Wk * sum(j=1 to N, Bjk)))) / (1 - (meu * (multiplicative(k = 1 to L)(1 - Wk))))
        aggregated_consequence_val = [0 for k in range(len(self.con_ref_values))]
        for k in range(len(self.con_ref_values)):
            aggregated_consequence_val[k] = m[k] / (1 - mhn)

        output = [each for each in aggregated_consequence_val]
        return output
