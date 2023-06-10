import os
from Writer import Writer


# Falls python3 oder python2, müssen Sie python nach python{Version} verändern
python_cmd="python -m pip install {}"
step = "[ + ] - Installing {}"

install_package = lambda x:os.system(python_cmd.format(x))
get_step = lambda x:step.format(x)

def installMe():
    try:
        import colorama
    except:
        print("[ + ] - Install colorama")
        install_package("colorama")
        import colorama

    writer = Writer()

    try:
        import sklearn
    except:
        writer.writeStep(get_step("sklearn"))
        install_package("sklearn")
    try:
        import pickle
    except:
        writer.writeStep(get_step("pickle"))
        install_package("pickle-mixin")
    try:
        from PyQt5 import QtCore
    except:
        writer.writeStep(get_step("PyQt5"))
        install_package("PyQt5 pyqt-tools")

    try:
        import numpy as np
    except:
        writer.writeStep(get_step("numpy"))
        install_package("numpy")
        import numpy as np

    try:
        import pandas as pd
    except:
        writer.writeStep(get_step("pandas"))
        install_package("pandas")
        import pandas as pd


