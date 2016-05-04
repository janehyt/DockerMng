import os
from mysite import settings

# class FileService(object):

def fileUpload(filename,file,path):
	upload_dir = os.path.join(settings.UPLOAD_ROOT,path)
	if not os.path.exists(upload_dir):
	    os.makedirs(upload_dir)
	filename = upload_dir+"/"+filename
	if os.path.exists(filename):
	    return 403

	with open(filename,'wb+') as destination:
	    for chunk in file.chunks():
	        destination.write(chunk)
	        # ...
	        # do some stuff with uploaded file
	        # ...
	return 204

def fileList(path):
	upload_dir = os.path.join(settings.UPLOAD_ROOT,path)
	if os.path.exists(upload_dir) and os.path.isdir(upload_dir):
		dir_list = os.listdir(upload_dir)
		result = []
		for p in dir_list:
			full = os.path.join(upload_dir,p)
			if os.path.isfile(full):
				item = {"name":p,"size":os.path.getsize(full)}
				result.append(item)
		return result
	return None