import os
import sys
import traceback
import argparse
import subprocess
import json

from etLauncher.preset_processor import PresetProcessor
from etLauncher.launchers import getLauncher


class Launcher(object):
    """Application Launcher"""

    def __init__(self):
        super(Launcher, self).__init__()
        self._processor = PresetProcessor()


    # ==================
    # Processor Methods
    # ==================
    def getProcessor(self):
        """Gets the processor for this launcher.

        Return:
        Instance, processor.

        """

        return self._processor


    # ===============
    # Launch Methods
    # ===============
    def executeLaunch(self, preset):

        processor = self.getProcessor()

        appName = processor.getAppName(preset)
        print "Launching Preset: " + appName

        appData = processor.getAppData(appName)

        if 'launcher' not in appData:
            raise KeyError("'launcher' not specified in the application file!")

        presetLauncher = getLauncher(appData['launcher'])
        presetLauncher(preset)

        return True


    def launch(self, preset):
        """Launches the specified preset.

        Arguments:
        preset -- String, prest to launch.

        Return:
        True if successful.

        """

        processor = self.getProcessor()

        if preset not in processor.getPresets().keys():
            raise KeyError("'" + preset + "' preset not registered!")

        processor.setEnvironment(preset)
        self.executeLaunch(preset)

        return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse arguments for launcher.')
    parser.add_argument('preset', help="The preset you'd like to launch.")
    args = parser.parse_args()

    preset = args.preset

    launcher = Launcher()
    launcher.launch(preset)