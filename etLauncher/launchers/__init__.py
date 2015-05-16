import os
import glob

__all__ = [os.path.splitext(os.path.basename(launcher))[0]
           for path in __path__
           for launcher in glob.glob(os.path.join(path, '*_launcher.py'))]


def getLauncher(launcherName):
    """Returns the appropriate launcher with the specified name.

    Arguments:
    launcherName -- String, name of the launcher to get.

    Return:
    Launcher, instance of the launcher.

    """

    launcher = None
    for eachLauncher in __all__:
        mod = __import__("etLauncher.launchers." + eachLauncher, fromlist=['nameTest'])
        reload(mod)

        if mod.nameTest(launcherName) is True:
            loaded_mod = __import__("etLauncher.launchers." + eachLauncher, fromlist=['launcher'])
            reload(loaded_mod)

            launcher = loaded_mod.launcher

    if launcher is None:
        print "Failed to find launcher. Falling back to Python launcher."

        from etLauncher.launchers.default_launcher import launcher

    return launcher
