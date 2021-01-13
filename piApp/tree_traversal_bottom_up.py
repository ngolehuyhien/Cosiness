import json

from manipulate_data import RuleBase
from data import Data


def brb_algorithm(structured_data):
    with open('brb_tree.json') as file_data:
        data = json.load(file_data)

    structured_result = list()
    result_nodes = ['x7', 'x8', 'x9', 'x10']
    obj_list = list()

    # Saving each node data as an object in a list
    for each in data:
        obj = Data(**data[each])
        obj.name = str(each)
        for each in structured_data:
            if each[0] == obj.name:
                obj.input_val = each[2]
        obj_list.append(obj)

    # Sorting the obj_list based on is_input is true
    obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
    node_list = [each for each in obj_list if each.antecedent_id != each.parent]


    visited = list()
    i = 0
    count = 1
    subtree = 1

    # While we have an object in node_list
    while len(node_list):

        # Get parent of the current node.
        parent = None
        for each in obj_list:
            if each.name == node_list[i].parent:
                parent = each
                break

        visiting = list()
        visiting.append(node_list[i])  # Adding the current node in the list
        
        # Finding if there is any other node which has the same parent
        for j in range(i + 1, len(node_list)):
            if node_list[i].parent == node_list[j].parent:
                visiting.append(node_list[j])

        # Checking if all the siblings has is_input true or not.
        is_all_input = True
        for each in visiting:
            if each.is_input != 'true':
                is_all_input = False

        
        if is_all_input:
            # Computing the BRB sub-tree for the nodes in visiting.

            rule_base = RuleBase(visiting, parent)
            initial_rule_base = rule_base.create_rule_base()
            transformed_input = rule_base.input_transformation()
            activation_weight = rule_base.activation_weight()
            belief_update = rule_base.belief_update()
            consequence_val = rule_base.aggregate_rule()

            crisp_val = 0.0
            for i in range(len(parent.ref_val)):
                crisp_val += float(parent.ref_val[i]) * float(consequence_val[i])

            parent.input_val = crisp_val

            for each in range(len(consequence_val)):
                consequence_val[each] = round(consequence_val[each], 3)

            if parent.antecedent_id in result_nodes:
                structured_result.append([parent.antecedent_id, consequence_val, str(round(crisp_val, 3))])

                
            # Removing the visited nodes from node_list
            for each in visiting:
                visited.append(each)
            node_list = [each for each in node_list if each not in visited]

            if len(node_list) == 0:               
                #print("All the current nodes have same parent \"{}\" so the tree traversal is done and the ultimate output is: {}".format(parent.antecedent_id, parent.antecedent_id))
                break

            else:
                
                # Make the current nodes is_input true
                current = list()
                for each in node_list:
                    if each == parent:
                        current = each
                        current.is_input = 'true'
                        i = 0

                # Sorting the node_list based on is_input is true
                node_list.sort(key=lambda x: x.is_input == "true", reverse=True)
                
                count += 1
                subtree += 1

        # if not all the siblings has same parent, continue to the next node of node_list
        else:
            i += 1
            
            count += 1
            node_list.sort(key=lambda x: x.is_input == "true", reverse=True)
            continue

    return structured_result
