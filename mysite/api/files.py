# -*- coding: UTF-8 -*- 
import os,shutil,zipfile
from mysite import settings
from .models import Volume
class VolumeService(object):

	def __init__(self,user,path=""):
		self._root = os.path.join(settings.UPLOAD_ROOT,str(user))
		if not os.path.isdir(self._root):
			os.makedirs(self._root)
		self._path = os.path.join(self._root,path)
		self._setBread(str(user),path)
		
	def list(self):
		if os.path.isdir(self._path):
			dir_list = os.listdir(self._path)
			result = []
			for p in dir_list:
				full = os.path.join(self._path,p)
				
				item={"name":p,"isfile":os.path.isfile(full),
					"editable":self._editable(full),
					"path":full[len(self._root)+1:],
					"size":self._getSize(full)}
				result.append(item)

			return {"bread":self._bread,"list":result}
		return None

	def download(self):
		if os.path.isfile(self._path):
			name = os.path.basename(self._path)
			return {"name":name,"stream":self._file_iterator(self._path)}
		return None
	def mkdir(self,name):
		path = os.path.join(self._path,name)
		if not os.path.isdir(path):
			os.makedirs(path)
			return 204
		return 403

	def fileUpload(self,filename,file):
		# upload_dir = getUploadDir(path)
		if not os.path.exists(self._path):
		    os.makedirs(self._path)
		filename =os.path.join(self._path,filename)
		
		if os.path.exists(filename):
		    return 403
		with open(filename,'wb+') as destination:
		    for chunk in file.chunks():
		        destination.write(chunk)
		    destination.close()
		        
		return 204
	def rename(self,name):
		if os.path.exists(self._path) and self._editable(self._path):
			name = os.path.join(os.path.dirname(self._path),name)
			# print 
			os.rename(self._path,name)
			return 204
		return 403
	def remove(self):
		if os.path.exists(self._path) and self._editable(self._path):
			if os.path.isfile(self._path):
				os.remove(self._path)
			elif os.path.isdir(self._path):
				shutil.rmtree(self._path)
			return 204
		return 403

	def unzip(self):
		basename=os.path.basename(self._path)
		splits = os.path.splitext(basename)
		zipdirname = os.path.join(os.path.dirname(self._path),splits[0])
		if splits[1] == ".zip" and os.path.exists(self._path) and not os.path.isdir(zipdirname):
		
			zfile = zipfile.ZipFile(self._path,'r')
			for filename in zfile.namelist():
				
				if not filename.endswith('/'):
					f = os.path.join(zipdirname,filename)
					dirname = os.path.dirname(f)
					if not os.path.exists(dirname):
						os.makedirs(dirname)
					data = zfile.read(filename)
					file = open(f, 'w+b')
					file.write(data)
					file.close()

			return 204
		return 404

	def getPath(self):
		if os.path.exists(self._path):
			return self._path
		return None
	def _getSize(self,path):
		size = 0
		if os.path.isdir(path):
			for root , dirs, files in os.walk(path, True):
				size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
		elif os.path.isfile(path):
			size=os.path.getsize(path)
		return size

	def _file_iterator(self,path,chunk_size=512):
		with open(path) as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break
	def _setBread(self,root,path):
		tmp = ""
		bread=[{"name":root,"path":tmp}]
		paths = path.split("/")
		for p in paths:
			if p:
				tmp=os.path.join(tmp,p);
				item = {"name":p,"path":tmp}
				bread.append(item)
		self._bread = bread

	def _editable(self,path):
		v = Volume.objects.filter(path__contains=path).count()
		# print v
		return (v is 0)
	# def getBread(self):
		# return self._bread

	
