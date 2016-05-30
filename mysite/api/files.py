# -*- coding: UTF-8 -*-
'''files'''
import os
import shutil
import zipfile
from mysite import settings
from .models import Volume
class VolumeService(object):
    '''VolumeService'''

    def __init__(self, user, path=""):
        self.__root = os.path.join(settings.UPLOAD_ROOT, str(user))
        if not os.path.isdir(self.__root):
            os.makedirs(self.__root)
        self.__path = os.path.join(self.__root, path)
        self.__set_bread(str(user), path)

    def list(self):
        '''list'''
        if os.path.isdir(self.__path):
            dir_list = os.listdir(self.__path)
            result = []
            for name in dir_list:
                full = os.path.join(self.__path, name)
                item = {"name":name, "isfile":os.path.isfile(full),\
                    "editable":self.__editable(full),\
                    "path":full[len(self.__root)+1:],\
                    "size":self.__get_size(full)}
                result.append(item)

            return {"bread":self.__bread, "list":result}
        return None
    def get_size(self):
        return self.__get_size(self.__path)

    def download(self):
        '''download'''
        if os.path.isfile(self.__path):
            name = os.path.basename(self.__path)
            return {"name":name, "stream":self.__file_iterator()}
        return None
    def mkdir(self, name):
        '''mkdir'''
        path = os.path.join(self.__path, name)
        if not os.path.isdir(path):
            os.makedirs(path)
            return 204
        return 403

    def file_upload(self, filename, fileobj):
        '''upload'''
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        filename = os.path.join(self.__path, filename)
        if os.path.exists(filename):
            return 403
        with open(filename, 'wb+') as destination:
            for chunk in fileobj.chunks():
                destination.write(chunk)
            destination.close()
        return 204
    def rename(self, name):
        '''rename'''
        if os.path.exists(self.__path) and self.__editable(self.__path):
            name = os.path.join(os.path.dirname(self.__path), name)
            os.rename(self.__path, name)
            return 204
        return 403
    def remove(self):
        '''remove'''
        if os.path.exists(self.__path) and self.__editable(self.__path):
            if os.path.isfile(self.__path):
                os.remove(self.__path)
            elif os.path.isdir(self.__path):
                shutil.rmtree(self.__path)
            return 204
        return 403

    def unzip(self):
        '''unzip'''
        basename = os.path.basename(self.__path)
        splits = os.path.splitext(basename)
        zipdirname = os.path.join(os.path.dirname(self.__path), splits[0])
        if os.path.isdir(zipdirname):
            return 403
        if splits[1] == ".zip" and os.path.exists(self.__path):
            zfile = zipfile.ZipFile(self.__path, 'r')
            for filename in zfile.namelist():
                if not filename.endswith('/'):
                    tmpf = os.path.join(zipdirname, filename)
                    dirname = os.path.dirname(tmpf)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    data = zfile.read(filename)
                    fileobj = open(tmpf, 'w+b')
                    fileobj.write(data)
                    fileobj.close()

            return 204
        return 404

    def get_path(self):
        '''getpath'''
        if os.path.exists(self.__path):
            return self.__path
        return None
    def __get_size(self, path):
        '''_get_size'''
        size = 0
        if self.__root in path:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path, True):#pylint: disable=unused-variable
                    size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
            elif os.path.isfile(path):
                size = os.path.getsize(path)
        return size

    def __file_iterator(self, chunk_size=512):
        '''_file_iterator'''
        with open(self.__path) as fileobj:
            while True:
                chunk = fileobj.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    break
    def __set_bread(self, root, path):
        tmp = ""
        bread = [{"name":root, "path":tmp}]
        paths = path.split("/")
        for name in paths:
            if name:
                tmp = os.path.join(tmp, name)
                item = {"name":name, "path":tmp}
                bread.append(item)
        self.__bread = bread

    def __editable(self, path):
        '''__editable'''
        if self.__root in path:
            vol = Volume.objects.filter(path__contains=path).count()#pylint: disable=no-member
            # print v
            return vol is 0
        return False
