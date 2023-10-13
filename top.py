import subprocess
import argparse

aparser = argparse.ArgumentParser(description="Process test case scenarios")
aparser.add_argument("test_type", nargs=1)
args = aparser.parse_args()

test_type = args.test_type[0]

print("Waiting for test case to execute:")
cmd = 'python3 ' + test_type 
process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

stdout_output = process.stdout.decode('utf-8')
stderr_output = process.stderr.decode('utf-8')

# Print the standard output and standard error
if stdout_output:
    print("Standard Output:")
    print(stdout_output)

if stderr_output:
    print("Standard Error:")
    print(stderr_output)