import os, pickle, argparse
from rich import print
from rich.pretty import pprint
import re

stats = {
    "classes": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "relationships": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "attributes": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "methods": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "access_modifiers": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "attribute_type": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "method_return_type": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "parameter_name": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    },
    "parameter_type": {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    }

}


def parse_relationship(line):
    matches = re.search(
        r'^(\w+)\s*("([-A-Za-z0-9\.\*\\\+\s]+)")?\s*(<|<\||o|\*)?((-|\.)*\w*(-|\.)*)(>|\|>|o|\*)?\s*("([-A-Za-z0-9\.\*\\\+\s]+)")?\s*(\w+)\s*(:\s*"?([-A-Za-z0-9\.\*\\\+\s]+)"?)?$', line)
    rel_dict = {}
    if matches:
        rel_dict["from"] = matches[1] if matches[1] is not None else "<none>"
        rel_dict["to"] = matches[11] if matches[11] is not None else "<none>"
        rel_dict["label"] = matches[13] if matches[13] is not None else "<none>"
        rel_dict["text_from"] = matches[3] if matches[3] is not None else "<none>"
        rel_dict["text_to"] = matches[10] if matches[10] is not None else "<none>"
        rel_dict["rel_line"] = matches[5] if matches[5] is not None else "<none>"
        rel_dict["rel_type_from"] = matches[4] if matches[4] is not None else "<none>"
        rel_dict["rel_type_to"] = matches[8] if matches[8] is not None else "<none>"
    return rel_dict


def parse_plantuml(filename):
    """Parse a PlantUML file and extract classes, attributes, and methods."""
    class_dict = {}
    relationships = []
    current_class = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            rel_regex = re.search(r"(-(.)*-)|(\.(.)*\.)", line)
            if rel_regex is not None:
                rel_dict = parse_relationship(line)
                relationships.append(rel_dict)
            elif line.startswith('@') or line.startswith("'"):
                continue
            elif line.startswith('class'):
                # Extract the class name
                line = line.replace(" ", "")
                x = re.search(r"(?<=(class))([A-Za-z0-9]+)", line)
                class_name = x.group(); 
                current_class = class_name
                class_dict[current_class] = {'attributes': [], 'methods': []}
            elif line.endswith('}') and current_class:
                # End of current class definition
                current_class = None
            elif current_class:
                line = line.replace(" ", "")
                # Inside a class, check for attributes or methods
                if '(' in line and ')' in line:  # Assume methods have parentheses
                    x = re.search(r"^[-+]", line)
                    y = re.search(r"[A-Za-z0-9]+(?=\()", line)
                    z = re.search(r'(?<=\):)[A-Za-z0-9<>,]+', line)
                    visibility = "<none>" if x is None else x.group()
                    name = "<nameless>" if y is None else y.group()
                    methodType = "<none>" if z is None else z.group()
                    # params
                    parameters = []
                    a = re.search(r"(?<=\().*(?=\))", line)

                    if a.group() != "":
                        paramsString = a.group()
                        pattern = r"(?:(\w+):)?(\w+)"
                        matches = re.findall(pattern, paramsString)
                        for match in matches:
                            param_dict = {
                                'name': match[0] if match[0] != '' else '<nameless>'}
                            if match[1]:  # Only add type if it exists
                                param_dict['type'] = match[1] if match[1] != '' else '<none>'
                            parameters.append(param_dict)

                    method = {"visibility": visibility,
                              "name": name, "methodType": methodType, "parameters": parameters}
                    class_dict[current_class]['methods'].append(method)
                elif line != "":
                    x = re.search(r"^[-+]", line)
                    y = re.search(r"[A-Za-z0-9\_]+", line)
                    z = re.search(r'(?<=:)[A-Za-z0-9<>,]+', line)
                    visibility = "<none>" if x is None else x.group()
                    name = "<none>" if y is None else y.group()
                    attrType = "<none>" if z is None else z.group()
                    attr = [visibility, name, attrType]
                    class_dict[current_class]['attributes'].append(attr)
    # print(class_dict)
    # print(relationships)
    return (class_dict, relationships)


