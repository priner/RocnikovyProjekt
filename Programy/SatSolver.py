from subprocess import run

satSolverPaths = [
    ["./glucose", "-model"],
    ["./glucose_static", "-model"],
    ["glucose", "-model"],
    ["./glucose-syrup", "-model"],
    ["./glucose-syrup_static", "-model"],
    ["glucose-syrup", "-model"],
]

def solveSAT(inputCNF):
    for satSolver in satSolverPaths:
        try:
            process = run(satSolver, input=inputCNF.encode(), capture_output=True)
            # print("Using", *satSolver)
            break
        except OSError:
            pass
    return process.stdout
