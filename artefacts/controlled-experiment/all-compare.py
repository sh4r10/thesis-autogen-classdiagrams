import os

output_file = "all_commands_output.txt"
with open(output_file, 'w') as f:
    for X in range(1, 6):
        for Y in range(1, 6):
            command = f"python compare.py project-{X}/human-diagram.puml project-{X}/t{Y}-no-haf.puml -f t{Y}-no-haf -d project-{X}/stats-no-haf"
            f.write(f"Executing command: {command}\n")
            result = os.popen(command).read()
            f.write(result)
            f.write("\n\n")
            command = f"python compare.py project-{X}/human-diagram.puml project-{X}/t{Y}-haf.puml -f t{Y}-haf -d project-{X}/stats-haf"
            f.write(f"Executing command: {command}\n")
            result = os.popen(command).read()
            f.write(result)
            f.write("\n\n")
