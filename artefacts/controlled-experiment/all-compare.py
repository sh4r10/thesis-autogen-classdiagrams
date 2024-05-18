import os

for X in range(1, 6):
    for Y in range(1, 6):
        command = f"python compare.py project-{X}/human-diagram.puml project-{X}/t{Y}-no-haf.puml -f t{Y}-no-haf -d project-{X}/stats-no-haf"
        os.system(command)
        command = f"python compare.py project-{X}/human-diagram.puml project-{X}/t{Y}-haf.puml -f t{Y}-haf -d project-{X}/stats-haf"
        os.system(command)