def compare_parameters(params1, params2):
    """Compare method parameters in detail, focusing on name and type."""
    # Create dictionaries indexed by parameter name for easy lookup
    params_dict1 = {param['name']: param['type']
                    for param in params1 if param['name']}
    params_dict2 = {param['name']: param['type']
                    for param in params2 if param['name']}

    # Combine all parameter names for comparison
    all_param_names = set(params_dict1.keys()).union(params_dict2.keys())
    detailed_diff = []

    for name in all_param_names:
        type1 = params_dict1.get(name)
        type2 = params_dict2.get(name)
        if name not in params_dict1:
            detailed_diff.append(
                f"    Parameter '{name}' of type '{type2}' is only in GPT diagram.")
            stats["parameter_name"]["fp"] += 1
        elif name not in params_dict2:
            detailed_diff.append(
                f"    Parameter '{name}' of type '{type1}' is only in Human diagram.")
            stats["parameter_name"]["fn"] += 1
        else:
            stats["parameter_name"]["tp"] += 1

        if type1 != type2:
            detailed_diff.append(
                f"    Parameter '{name}' has different types (Human: '{type1}', GPT: '{type2}').")
            if type1 == "<none>":
                stats["parameter_type"]["fp"] += 1
            elif type2 == "<none>":
                stats["parameter_type"]["fn"] += 1
            else:
                stats["parameter_type"]["fn"] += 1
                stats["parameter_type"]["fp"] += 1
        else:
            stats["parameter_type"]["tp"] += 1

    # Return the collected differences as a string if there are any
    return "\n  ".join(detailed_diff) if detailed_diff else None


def compare_methods(methods1, methods2, missing):
    """Compare methods based on visibility, name, and type, providing detailed differences."""
    # Convert list of method dictionaries to key by name for easier comparison
    method_dict1 = {method['name']: method for method in methods1}
    method_dict2 = {method['name']: method for method in methods2}
    # Collect all method names
    all_method_names = set(method_dict1.keys()).union(method_dict2.keys())
    for name in all_method_names:
        m1 = method_dict1.get(name)
        m2 = method_dict2.get(name)
        if not m1:
            missing.append(
                f"  Method '{name}' exists only in GPT diagram.")
            stats["methods"]["fp"] += 1
            continue
        if not m2:
            missing.append(
                f"  Method '{name}' exists only in Human diagram.")
            stats["methods"]["fn"] += 1
            continue
        # Add a tp
        stats["methods"]["tp"] += 1

        m1 = method_dict1[name]
        m2 = method_dict2[name]
        differences = []

        if m1['visibility'] != m2['visibility']:
            differences.append(
                f"    Visibility (Human: '{m1['visibility']}', GPT: '{m2['visibility']}')")
            if m1['visibility'] == "<none>":
                stats["access_modifiers"]["fp"] += 1
            elif m2['visibility'] == "<none>":
                stats["access_modifiers"]["fn"] += 1
        else:
            stats["access_modifiers"]["tp"] += 1

        if m1['methodType'] != m2['methodType']:
            differences.append(
                f"    Return Type (Human: '{m1['methodType']}', GPT: '{m2['methodType']}')")
            if m1['methodType'] == "<none>":
                stats["method_return_type"]["fp"] += 1
            elif m2['methodType'] == "<none>":
                stats["method_return_type"]["fn"] += 1
        else:
            stats["method_return_type"]["tp"] += 1

        param_diff = compare_parameters(m1["parameters"], m2["parameters"])
        if param_diff:
            differences.append(param_diff)
        if differences:
            missing.append(f"  Method '{name}' has different \n" +
                           "\n".join(differences))
        else:
            print(f"  Method '{name}' is identical in both files.")


