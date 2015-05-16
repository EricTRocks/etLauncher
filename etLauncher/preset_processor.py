import os
import sys
import traceback
import argparse
import subprocess
import json


class PresetProcessor(object):
    """Preset Processor"""

    def __init__(self):
        super(PresetProcessor, self).__init__()
        self._apps = None
        self._envs = None
        self._presets = None

        self.registerApps()
        self.registerEnvs()
        self.registerPresets()


    # =====================
    # Registration Methods
    # =====================
    def getApps(self):
        """Gets the applications that are currently registered.

        Return:
        Dict, registered applications.

        Example:
        {
          "softimage2015": "C:\\etLauncher\\apps\\softimage_2015.json",
          "maya2015": "C:\\etLauncher\\apps\\maya_2015.json"
        }

        """

        return self._apps


    def registerApps(self):
        """Registers applications in the 'apps' directory.

        Return:
        True if successful.

        """

        appsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apps')

        apps = {}
        for root, dirs, files in os.walk(appsDir):
            for eachFile in files:
                if eachFile.endswith('.json'):
                    appFilePath = os.path.join(root, eachFile)

                    appData = None
                    with open(appFilePath) as appFile:
                        appData = json.load(appFile)

                    appName = appData['name']
                    if appName in apps.keys():
                        print "Skipping Application '" + appName + "' as it is already registered."
                        continue

                    apps[appName] = appFilePath

        self._apps = apps

        return True


    def getEnvs(self):
        """Gets the environments that are currently registered.

        Return:
        Dict, registered environments.

        Example:
        {
          "kraken": "C:\\etLauncher\\envs\\kraken.json",
          "kraken_maya": "C:\\etLauncher\\envs\\maya\\kraken_maya.json"
        }

        """

        return self._envs


    def registerEnvs(self):
        """Registers environments in the 'envs' directory.

        Return:
        True if successful.

        """

        envsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'envs')

        envs = {}
        for root, dirs, files in os.walk(envsDir):
            for eachFile in files:
                if eachFile.endswith('.json'):
                    envFilePath = os.path.join(root, eachFile)

                    envData = None
                    with open(envFilePath) as envFile:
                        envData = json.load(envFile)

                    envName = envData['name']
                    if envName in envs.keys():
                        print "Skipping Environment '" + envName + "' as it is already registered."
                        continue

                    envs[envName] = envFilePath

        self._envs = envs

        return True


    def getPresets(self):
        """Gets the presets that are currently registered.

        Return:
        Dict, registered presets.

        Example:
        {
          "soft2015_kraken": "C:\\etLauncher\\presets\\soft2015_kraken.json"
        }

        """

        return self._presets


    def registerPresets(self):
        """Registers presets in the 'presets' directory.

        Return:
        True if successful.

        """

        presetsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'presets')

        presets = {}
        for root, dirs, files in os.walk(presetsDir):
            for eachFile in files:
                if eachFile.endswith('.json'):
                    presetFilePath = os.path.join(root, eachFile)

                    presetData = None
                    with open(presetFilePath) as presetFile:
                        presetData = json.load(presetFile)

                    presetName = presetData['name']
                    if presetName in presets.keys():
                        print "Skipping Preset '" + presetName + "' as it is already registered."
                        continue

                    presets[presetName] = presetFilePath

        self._presets = presets

        return True


    # ============
    # App Methods
    # ============
    def getAppName(self, preset):
        """Gets the name of the application that will be launched from the specified
        preset.

        Arguments:
        preset -- String, name of the preset being launched.

        Return:
        String, name of the application to launch.

        """

        # Get Preset Data
        presetData = self.getPresetData(preset)

        # Check application is registered
        if 'application' not in presetData:
            raise KeyError("'application' not specified in the preset file!")

        appData = self.getAppData(presetData['application'])
        if 'name' not in appData:
            raise KeyError("'name' not found in application data!")

        return appData['name']


    def getAppData(self, app):
        """Gets the data for the specified app.

        Arguments:
        app -- String, the application to get data for.

        Return:
        Dict, data read from application's json file.

        """

        appData = None
        with open(self._apps[app]) as appFile:
            appData = json.load(appFile)

        return appData


    def getAppExecutable(self, preset):
        """Gets the application's executable from the specified preset.

        Arguments:
        preset -- String, preset to get application executable for.

        Return:
        String, executable path.

        """

        # Get Preset Data
        presetData = self.getPresetData(preset)

        # Check application is registered
        if 'application' not in presetData:
            raise KeyError("'application' not specified in the preset file!")

        app = presetData['application']
        if app not in self.getApps().keys():
            raise KeyError("'" + app + "' application not registered!")

        executable = self.getAppData(app)['executable']

        return executable


    # ============
    # Env Methods
    # ============
    def getEnvData(self, env):
        """Gets the data for the specified env.

        Arguments:
        env -- String, the environment to get data for.

        Return:
        Dict, data read from environment's json file.

        """

        envData = None
        with open(self._envs[env]) as envFile:
            envData = json.load(envFile)

        return envData


    def processEnvironment(self, preset):
        """Processes the environment based ont he preset that is specified.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        # Get Preset Data
        presetData = self.getPresetData(preset)

        # Check environments are registered
        if 'envs' not in presetData:
            raise KeyError("'envs' not specified in the preset file!")

        # Filter Environments
        validEnvs = []
        for env in presetData['envs']:
            if env not in self.getEnvs().keys():
                print "'" + env + "' environment not registered. Skipping."
                continue

            validEnvs.append(env)

        # Combine Environments
        combinedEnvs = {}
        for env in validEnvs:
            envData = self.getEnvData(env)

            if 'vars' not in envData:
                raise KeyError("'vars'" + " not specified in environment: " + env)

            combinedEnvs.update(envData['vars'])

        return combinedEnvs


    def setEnvironment(self, preset):
        """Sets the environment based on the preset that is specified.

        Arguments:
        preset -- String, name of preset to set environment for.

        Return:
        True if successful.

        """

        combinedEnvs = self.processEnvironment(preset)

        # Set Environment Variables
        for k, v in combinedEnvs.iteritems():
            if type(v) is list:
                os.environ[k] = ";".join(v)
            elif type(v) is str:
                os.environ[k] = v
            else:
                continue

        return True


    # ===============
    # Preset Methods
    # ===============
    def getPresetData(self, preset):
        """Gets the preset data from the specified preset.

        Arguments:
        preset -- String, preset to get data for.

        Return:
        Dict, data contained in the preset json file.

        """

        # Get Preset Data
        presetData = None
        with open(self._presets[preset]) as presetFile:
            presetData = json.load(presetFile)

        return presetData
