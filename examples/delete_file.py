from pyinfra.operations import files

files.file('hello.txt', present=False)
