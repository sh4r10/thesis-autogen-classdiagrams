prompt_commands = []


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


def compare_and_record_multi(selected, choices):
    if selected == "all":
        prompt_commands.append(choices[0])
    elif selected == "some":
        prompt_commands.append(choices[1])
    elif selected == "none":
        prompt_commands.append(choices[2])


def compare_and_record_binary(selected, choices):
    if selected == "yes":
        prompt_commands.append(choices[0])
    elif selected == "no":
        prompt_commands.append(choices[1])


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
    relationships = get_input(
        "Include relationships (all/some): ", ["all", "some"])
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

    attribute_type_choices = ["All attribute types must be included in the diagram", "",
                              "All attribute types must be excluded from the diagram"]

    return_type_choices = ["All return types of methods must be included in the diagram", "",
                           "All return types of methods must be excluded from the diagram"]

    access_choices = ["All access modifiers must be included in the diagram",
                      "You are allowed to omit some but not all access modifiers from the diagram",
                      "All access modifiers must be excluded from the diagram"]

    parameter_choices = ["All method parameters must be included in the diagram",
                         "All method parameters must be excluded from the diagram"]

    aggregation_choices = [
        "You should represent aggregation relationships into association relationships with multiplicities.",
        ""]
    composition_choices = [
        "You should represent composition relationships into association relationships with multiplicities.",
        ""]

    parameter_type_choices = ["All method parameter types must be included in the diagram",
                              "All method parameter types must be excluded from the diagram"]

    relationship_choices = ["All relationships must be included in the diagram",
                            "You are allowed to omit some but not all relationships from the diagram", ""]

    prompt_commands.append(
        "Ask the user if they would like to provide further files, if not proceed, if they do, wait for them to provide further files and repeat step 1.")
    prompt_commands.append(
        "List all the classes provided by the user, along with a one sentence description.")
    prompt_commands.append(
        "Ask the user if they would like to provide further files, if not proceed, if they do, wait for them to provide further files and repeat step 1.")

    compare_and_record_multi(getters, getter_choices)
    compare_and_record_multi(setters, setter_choices)
    compare_and_record_multi(methods, method_choices)
    compare_and_record_multi(constructors, constructor_choices)
    compare_and_record_multi(attributes, attribute_choices)
    compare_and_record_multi(attribute_types, attribute_type_choices)
    compare_and_record_multi(return_types, return_type_choices)
    compare_and_record_multi(access_modifiers, access_choices)
    compare_and_record_multi(relationships, relationship_choices)

    compare_and_record_binary(parameter_names, parameter_choices)
    compare_and_record_binary(parameter_types, parameter_type_choices)
    compare_and_record_binary(convert_aggregation, aggregation_choices)
    compare_and_record_binary(convert_composition, composition_choices)

    prompt_commands.append(
        "Empty classes, i.e classes that would have no body in the diagram should not be included in the diagram.")
    prompt_commands.append(
        "Create a class diagram which reflects the above instructions, in PlantUML syntax")
    prompt_commands.append(
        "Ensure that the correct PlantUML syntax specifications are followed an no artifacts are included in the resulting diagram.")
    prompt_commands.append(
        "Go back to step 4 and ensure that all instructions were followed properly, if any mistakes are found fix the mistakes and go back to step 4 to restart the final checking process.")
    prompt_commands.append(
        "Say 'Ad Astra Aspera' and finish")
    prompt_commands.append(
        "Create a class diagram which reflects the above instructions, in PlantUML syntax")

    with open("prompt.txt", "w") as file:
        file.write("""You should perform the following actions in this order to create a PlantUML class diagram from code, once a user has 
submitted a prompt. It is extremely important that you follows this exact 
sequence of actions in order to develop a coherent chain of thought.\n""")

        for index, command in enumerate(prompt_commands):
            if (command != ""):
                file.write(f"{index+1}. {command}\n")


if __name__ == "__main__":
    main()