def compare_attributes(attrs1, attrs2, missing):
    """Compare attributes based on visibility, name, and type, providing detailed differences."""
    # Group attributes by name
    # name as key, (visibility, type) as value
    attr_dict1 = {attr[1]: (attr[0], attr[2]) for attr in attrs1}
    attr_dict2 = {attr[1]: (attr[0], attr[2]) for attr in attrs2}

    # Check for all attribute names
    all_attr_names = set(attr_dict1.keys()).union(set(attr_dict2.keys()))
    for name in all_attr_names:
        if name not in attr_dict1:
            visibility2, type2 = attr_dict2[name]
            missing.append(
                f"  Attribute '{name}' of type '{type2}' missing in Human diagram.")
            stats["attributes"]["fp"] += 1
        elif name not in attr_dict2:
            visibility1, type1 = attr_dict1[name]
            missing.append(
                f"  Attribute '{name}' of type '{type1}' missing in GPT diagram.")
            stats["attributes"]["fn"] += 1
        else:
            stats["attributes"]["tp"] += 1
            visibility1, type1 = attr_dict1[name]
            visibility2, type2 = attr_dict2[name]
            differences = []
            if visibility1 != visibility2:
                differences.append(
                    f"    Visibility (Human: '{visibility1}', GPT: '{visibility2}')")
                if visibility1 == "<none>":
                    stats["access_modifiers"]["fp"] += 1
                elif visibility2 == "<none>":
                    stats["access_modifiers"]["fn"] += 1
            else:
                stats["access_modifiers"]["tp"] += 1

            if type1 != type2:
                differences.append(
                    f"    Type (Human: '{type1}', GPT: '{type2}')")
                if type1 == "<none>":
                    stats["attribute_type"]["fp"] += 1
                elif type2 == "<none>":
                    stats["attribute_type"]["fn"] += 1
            else:
                stats["attribute_type"]["tp"] += 1

            if differences:
                missing.append(f"  Attribute '{name}' has different: \n" +
                               "\n".join(differences))
            else:
                print(f"  Attribute '{name}' is identical in both files.")


def compare_classes(classes1, classes2):
    """Compare two dictionaries of class definitions."""
    all_classes = set(classes1.keys()).union(set(classes2.keys()))
    missing = {}
    print("\n# CLASS SIMILARITIES")
    for cls in all_classes:
        missing[cls] = [] if cls not in missing else missing[cls]
        if cls in classes1 and cls in classes2:
            print(f"Class '{cls}' is in both files.")
            # compare attributes
            compare_attributes(
                classes1[cls]['attributes'], classes2[cls]['attributes'], missing[cls])
            compare_methods(classes1[cls]['methods'],
                            classes2[cls]['methods'], missing[cls])
            stats["classes"]["tp"] += 1
        else:
            if cls in classes1:
                missing[cls].append(f"Class '{cls}' is only in Human diagram.")
                stats["classes"]["fn"] += 1
            else:
                missing[cls].append(f"Class '{cls}' is only in GPT diagram.")
                stats["classes"]["fp"] += 1
    print("\n# CLASS DIFFERENCES")

    missing = dict(sorted(missing.items(), reverse=True, key=lambda s: (
        'only' not in s[0], len(s[0]) if 'only' not in s[0] else 0, s[0])))
    for key in missing:
        if len(missing[key]) == 0:
            continue
        if len(missing[key]) == 1 and "is only in" in missing[key][0]:
            print(missing[key][0])
            continue

        print(f"Class '{key}' has the following differences:")
        for difference in missing[key]:
            print(difference)


