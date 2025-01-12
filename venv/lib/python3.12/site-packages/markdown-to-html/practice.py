"""
Generates HTML from markdown

Usage:
	practice.py <filepath>
"""


import docopt
import os
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import Template

def generator(lines):
	"""
	>>> lines = ['Question: 1', 'Option: 1', 'Question: 2', 'Option: 3', "Question: 3", "Option: 4"]
	>>> questions = list(generator(lines))
	>>> len(questions)
	3
	>>> len(questions[0])
	2
	>>> len(questions[1])
	2
	"""
	lst = []
	for line in lines:
		if line.startswith('Question:'):
			if lst:
				yield lst
			lst = [line.replace('Question:', '', 1)]
		elif line.strip():
			lst.append(line.replace('Option:', '', 1))
	if lst:
		yield lst

def converter(path, template):
	questions = generator(open(path).readlines())
	outpath = os.path.join('outputs', path.replace('.md', '.html'))
	f = open(outpath, 'w')
	f.write(template.render(questions = questions))
	f.close()
	print(' * File outputted at', outpath)

def main():
	arguments = docopt.docopt(__doc__, version='Practice 1.0')
	env = Environment(loader=PackageLoader('practice', 'templates'))	
	template = env.get_template('index.html')
	path = arguments['<filepath>']
	if os.path.isdir(path):
		os.makedirs(os.path.join('outputs', path), exist_ok=True)
		for filename in os.listdir(path):
			if filename.endswith('.md'):
				filepath = os.path.join(path, filename)
				converter(filepath, template)		
	else:
		converter(path, template)

if __name__ == '__main__':
	main()