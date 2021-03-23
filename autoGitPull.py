from subprocess import Popen, PIPE

process = Popen(["git", "pull"], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout.decode("utf8"))
print(stderr)
