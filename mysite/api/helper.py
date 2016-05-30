# -*- coding: UTF-8 -*-
'''helper'''
import json
import calendar
import datetime
from docker import errors
from .dockerconn import DockerClient
from .models import Process, Image, Container

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
                # print "build"
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
        # print prtmp
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
        process.detail = json.dumps(detail)
        process.save()
        return detail

class ContainerHelper(object):
    '''ContainerHelper'''
    __cli = DockerClient().get_client()

    def __init__(self,container):
        if isinstance(container, Container):
            self.__container = container
        else:
            raise TypeError("expect Container")

    def destroy(self):
        try:
            self.__cli.remove_container(self.__container.name)
        except errors.APIError, errormsg:
            if errormsg.response.status_code==404:
                pass
            else:
                return {"data":{"reason":errormsg.response.reason,\
                "detail":errormsg.explanation},"status":errormsg.response.status_code}
        binds = self.__container.binds.all()
        volume_to_check=[]
        for bind in binds:
            volume_to_check.append(bind.volume)
        self.__container.delete()
        for volume in volume_to_check:
            if volume.binds.count() is 0 and volume.private:
                volume.delete()

        return {"data":"删除成功","status":200}

    def detail(self):
        data = {"id":self.__container.id,"name":self.__container.name,\
            "config":self.__container.display_config(),"created":self.__container.created}
        try:
            data["inspect"] = self.__cli.inspect_container(self.__container.name)
            if data["inspect"]["State"]["FinishedAt"] == "0001-01-01T00:00:00Z":
                data["inspect"]["State"]["FinishedAt"] = None
            data["status"] = data["inspect"]["State"]["Status"]
        except errors.APIError, errormsg:
            if errormsg.response.status_code == 404:
                data["status"] = "none"
            else:
                return {"data":{"reason":errormsg.response.reason,\
                    "detail":errormsg.explanation},"status":errormsg.response.status_code}
        return {"data":data,"status":200}

    def stat(self):
        data = {}
        try:
            d = self.__cli.stats(container=self.__container.name, stream=False)
            data["block"]=self.__solve_block(d.get("blkio_stats"))
            data["cpu"]=self.__solve_cpu(d.get("cpu_stats"))
            data["memory"]=self.__solve_memory(d.get("memory_stats"))
            data["network"]=self.__solve_net(d.get("networks"))
            data["time"] = calendar.timegm(datetime.datetime.now().timetuple())*1000

        except errors.APIError, e:
            return {"data":{"reason":e.response.reason,\
                "detail":e.explanation},"status":e.response.status_code}
        return {"data":data,"status":200}
   
    def run(self):
        params =  self.__get_params()
        try:
            data = self.__cli.create_container(**params)           
        except errors.APIError, e:
            if e.response.status_code == 409:
               pass
            else:
                return {"data":{"reason":e.response.reason,\
                "detail":e.explanation},"status":e.response.status_code}
        return self.start()

    def start(self):
        try:
            self.__cli.start(self.__container.name)
        except errors.APIError, e:
            return {"data":{"reason":e.response.reason,\
                "detail":e.explanation},"status":e.response.status_code}
        return {"data":"启动成功","status":200}

    def stop(self):
        try:
            self.__cli.stop(self.__container.name)
        except errors.APIError, e:
            return {"data":{"reason":e.response.reason,\
                "detail":e.explanation},"status":e.response.status_code}
        return {"data":"停止成功","status":200}

    def pause(self):
        try:
            self.__cli.pause(self.__container.name)
        except errors.APIError, errormsg:
            return {"data":{"reason":errormsg.response.reason,\
                "detail":errormsg.explanation},"status":errormsg.response.status_code}
        return {"data":"暂停成功","status":200}

    def unpause(self):
        try:
            self.__cli.unpause(self.__container.name)
        except errors.APIError, errormsg:
            return {"data":{"reason":errormsg.response.reason,\
                "detail":errormsg.explanation},"status":errormsg.response.status_code}
        return {"data":"恢复成功","status":200}

    def restart(self):
        try:
            self.__cli.restart(self.__container.name)
        except errors.APIError, errormsg:
            return {"data":{"reason":errormsg.response.reason,\
                "detail":errormsg.explanation},"status":errormsg.response.status_code}
        return {"data":"重启成功","status":200}

    def __get_params(self):
        params = {"name":self.__container.name,\
            "image":str(self.__container.image),"detach":True}
        host_config = self.__get_host_config()
        ports = self.__ports_config()
        if ports["host"]:
            host_config["PortBindings"] = ports["host"]
        if ports["params"]:
            params["ports"] = ports["params"]
        params["host_config"] = host_config
        if self.__container.command:
            params["command"] = self.__container.command.split(",")
        envs = self.__get_envs()
        if envs:
            params["environment"] = envs
        return params

    def __get_envs(self):
        envs = []
        for env in self.__container.environments.all():
            envs.append(unicode(env))
        return envs

    def __get_host_config(self):
        host_config={}
        host_config["RestartPolicy"] = self.__host_restart_config()
        links = self.__host_links_config()
        if links:
            host_config["Links"] = links
        binds = self.__host_binds_config()
        if binds:
            host_config["Binds"] = binds
        return host_config


    def __ports_config(self):
        ports={"params":[],"host":{}}
        for port in self.__container.ports.all():
            internal = str(port.port)
            ports["params"].append(internal)
            if port.external:
                ports["host"][internal+"/tcp"] = [{"HostPort":port.expose}]
        return ports

    def __host_restart_config(self):
        if self.__container.restart:
            return { "Name": "always" }
        else:
            return { "Name": "", "MaximumRetryCount": 5 }
    
    def __host_links_config(self):
        links = []
        for link in self.__container.links.all():
            links.append(unicode(link))
        return links
    def __host_binds_config(self):
        binds = []
        for bind in self.__container.binds.all():
            # print unicode(bind)
            b = bind.volume.path+":"+bind.path
            binds.append(b)
        return binds

    def __solve_block(self,block):
        block_data={"Read":0,"Write":0,"Sync":0,"Async":0,"Total":0}
        tmp = block.get("io_service_bytes_recursive")
        if tmp: 
            for t in tmp:
                if t.get("op") in block_data:
                    block_data[t.get("op")]=block_data[t.get("op")]+t.get("value",0)
        return block_data
    def __solve_cpu(self,cpu):
        return {
            "usermode":cpu["cpu_usage"]["usage_in_usermode"],
            "kernelmode":cpu["cpu_usage"]["usage_in_kernelmode"],
            "total":cpu["cpu_usage"]["total_usage"],
            "system":cpu["system_cpu_usage"]
        }
    def __solve_memory(self,memory):
        return {
            "usage":memory["usage"],
            "limit":memory["limit"],
            "max":memory["max_usage"],
        }
    def __solve_net(self,net):
        net_data={"read":0,"write":0}
        if net:
            for n in net:
                net_data["read"]+=net[n]["rx_bytes"]
                net_data["write"]+=net[n]["tx_bytes"]
        return net_data