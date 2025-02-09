import subprocess

def execute_command(command):
    """Execute a shell command and return its output."""
    try:
        result = subprocess.check_output(command, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error executing command: {e}"
    return result

def main():
    output_file = "all_commands_output.txt"

    with open(output_file, 'w') as f:
        for X in range(1, 6):
            for Y in range(1, 6):
                # Generate and execute the first command
                command1 = (
                    rf"python compare.py project-{X}/human-diagram.puml "
                    rf"project-{X}/t{Y}-no-haf.puml -f t{Y}-no-haf -d project-{X}/stats-no-haf"
                )
                f.write(f"Executing command: {command1}\n")
                result1 = execute_command(command1)
                f.write(result1)
                f.write("\n\n")

                # Generate and execute the second command
                command2 = (
                    rf"python compare.py project-{X}/human-diagram.puml "
                    rf"project-{X}/t{Y}-haf.puml -f t{Y}-haf -d project-{X}/stats-haf"
                )
                f.write(f"Executing command: {command2}\n")
                result2 = execute_command(command2)
                f.write(result2)
                f.write("\n\n")

if __name__ == "__main__":
    main()

