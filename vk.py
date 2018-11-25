import json


def parse(s):
	spl = s.split('<!>')
	print spl
	error = spl[4]
	if int(error) != 0:
		raise Exception(spl[5])
	base = spl[5]
	if base[0] == '<':
		l = base.find('>')
		type = base[2:l]
		value = base[l+1:]
#		print type
		if type == 'json':
			return json.loads(value)
		if type == 'bool':
			return value == '1'
	return base
