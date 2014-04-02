
test = ['NE4', 'SE4', 'NENE', 'S2S2', 'S2', 
	'N2S2+W2NW4', 'ALL','SW4NE4','S2NW4+SW4','E2', 'W2W2']



def parseSTR(legal):
	quarters = ['NE', 'SE', 'NW', 'SW']
	halves = ['N', 'S', 'E', 'W']
	numeric = ['2','4']
	section = 640.0 #get area of shape in actual script

	print '== {0}'.format(legal)
	legal = legal.replace('2', '')
	legal = legal.replace('4', '')
	print '-- {0}'.format(legal)
	parts = []
	nparts = []

	if legal == 'ALL':
		print 'Unmodified Section = {0}'.format(section)
		parts.append("ALL")
		nparts.append(parts)
	else:
		charidx = 0
		partidx = 0
		part = ''
		
		for char in legal:
			if char == '+':
				print 'Multipart Description'
				charidx = 0
				partidx += 1
			
			if charidx == 0:
				if char in ('E','W'):
					part += char
					print '{0} Half'.format(part)
					parts.append(part)
					nparts.append(parts)
					part = ''
					parts = []
				elif char in ('N','S'):
					part += char
					charidx = 1
			elif charidx > 0:
				if char in ('E', 'W'):
					part += char
					parts.append(part)
					part = ''
					charidx = 0
				else:
					parts.append(part)
					part = ''
					charidx = 0

	print parts
	print nparts




for legal in test:
	parseSTR(legal)