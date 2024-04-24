selected_choices = ""


def get_input(prompt, valid_options):
    """
    Prompt the user for input, and ensure it's one of the valid options.
    """
    while True:
        user_input = input(prompt).lower().strip()
        if user_input in valid_options:
            return user_input
        else:
            print(
                f"Invalid input. Please choose one of the following: {', '.join(valid_options)}")


def compare_and_record(options, choices):

    test = ""


def main():
    options_yes_no = ["yes", "no"]
    options_all_some_none = ["all", "some", "none"]

    # Collect user responses
    getters = get_input("Include getters (all/some/none): ",
                        options_all_some_none)
    setters = get_input("Include setters (all/some/none): ",
                        options_all_some_none)
    methods = get_input("Include methods (all/some/none): ",
                        options_all_some_none)
    constructors = get_input(
        "Include constructors (all/some/none): ", options_all_some_none)
    attributes = get_input(
        "Include attributes (all/some/none): ", options_all_some_none)
    attribute_types = get_input(
        "Include attribute types (all/none): ", ["all", "none"])
    return_types = get_input(
        "Include return types (all/none): ", ["all", "none"])
    access_modifiers = get_input(
        "Include access modifiers (all/some/none): ", options_all_some_none)
    parameter_names = get_input(
        "Include parameter names (yes/no): ", options_yes_no)
    parameter_types = get_input(
        "Include parameter types (yes/no): ", options_yes_no)
    convert_aggregation = get_input(
        "Convert aggregation relationships into association relationships with multiplicities (yes/no): ",
        options_yes_no)
    convert_composition = get_input(
        "Convert composition relationships into association relationships with multiplicities (yes/no): ",
        options_yes_no)

    # Output the results
    print("\nUser Configuration:")
    print(f"Getters: {getters}")
    print(f"Setters: {setters}")
    print(f"Methods: {methods}")
    print(f"Constructors: {constructors}")
    print(f"Attributes: {attributes}")
    print(f"Attribute Types: {attribute_types}")
    print(f"Return Types: {return_types}")
    print(f"Access Modifiers: {access_modifiers}")
    print(f"Parameter Names: {parameter_names}")
    print(f"Parameter Types: {parameter_types}")
    print(f"Convert Aggregation Relationships: {convert_aggregation}")
    print(f"Convert Composition Relationships: {convert_composition}")

    getter_choices = ["All getter methods must be included in the diagram",
                      "You are allowed to omit some but not all getter methods from the diagram",
                      "All getter methods must be excluded from the diagram"]

    setter_choices = ["All setter methods must be included in the diagram",
                      "You are allowed to omit some but not all setter methods from the diagram",
                      "All setter methods must be excluded from the diagram"]

    method_choices = ["All methods must be included in the diagram",
                      "You are allowed to omit some but not all methods from the diagram",
                      "All methods must be excluded from the diagram"]

    constructor_choices = ["All constructors must be included in the diagram",
                           "You are allowed to omit some but not all constructors from the diagram",
                           "All constructors must be excluded from the diagram"]

    attribute_choices = ["All attributes must be included in the diagram",
                         "You are allowed to omit some but not all attributes from the diagram",
                         "All attributes must be excluded from the diagram"]

    attribute_type_choices = ["All attribute types must be included in the diagram",
                              "All attribute types must be excluded from the diagram"]

    return_type_choices = ["All return types of methods must be included in the diagram",
                           "All return types of methods must be excluded from the diagram"]

    access_choices = ["All access modifiers methods must be included in the diagram",
                      "You are allowed to omit some but not all access modifiers from the diagram",
                      "All access modifiers methods must be excluded from the diagram"]

    parameter_choices = ["All method parameters must be included in the diagram",
                         "All method parameters must be excluded from the diagram"]

    aggregation_choices = [
        "You should represent aggregation relationships into association relationships with multiplicities.",
        ""]
    composition_choices = [
        "You should represent composition relationships into association relationships with multiplicities.",
        ""]
    """
    NEW ADDITION
    """
    parameter_type_choices = ["All method parameter types must be included in the diagram",
                              "All method parameter types must be excluded from the diagram"]

    relationship_choices = ["All relationships must be included in the diagram",
                            "You are allowed to omit some but not all relationships from the diagram"]


if __name__ == "__main__":
    main()
