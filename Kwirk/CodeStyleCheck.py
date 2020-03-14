import pep8
import os

if __name__ == "__main__":
    for file in os.listdir():
        if file[-3:] == ".py":
            checker = pep8.Checker(file, show_source=True)
            errors = checker.check_all()
            print("{} error(s) in {}".format(errors, file))
