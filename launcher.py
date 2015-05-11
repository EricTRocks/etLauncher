import os
import argparse
import subprocess
import json


def combineVars(env):
    """Combines the environment variables and ensures there are no duplicates.

    Arguments:
    env -- Dict, dictionary of variables and values (list) to use.

    Return:
    Dict, processedVars.

    """

    processedVars = {}
    for var, paths in env.iteritems():
        if var in os.environ:
            combineVars = os.environ[var] + ';' + ';'.join(paths)
            processedVars[var] = ';'.join(list(set(combineVars.split(';'))))

        else:
            combineVars = ';'.join(paths)
            processedVars[var] = ';'.join(list(set(combineVars.split(';'))))

    return processedVars


def getApps():
    """Gets all the available apps from the 'apps' directory.

    Return:
    Dict, app name as the key and the file name as the value.

    """

    appsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apps')

    apps = {}
    for eachFile in os.listdir(appsDir):
        if eachFile.endswith('.json'):
            apps[eachFile.split('.')[0]] = os.path.join(appsDir, eachFile)

    return apps


def getEnvs():
    """Gets all the available environments from the 'envs' directory.

    Return:
    Dict, env name as the key and the file name as the value.

    """

    envsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'envs')

    envs = {}
    for eachFile in os.listdir(envsDir):
        if eachFile.endswith('.json'):
            envs[eachFile.split('.')[0]] = os.path.join(envsDir, eachFile)

    return envs


def launch(app, env):
    """Launches the application with specified environment.

    Arguments:
    app -- String, name of the application to launch.
    env -- String, name of the environment to use.

    Return:
    True if successful.

    """

    appData = None
    with open(app) as appFile:
        appData = json.load(appFile)

    envData = None
    with open(env) as envFile:
        envData = json.load(envFile)

    combinedVars = combineVars(envData)
    for k, v in combinedVars.iteritems():
        os.environ[k] = v

    subprocess.Popen('%s' % (appData['executable']), shell=True)

    return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse arguments for launcher.')
    parser.add_argument('app', help="The application you'd like to launch.")
    parser.add_argument('env', help="The environment you'd like to launch with.")
    args = parser.parse_args()

    app = args.app
    env = args.env

    apps = getApps()
    envs = getEnvs()

    if app not in apps.keys():
        raise IOError("Application '" + app + "' not found!")

    if env not in envs.keys():
        raise IOError("Environment '" + env + "' not found!")

    print "Launching Application: " + app
    print "Launching Environment: " + env

    launch(apps[app], envs[env])