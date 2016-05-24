'''helper'''
# -*- coding: UTF-8 -*-
import json
from .dockerconn import DockerClient
from .models import Process, Image
from docker import errors

class ImageHelper(object):
    '''ImageHelper'''
    __cli = DockerClient().get_client()

    def __init__(self,image):
        if type(image) is Image:
            self.__image=image
        else:
            raise TypeError("expect Image")

    def pull(self):
        self.__image.status = Image.PULLING
        self.__image.save()
        self.__image.processes.all().delete()
        try:
            pull_image = self.__cli.pull(unicode(self.__image), stream=True)
            for line in pull_image:
                prtmp = json.loads(line)
                # print prtmp
                status = prtmp.get("status", "")
                p_id = prtmp.get("id", Process.DEFAULT)
                # if "Pulling from" not in status:
                process = self.__image.processes.get_or_create(
                    pid=p_id)[0]
                process.status = status
                detail = prtmp.get("progressDetail", {})
                process.detail = json.dumps(detail)
                process.proc = prtmp.get("progress", "")
                process.save()
            if "Status: Downloaded newer image" in status or\
            "Status: Image is up to date" in status:
                self.__image.status = Image.EXISTED
                self.__image.save()
                self.__image.processes.all().delete()
            else:
                self.__image.status = Image.ERROR
                self.__image.save()
                return 408
                # return Response({"detail":\
                #     "Error occurs when pulling image"}, status=408)
        except errors.APIError, errormsg:
            self.__image.status = Image.ERROR
            self.__image.save()
            return errormsg.response.status_code
        return 200
            # return Response({"reason":errormsg.response.reason,\
            #     "detail":errormsg.explanation},\
            #     status=errormsg.response.status_code)