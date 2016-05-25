'''helper'''
# -*- coding: UTF-8 -*-
import json
from .dockerconn import DockerClient
from .models import Process, Image, Container
from docker import errors

def port_generater():
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    tt= random.randint(10000,65534)
    if tt not in procarr:
        return tt
    else:
        port_generater()

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
                status = self.__resolve_process(line)
            if "Status: Downloaded newer image" in status or\
            "Status: Image is up to date" in status:
                self.__image.status = Image.EXISTED
                self.__image.save()
                self.__image.processes.all().delete()
            else:
                self.__image.status = Image.ERROR
                self.__image.save()
                return {"data":{"detail:Error occurs when pulling image"},\
                "status":408}
                # return Response({"detail":\
                #     "Error occurs when pulling image"}, status=408)
        except errors.APIError, errormsg:
            self.__image.status = Image.ERROR
            self.__image.save()
            return {"data":{"reason":errormsg.response.reason,"detail":errormsg.explanation},\
            "status":errormsg.response.status_code}
        return self.__image
            # return Response({"reason":errormsg.response.reason,\
            #     "detail":errormsg.explanation},\
            #     status=errormsg.response.status_code)
    def build(self):
        self.__image.status = Image.BUILDING
        self.__image.save()
        self.__image.processes.all().delete()
        try:
            build_image = self.__cli.build(path=self.__image.builddir,\
                tag=unicode(self.__image), rm=True, stream=True)
            for line in build_image:
                print "build"
                status = self.__build_process(line)
                print status
            if "Successfully built" in status:
                self.__image.status = Image.EXISTED
                self.__image.save()
                self.__image.processes.all().delete()
            else:
                self.__image.status = Image.ERROR
                self.__image.save()
                return {"data":{"detail:Error occurs when building image"},\
                "status":408}
                # return Response({"detail":\
                #     "Error occurs when pulling image"}, status=408)
        except errors.APIError, errormsg:
            self.__image.status = Image.ERROR
            self.__image.save()
            return {"data":{"reason":errormsg.response.reason,"detail":errormsg.explanation},\
            "status":errormsg.response.status_code}
        return self.__image
    
    def destroy(self):
        try:           
            self.__cli.remove_image(unicode(self.__image))
        except errors.APIError,e:
            if e.response.status_code==404:
                pass
            else:
                return {"data":{"reason":errormsg.response.reason,"detail":errormsg.explanation},\
            "status":errormsg.response.status_code}
        self.__image.delete()
        return {"data":"", "status":204}

    def __resolve_process(self,line):
        prtmp = json.loads(line)
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
        return status
    def __build_process(self,line):
        prtmp = json.loads(line)
        process = self.__image.processes.get_or_create(
            pid=Process.DEFAULT)[0]
        detail = prtmp.get("stream","")
        process.detail = detail
        process.save()
        return detail

class ContainerHelper(object):
    '''ContainerHelper'''
    __cli = DockerClient().get_client()

    def __init__(self,container):
        if isinstance(container, Container):
            self.__contaienr = container
        else:
            raise TypeError("expect Container")

    def destroy(self):
        '''destroy'''
        return "Response()"

    def detail(self):
        '''detail'''
        return "Response()"

    def stat(self):
        '''stat'''
        return "Response()"
   
    def run(self):
        '''run'''
        return "Response()"

    def stop(self):
        '''stop'''
        return "Response()"

    def pause(self):
        '''pause'''
        return "Response()"

    def unpause(self):
        '''unpause'''
        return "Response()"

    def restart(self):
        '''restart'''
        return "Response()"