import asyncio

satSolverPaths = [
    "./glucose",
    "./glucose_static",
    "glucose",
    "./glucose-syrup",
    "./glucose-syrup_static",
    "glucose-syrup",
]

async def solveSAT(inputCNF):
    for satSolver in satSolverPaths:
        try:
            process = await asyncio.create_subprocess_exec(
                satSolver,
                "-model",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # print("Using", *satSolver)
            break
        except OSError:
            pass

    stdout, stderr = await process.communicate(inputCNF.encode())
    return stdout

async def solveSATparallel(inputCNFlist):
    processes = []

    for inputCNF in inputCNFlist:
        processes.append(asyncio.create_task(solveSAT(inputCNF)))

    outputs = []
    for process in processes:
        stdout = await(process)
        outputs.append(stdout)
    return outputs