def compare_relationships(rels1, rels2):
    """Compare two lists of relationship dictionaries and print differences."""
    # Assuming relationships can be identified by a unique combination of 'from' and 'to'
    print("\n# RELATIONSHIP SIMILARITIES")
    errors = []

    def relationship_key(rel):
        return tuple(sorted([rel.get("from", "<none>"), rel.get("to", "<none>")]))

    # Convert lists to dictionaries using a unique key
    dict1 = {relationship_key(rel): rel for rel in rels1}
    dict2 = {relationship_key(rel): rel for rel in rels2}

    # Gather all unique relationship keys
    all_rel_keys = set(dict1.keys()).union(dict2.keys())

    reversible_rels = {
            ">": "<",
            "|>": "<|",
            "<": ">",
            "<|": "|>",
            "o": "o",
            "*": "*",
            "<none>": "<notnone>"
        }
        
    def is_reversible(rel1, rel2):
        if rel1 == None or rel2 == None:
            return False

        rel_head_from_1 = rel1.get("rel_type_from", "");
        rel_head_from_2 = rel2.get("rel_type_from", "");
        rel_head_to_1 = rel1.get("rel_type_to", "");
        rel_head_to_2 = rel2.get("rel_type_to", "");
        
        if (rel_head_from_1 == "" and rel_head_to_2 == ""):
            return True
        if (rel_head_from_1 != "<none>" or rel_head_to_2 != "<none>") and rel_head_from_1 == reversible_rels[rel_head_to_2]:
            return True
        elif (rel_head_to_1 != "<none>" or rel_head_from_2 != "<none>") and rel_head_to_1 == reversible_rels[rel_head_from_2]:
            return True
        else:
            return False


    for key in all_rel_keys:
        rel1 = dict1.get(key)
        rel2 = dict2.get(key)
        reversible = is_reversible(rel1, rel2);
        if not rel1:
            errors.append(
                f"Relationship from '{key[0]}' to '{key[1]}' exists only in the GPT diagram")
            stats["relationships"]["fp"] += 1
            continue
        if not rel2:
            errors.append(
                f"Relationship from '{key[0]}' to '{key[1]}' exists only in the Human diagram")
            stats["relationships"]["fn"] += 1
            continue
        
        if rel1 and rel2 and reversible:
            stats["relationships"]["tp"] += 1

        # Compare each attribute within the relationship dictionaries


        differences = []
        for attr in ["text_from", "text_to", "rel_type_from", "rel_type_to"]:
            value1 = rel1.get(attr, "<none>")
            value2 = rel2.get(attr, "<none>")

            differences.append(
                    f"  {attr}: (Human: '{value1}', GPT: '{value2}')")

        if differences:
            errors.append(
                f"Relationship from '{key[0]}' to '{key[1]}' has differences: \n" + "\n".join(differences) + ".")
        else:
            print(
                f"Relationship from '{key[0]}' to '{key[1]}' is identical in both lists.")
    if len(errors) > 0:
        print("\n# RELATIONSHIP DIFFERENCES")
    for err in errors:
        print(err)

def print_stats():
    for c in stats:
        category = stats[c]
        precision = category["tp"]/((category["tp"]+category["fp"]) if (category["tp"]+category["fp"]) != 0 else 1)
        recall = category["tp"]/((category["tp"]+category["fn"]) if (category["tp"]+category["fn"]) != 0 else 1)
        f1 = 2*(precision*recall)/((precision+recall) if (precision+recall) != 0 else 1) 
        category["precision"] = precision
        category["recall"] = recall
        category["f1"] = f1

    print("\n# STATISTICS")
    pprint(stats, expand_all=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("compare.py");
    parser.add_argument('human_diagram')
    parser.add_argument('gpt_diagram')
    parser.add_argument('-d', '--dir', action='store')
    
    args = parser.parse_args()
    file1, file2 = args.human_diagram, args.gpt_diagram
    (classes_file1, rels_file1) = parse_plantuml(file1)
    (classes_file2, rels_file2) = parse_plantuml(file2)
    compare_classes(classes_file1, classes_file2)
    compare_relationships(rels_file1, rels_file2)
    print_stats();
    
    if(args.dir):
        if args.dir and not os.path.exists(args.dir):
            os.makedirs(args.dir)

        dir = args.dir if args.dir else "."
        filename = re.search(r"[-\w]+(?=.puml)", args.gpt_diagram)
        with open(dir+'/'+filename.group()+'.stat', 'wb') as file:
            pickle.dump(stats, file)
