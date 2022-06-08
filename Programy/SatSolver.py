from subprocess import run, Popen, PIPE

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

def solveSATparallel(inputCNFlist):
    processes = []

    for inputCNF in inputCNFlist:
        for satSolver in satSolverPaths:
            try:
                process = Popen(satSolver, stdin=PIPE, stdout=PIPE)
                # print("Using", *satSolver)
                break
            except OSError:
                pass
        process.stdin.write(inputCNF.encode())
        processes.append(process)

    outputs = []
    for process in processes:
        stdout, stderr = process.communicate()
        outputs.append(stdout)
    return outputs
