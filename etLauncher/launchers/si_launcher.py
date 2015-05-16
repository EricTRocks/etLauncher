import os
import subprocess

from etLauncher.preset_processor import PresetProcessor

__LAUNCHER_NAME = "softimage"


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


def getBatch(preset):

    processor = PresetProcessor()
    appData = processor.getAppData(processor.getAppName(preset))

    if 'batch' not in appData.keys():
        raise KeyError("'batch' not specified in the application json!")

    return appData['batch']


def getWorkgroups(preset):

    processor = PresetProcessor()
    presetData = processor.getPresetData(preset)

    workgroups = []
    for eachEnv in presetData['envs']:
        envData = processor.getEnvData(eachEnv)

        if 'workgroups' not in envData:
            continue

        workgroups += envData['workgroups']

    workgroupsCombined = ";".join(workgroups)

    return workgroupsCombined


def updateUserPref(preset):

    processor = PresetProcessor()
    appData = processor.getAppData(processor.getAppName(preset))

    if 'xsi_user_home' not in appData.keys():
        raise KeyError("'xsi_user_home' not specified in the application json!")

    workgroups = getWorkgroups(preset)

    # =====================
    # Update XSI Pref File
    # =====================
    prefData = None
    xsiPrefFile = os.path.join(appData['xsi_user_home'], 'Data', 'Preferences', 'default.xsipref')
    with open(xsiPrefFile, 'r') as prefFile:
        prefData = prefFile.readlines()

    if prefData is None:
        raise IOError('Could not find the user preference file: ' + xsiPrefFile)

    newPrefData = list(prefData)
    for i, each in enumerate(prefData):
        if each.startswith('data_management.workgroup_appl_path'):
            newPrefData[i] = 'data_management.workgroup_appl_path = ' + workgroups + '\n'

    with open(xsiPrefFile, 'w') as newPrefFile:
        newPrefFile.write(''.join(newPrefData))

    return


def launcher(preset):

    updateUserPref(preset)

    batch = getBatch(preset)
    executable = getExecutable(preset)

    subprocess.Popen('%s' % (executable), shell=True)

    return True