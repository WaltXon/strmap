
test = ['NE4', 'SE4', 'NENE', 'S2S2', 'S2',
	'N2S2+W2NW4', 'ALL','SW4NE4','S2NW4+SW4','E2', 'W2W2']


def ParseLegalPart(part):
	if part == 'ALL':
		print 'Unmodified Section'
		return(["ALL"])
	else:
		partstr = ''
		parts = []
		for char in part:
			if partstr == '':
				if char in ('E','W'):
					parts.append(char)
				elif char in ('N','S'):
					partstr += char
			else:
				if char in ('N', 'S'):
					parts.append(partstr)
					partstr = char
				elif char in ('E', 'W'):
					partstr += char
					parts.append(partstr)
					partstr = ''

		if partstr != '':
			parts.append(partstr)
	return parts


def ParseLegal(legal):
	quarters = ['NE', 'SE', 'NW', 'SW']
	halves = ['N', 'S', 'E', 'W']
	numeric = ['2','4']
	section = 640.0 #get area of shape in actual script

	#remove the numers from the string
	print 'Original == {0}'.format(legal)
	legal = legal.replace('2', '')
	legal = legal.replace('4', '')
	# print '-- {0}'.format(legal)

	partlist = legal.split("+")
	print("partlist = {}".format(partlist))

	legallist = []
	for part in partlist:
		print("--part = {0}".format(part))
		legallist.append(ParseLegalPart(part))

	return legallist

for legal in test:
	print("""
	      =================
	      """)
	print("ParsedSTR = {0}".format(ParseLegal(legal)))
