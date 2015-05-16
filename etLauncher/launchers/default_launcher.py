import os
import subprocess

from etLauncher.preset_processor import PresetProcessor

__LAUNCHER_NAME = "default"


def nameTest(launcherName):
    """Tests whether this launcher matches the input name.

    Arguments:
    launcherName -- String, name to match.

    Return:
    True if successful.

    """

    return launcherName == __LAUNCHER_NAME


def getExecutable(preset):

    processor = PresetProcessor()

    return processor.getAppExecutable(preset)


def launcher(preset):

    executable = getExecutable(preset)

    subprocess.Popen('%s' % (executable), shell=True)

    return True