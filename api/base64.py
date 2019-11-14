import base64
import uuid
from django.core.files.base import ContentFile

def decode_base64(encoding):
	extension = ""
	result = {}
	if "data:" in encoding and ";base64," in encoding:
		extension, encoding = encoding.split(";base64,")
	try:
		result = base64.standard_b64decode(encoding)
	except TypeError:
		print("error:", TypeError)
	if extension:
		trash, extension = extension.split("/")
	if extension != "png" or extension != "jpg" or extension !="jpeg":
		extension = "jpeg"
	name = str(uuid.uuid4())[:12]
	file_name = "%s.%s" % (name, extension)
	data = ContentFile(result, name=file_name)
	return data