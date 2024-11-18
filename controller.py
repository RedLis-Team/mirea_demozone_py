import os, re

import shutil

from fastapi import HTTPException, UploadFile
from starlette import status

"""
Source:
https://github.com/BadWolf1st/wolfinfo/blob/wolfinfo5-back/backend/api/src/req/images/controller.py
"""

class Controller:
    def __init__(self):
        """
        The function initializes a class instance with a specified files path and creates directories if
        they do not exist.
        """
        if not os.path.exists("./data"):
            print("WARNING: Data directory not found! Creating dir...")
            os.mkdir("./data")
        self.files_path = "./data/files"
        if not os.path.exists(self.files_path):
            print("WARNING: Files directory not found! Creating dir...")
            os.mkdir(self.files_path)
        # if not os.path.exists(self.files_path + "/avatars"):
        #     print("WARNING: Avatar directory not found! Creating dir...")
        #     os.mkdir(self.files_path + "/avatars")

    @staticmethod
    def delete(path):
        # TODO: add check for file existence and raise 404 if not found
        """
        The function `delete` deletes a file located at the specified `path`.

        :param path: The `path` parameter in the `delete` function is a string that represents the file
        path of the file that you want to delete. This function uses the `os.remove()` method to delete
        the file located at the specified path
        """
        os.remove(path)

    def write(self, file: UploadFile, name: str, type: str = "images", no_check: bool = False) -> None: # no_check = True if we update file
        """
        This function writes an uploaded file to a specified location with optional checks and updates.

        :param file: The `file` parameter is of type `UploadFile` and represents the file that will be
        written to the specified location. It is used to read the contents of the uploaded file and
        write it to the destination file path
        :type file: UploadFile
        :param name: The `name` parameter in the `write` function represents the name of the file being
        uploaded. It is a string that specifies the name of the file. In the function, the name is
        modified to include the path "avatars/" if the type of file is "avatars"
        :type name: str
        :param type: The `type` parameter in the `write` method is used to specify the type of file
        being written. It has a default value of "images" but can be overridden with values like
        "avatars" based on the use case, defaults to images
        :type type: str (optional)
        :param no_check: The `no_check` parameter in the `write` method is a boolean flag that indicates
        whether to skip the file existence check before writing the file. When `no_check` is set to
        `True`, it means that the method should update the file without checking if a file with the same
        name already, defaults to False
        :type no_check: bool (optional)
        """
        # name = f"avatars/{name}" if type=="avatars" else name
        name = name
        full_path = f"{self.files_path}/{name}"
        if not no_check:
            if os.path.isfile(full_path):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        try:
            with open(full_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        finally:
            file.file.close()

    def read(self, name: str, type: str = "images") -> bytes:
        """
        This Python function reads a file as bytes from a specified path, handling exceptions for file
        not found.

        :param name: The `name` parameter is a string that represents the name of the file to be read
        :type name: str
        :param type: The `type` parameter in the `read` method specifies the type of file to read. By
        default, it is set to "images", but it can be optionally set to "avatars". If the type is
        "avatars", the method will look for the file in the "avatars" directory by, defaults to images
        :type type: str (optional)
        :return: The `read` method returns the content of the file specified by the `name` parameter as
        bytes. If the file is found and successfully read, its content is returned. If the file is not
        found, a `FileNotFoundError` exception is caught and an HTTPException with a status code of 404
        (Not Found) and a detail message of "File not found" is raised.
        """
        # name = f"avatars/{name}" if type=="avatars" else name
        name = name
        try:
            with open(f"{self.files_path}/{name}", "rb") as session:
                return session.read()
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    @staticmethod
    def get_file_type_from_name(filename: str, get_prefix: bool = False) -> str:
        """
        The function `get_file_type_from_name` returns the file type of a given filename, defaulting to
        'image/jpeg' unless specified to return the file extension.

        :param filename: The `filename` parameter is a string that represents the name of a file, including
        its extension
        :type filename: str
        :param get_prefix: The `get_prefix` parameter is a boolean flag that determines whether the function
        should return only the file extension prefix (e.g., "png" or "jpeg") or the full MIME type (e.g.,
        "image/png" or "image/jpeg") based on the provided filename, defaults to False
        :type get_prefix: bool (optional)
        :return: The function `get_file_type_from_name` is returning a string that represents the file type
        of the given filename. If the `get_prefix` parameter is set to `True`, it returns the file type
        prefix (e.g., "png" or "jpeg"). If `get_prefix` is `False`, it returns the full file type string
        (e.g., "image/png" or "image
        """
        if get_prefix:
            return re.search(r'\.([a-zA-Z0-9]+)$', filename).group(1)
        return 'image/png' if re.search(r'\.([a-zA-Z0-9]+)$', filename).group(1) == "png" else 'image/jpeg'
