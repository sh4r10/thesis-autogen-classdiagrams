import sys
from rich import print
import re


def parse_plantuml(filename):
    """Parse a PlantUML file and extract classes, attributes, and methods."""
    class_dict = {}
    current_class = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('class'):
                # Extract the class name
                parts = line.split()  # class ClassName {
                class_name = parts[1]
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
                    y = re.search(r"\w+(?=\()", line)
                    z = re.search(r'(?<=\):)\w+', line)
                    visibility = "!" if x is None else x.group()
                    name = "noname" if y is None else y.group()
                    methodType = "none" if z is None else z.group()
                    # params
                    parameters = []
                    a = re.search(r"(?<=\().*(?=\))", line)

                    if a.group() != "":
                        paramsString = a.group()
                        pattern = r"(?:(\w+):)?(\w+)"
                        matches = re.findall(pattern, paramsString)
                        for match in matches:
                            param_dict = {'name': match[0]}
                            if match[1]:  # Only add type if it exists
                                param_dict['type'] = match[1]
                            parameters.append(param_dict)

                    method = {"visibility": visibility,
                              "name": name, "methodType": methodType, "parameters": parameters}
                    class_dict[current_class]['methods'].append(method)
                else:
                    x = re.search(r"^[-+]", line)
                    y = re.search(r"\w+", line)
                    z = re.search(r'(?<=:)\w+', line)
                    visibility = "!" if x is None else x.group()
                    name = "noname" if y is None else y.group()
                    attrType = "none" if z is None else z.group()
                    attr = [visibility, name, attrType]
                    class_dict[current_class]['attributes'].append(attr)
    return class_dict


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
                f"  Parameter '{name}' of type '{type2}' is missing in Human diagram.")
        elif name not in params_dict2:
            detailed_diff.append(
                f"  Parameter '{name}' of type '{type1}' is missing in GPT diagram.")
        elif type1 != type2:
            detailed_diff.append(
                f"  Parameter '{name}' has different types (Human: '{type1}', GPT: '{type2}').")

    # Return the collected differences as a string if there are any
    return "\n".join(detailed_diff) if detailed_diff else None


def compare_methods(methods1, methods2, cls, missing):
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
                f"Method '{name}' in class '{cls}' exists only in GPT diagram.")
            continue
        if not m2:
            missing.append(
                f"Method '{name}' in class '{cls}' exists only in Human diagram.")
            continue

        if name not in method_dict1:
            visibility2, methodType2 = method_dict2[name]
            missing.append(
                f"Method '{name}' of type '{methodType2}' in class '{cls}' missing in Human diagram.")
        elif name not in method_dict2:
            visibility1, methodType1 = method_dict1[name]
            missing.append(
                f"Method '{name}' of type '{methodType1}' in class '{cls}' missing in GPT diagram.")
        else:
            m1 = method_dict1[name]
            m2 = method_dict2[name]
            differences = []
            if m1['visibility'] != m2['visibility']:
                differences.append(
                    f"  Visibility (Human: {m1['visibility']}, GPT: {m1['visibility']})")
            if m1['methodType'] != m2['methodType']:
                differences.append(
                    f"  Return Type (Human: {m1['methodType']}, GPT: {m2['methodType']})")

            param_diff = compare_parameters(m1["parameters"], m2["parameters"])
            if param_diff:
                differences.append(param_diff)
            if differences:
                missing.append(f"Method '{name}' in class '{cls}' has different \n" +
                               "\n".join(differences))
            else:
                print(f"  Method '{name}' is identical in both files.")


def compare_attributes(attrs1, attrs2, cls, missing):
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
                f"Attribute '{name}' of type '{type2}' in class '{cls}' missing in Human diagram.")
        elif name not in attr_dict2:
            visibility1, type1 = attr_dict1[name]
            missing.append(
                f"Attribute '{name}' of type '{type1}' in class '{cls}' missing in GPT diagram.")
        else:
            visibility1, type1 = attr_dict1[name]
            visibility2, type2 = attr_dict2[name]
            differences = []
            if visibility1 != visibility2:
                differences.append(
                    f"  Visibility (Human: '{visibility1}', GPT: '{visibility2}')")
            if type1 != type2:
                differences.append(
                    f"  Type (Human: '{type1}', GPT: '{type2}')")
            if differences:
                missing.append(f"Attribute '{name}' in class '{cls}' has different \n" +
                               "\n".join(differences))
            else:
                print(f"  Attribute '{name}' is identical in both files.")


def compare_classes(classes1, classes2):
    """Compare two dictionaries of class definitions."""
    all_classes = set(classes1.keys()).union(set(classes2.keys()))
    missing = []
    stats = {"classes": {"correct": 0, "total": 0}}
    print("\n# SIMILARITIES")
    for cls in all_classes:
        if cls in classes1 and cls in classes2:
            # Stats
            stats["classes"]['correct'] += 1
            stats["classes"]['total'] += 1

            print(f"Class '{cls}' is in both files.")
            # compare attributes
            compare_attributes(
                classes1[cls]['attributes'], classes2[cls]['attributes'], cls, missing)
            compare_methods(classes1[cls]['methods'],
                            classes2[cls]['methods'], cls, missing)

        else:
            if cls in classes1:
                missing.append(f"Class '{cls}' is only in Human diagram.")
                stats["classes"]['total'] += 1
            else:
                missing.append(f"Class '{cls}' is only in GPT diagram.")
    print("\n# DIFFERENCES")
    print("\n".join(missing))

    print("\n# STATISTICS")
    print(stats)


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: {:s} <human> <ai>".format(sys.argv[0]))
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]
    classes_file1 = parse_plantuml(file1)
    classes_file2 = parse_plantuml(file2)
    compare_classes(classes_file1, classes_file2)
