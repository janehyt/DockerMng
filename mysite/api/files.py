# -*- coding: UTF-8 -*- 
import os,shutil,zipfile
from mysite import settings

# class FileService(object):
def getUploadDir(path):
	return os.path.join(settings.UPLOAD_ROOT,path)
def removeDirs(path):
	if os.path.exists(path):
		# print "remove dir"
		shutil.rmtree(path)

#参数分别为volumes参数，用户目录，容器名称,最终处理目录为path/containers/name
def resolveVolumes(volumes,path,name):
	results = ""
	con_path=os.path.join(path,'containers',name)
	removeDirs(con_path)
	if len(volumes)>0:
		vs = volumes.split(",")
		for v in vs:
			gs = v.split(":")
			if len(gs)==2:
				#绝对路径，直接返回
				if os.path.isabs(gs[0]):
					results+=gs[0]+":"+gs[1]+","
					continue
				#上传文件，处理
				tmp=os.path.join(path,gs[0])
				if os.path.isfile(tmp):
					# print tmp
					filePath = resolveFile(tmp,con_path)
					results+=filePath+":"+gs[1]+","
					continue
				tmp=os.path.join(con_path,gs[0])
				if not os.path.exists(tmp):
					os.makedirs(tmp)
					results+=tmp+":"+gs[1]+","
				#相对路径,创建文件夹
	if len(results)>0:
		results=results[0:len(results)-1]
	# print results
	return results;
#zip则解压，否则cp，filename为文件路径，path为目标路径
def resolveFile(filename,path):
	basename=os.path.basename(filename)
	splits = os.path.splitext(basename)
	if splits[1]==".zip":
		path = os.path.join(path,splits[0])
		unzip(filename,path)
	else:
		if not os.path.exists(path):
			os.makedirs(path)
		path = os.path.join(path,basename)
		shutil.copyfile(filename,path)
	# unzip_dir(filename,path)
	return path
#文件上传
def fileUpload(filename,file,path):
	# upload_dir = getUploadDir(path)
	if not os.path.exists(path):
	    os.makedirs(path)
	filename = path+"/"+filename
	if os.path.exists(filename):
	    return 403

	with open(filename,'wb+') as destination:
	    for chunk in file.chunks():
	        destination.write(chunk)
	    destination.close()
	        # ...
	        # do some stuff with uploaded file
	        # ...
	return 204

#文件列表
def fileList(path):
	# upload_dir = getUploadDir(path)
	if os.path.exists(path) and os.path.isdir(path):
		dir_list = os.listdir(path)
		result = []
		for p in dir_list:
			full = os.path.join(path,p)
			if os.path.isfile(full):
				item = {"name":p,"size":os.path.getsize(full)}
				result.append(item)
		return result
	return None
def unzip(zipfilename, unzipdirname):
	zfile = zipfile.ZipFile(zipfilename,'r')
	for filename in zfile.namelist():
		
		if not filename.endswith('/'):
			f = os.path.join(unzipdirname,filename)
			dirname = os.path.dirname(f)
			if not os.path.exists(dirname):
				os.makedirs(dirname)
			data = zfile.read(filename)
			file = open(f, 'w+b')
			file.write(data)
			file.close()

	print "success"

def renameFile(filename,newname):
	if os.path.isfile(filename):
		os.rename(filename,newname)
		return 204
	return 403
def destroyFile(filename):
	if os.path.isfile(filename):
		os.remove(filename)
		return 204
	elif os.path.isdir(filename):
		removeDirs(filename)
		return 204
	return 403

def dirSize(path):
	size = 0
	if os.path.isdir(path):
		for root , dirs, files in os.walk(path, True):
			size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
	return size

def getDetail(path):
	if os.path.isdir(path):
		dir_list = os.listdir(path)
		result=[]
		for p in dir_list:
			full=os.path.join(path,p)
			result.append({"name":p,"isdir":os.path.isdir(full),"isfile":os.path.isfile(full)})
		return result
	elif os.path.isfile(path):
		all_the_text=open(path).read()
		return {"content":all_the_text}

def saveFile(path,content):
	with open(path,"w") as des:
		des.write(content)
		des.close()
	return True