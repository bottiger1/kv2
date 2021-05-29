'''
BSD 2-Clause License

Copyright (c) 2021, bottiger1
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import uuid
import pprint
import parsimonious

grammar = parsimonious.grammar.Grammar(
r'''
main 	    = header? object+
header 		= whitespace ~r'<\!--.*-->'
object	    = quoted "{" whitespace value* whitespace "}" whitespace

value 					= value_element_array / value_string_array / value_typed
value_element_array 	= quoted '"element_array"' array
value_string_array		= quoted '"string_array"' string_array
value_typed				= quoted quoted quoted
value_element 			= quoted quoted

array       			= whitespace "[" whitespace array_element* whitespace "]"
array_element   		= (value_element / object) ","?

string_array			= whitespace "[" whitespace string_array_element* whitespace "]"
string_array_element 	= quoted ","? whitespace

quoted    				= whitespace '"' ~r'(\\"|[^"])*' '"' whitespace
whitespace 				= ~'\s*'
''')

def unescape_string(s: str):
	return s.encode('utf8').decode('unicode_escape')

def escape_string(s: str):
	return s.encode('unicode_escape').decode('utf8')

def strip_quotes(s: str):
	return unescape_string(s.strip().rstrip(',')[1:-1])

class NodeList(list):
	def __init__(self, args=None, node=None):
		if args is None:
			super().__init__()
		else:
			super().__init__(args)

		self.node = node

printer = pprint.PrettyPrinter(indent=2)
class KV2:
	def __init__(self, s: str):
		g = grammar.parse(s)
		self.header = None
		self.base = NodeList()
		self.parse(g, self.base)

	def __repr__(self):
		return 'KV2\n %s' % printer.pformat(self.base)

	def __str__(self):
		return self.serialize()

	def parse(self, g: parsimonious.nodes.Node, entries: NodeList):
		name = g.expr_name
	
		if name == 'header':
			self.header = g.text.strip()
		elif name == 'object':
			object_name = strip_quotes(g.children[0].text)
			obj = NodeList([object_name, NodeList()])
			obj.node = name
			for child in g.children[1:]:
				self.parse(child, obj[1])
			entries.append(obj)
		elif name == 'value_typed':
			obj = NodeList([strip_quotes(g.children[0].text), strip_quotes(g.children[1].text), strip_quotes(g.children[2].text)])
			obj.node = name
			entries.append(obj)
		elif name == 'value_element':
			obj = NodeList([strip_quotes(g.children[0].text), strip_quotes(g.children[1].text)])
			obj.node = name
			entries.append(obj)
		elif name == 'value_element_array':
			obj = NodeList([strip_quotes(g.children[0].text), strip_quotes(g.children[1].text), NodeList()])
			obj.node = name
			self.parse(g.children[2], obj[2])
			entries.append(obj)
		elif name == 'value_string_array':
			obj = NodeList([strip_quotes(g.children[0].text), strip_quotes(g.children[1].text), NodeList()])
			obj.node = name
			self.parse(g.children[2], obj[2])
			entries.append(obj)
		elif name == 'string_array_element':
			entries.append(strip_quotes(g.text))
		else:
			for child in g.children:
				self.parse(child, entries)

	def serialize(self):
		output = []
		if self.header:
			output.append(self.header)

		output.extend(self.serialize_recurse(self.base, self.base))
		return '\n'.join(output)

	def append_child_output(self, output: list, child_output: list):
		spacing = '  '
		for line in child_output:
			output.append('%s%s' % (spacing, line))

	def serialize_recurse(self, node: NodeList, parent: NodeList) -> list:
		output = []
		comma_node = parent.node == 'value_element_array' 

		for i,e in enumerate(node):
			if e.node == 'object':
				output.append('"%s"' % escape_string(e[0]) )
				output.append('{')
				child_output = self.serialize_recurse(e[1], e)
				self.append_child_output(output, child_output)
				output.append('}')
			elif e.node == 'value_typed':
				output.append('"%s" "%s" "%s"' % (escape_string(e[0]), escape_string(e[1]), escape_string(e[2]) ))
			elif e.node == 'value_element':
				output.append('"%s" "%s"' % (escape_string(e[0]), escape_string(e[1]) ))
			elif e.node == 'value_element_array':
				output.append('"%s" "%s"' % (escape_string(e[0]), escape_string(e[1]) ))
				output.append('[')
				child_output = self.serialize_recurse(e[2], e)
				self.append_child_output(output, child_output)
				output.append(']')
			elif e.node == 'value_string_array':
				output.append('"%s" "%s"' % (escape_string(e[0]), escape_string(e[1]) ))
				output.append('[')
				for j,string in enumerate(e[2]):
					comma = ''
					if j < len(e[2]) - 1:
						comma = ','
					output.append('  "%s"%s' % (escape_string(string), comma))
				output.append(']')

			if comma_node and i < len(node) - 1 and len(output) > 0:
				output[-1] += ','
	
		return output

def get_kv2_value(l: list, name: str):
	for e in l:
		if e[0] == name:
			return e[2]

def set_kv2_value(l: list, name: str, value: str) -> bool:
	for e in l:
		if e[0] == name:
			e[2] = value
			return True
	return False

def test():
	d = KV2(example)
	return d