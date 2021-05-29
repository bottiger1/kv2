import kv2
import pprint

example_input = r'''
<!-- dmx encoding keyvalues2 1 format dmx 18 -->
"DmElement"
{
	"id" "elementid" "d1d1ffff-18a8-4fa7-ac0c-b436a32e5004"
	"name" "string" "untitled"
	"testarray" "element_array" 
	[
		"element" "6a1cd593-a1bf-48d2-843a-cc7c8f3ae05e",
		"element" "e6f90bc8-3b4c-4ea2-b863-c5ccdfef5954",
		"element" "bf783c0a-f0ac-4255-abc3-78e1a958296d",
		"element" "84231e1d-1315-46ad-9878-540757b6dfe9",
		"nested1"
		{
			"id" "elementid" "e1dc7c15-75a9-43fa-8f27-20d5ce8993fb"
			"name" "string" "asdf1"
			"functionName" "string" "asdf2"
		},
		"nested2"
		{
			"id" "elementid" "e1dc7c15-75a9-43fa-8f27-20d5ce8993fb"
			"name" "string" "asdf3"
			"functionName" "string" "asdf4"
		}
	]
	"blah" "element_array"
	[
	]
	"stringtest" "string_array"
	[
		"foo",
		"bar"
	]
}

"DmElement2"
{
	"id" "elementid" "d1d1ffff-18a8-4fa7-ac0c-b436a32e5004"
	"name" "string" "untitled"
	"testarray" "element_array" 
	[
		"element" "6a1cd593-a1bf-48d2-843a-cc7c8f3ae05e",
		"element" "e6f90bc8-3b4c-4ea2-b863-c5ccdfef5954",
		"nested1"
		{
			"id" "elementid" "e1dc7c15-75a9-43fa-8f27-20d5ce8993fb"
			"name" "string" "asdf1"
			"functionName" "string" "asdf2"
		},
		"nested2"
		{
			"id" "elementid" "e1dc7c15-75a9-43fa-8f27-20d5ce8993fb"
			"name" "string" "asdf3"
			"functionName" "string" "asdf4"
		}
	]
	"blah" "element_array"
	[
	]
	"stringtest" "string_array"
	[
		"foo",
		"bar"
	]
}

'''

# parse a string
input_parsed = kv2.KV2(example_input)

# show the array based representation of the data
# the data is stored as a list of lists in the "base" member
# each list has the member "node" which is a string representing what type of node it is

print(input_parsed.base)

'''
KV2
 [ [ 'DmElement',
    [ ['id', 'elementid', 'd1d1ffff-18a8-4fa7-ac0c-b436a32e5004'],
      ['name', 'string', 'untitled'],
      [ 'testarray',
        'element_array',
        [ ['element', '6a1cd593-a1bf-48d2-843a-cc7c8f3ae05e'],
          ['element', 'e6f90bc8-3b4c-4ea2-b863-c5ccdfef5954'],
          ['element', 'bf783c0a-f0ac-4255-abc3-78e1a958296d'],
          ['element', '84231e1d-1315-46ad-9878-540757b6dfe9'],
          [ 'nested1',
            [ ['id', 'elementid', 'e1dc7c15-75a9-43fa-8f27-20d5ce8993fb'],
              ['name', 'string', 'asdf1'],
              ['functionName', 'string', 'asdf2']]],
          [ 'nested2',
            [ ['id', 'elementid', 'e1dc7c15-75a9-43fa-8f27-20d5ce8993fb'],
              ['name', 'string', 'asdf3'],
              ['functionName', 'string', 'asdf4']]]]],
      ['blah', 'element_array', []],
      ['stringtest', 'string_array', ['foo', 'bar']],
      ['n', 'int', 'v']]],
  [ 'DmElement2',
    [ ['id', 'elementid', 'd1d1ffff-18a8-4fa7-ac0c-b436a32e5004'],
      ['name', 'string', 'untitled'],
      [ 'testarray',
        'element_array',
        [ ['element', '6a1cd593-a1bf-48d2-843a-cc7c8f3ae05e'],
          ['element', 'e6f90bc8-3b4c-4ea2-b863-c5ccdfef5954'],
          [ 'nested1',
            [ ['id', 'elementid', 'e1dc7c15-75a9-43fa-8f27-20d5ce8993fb'],
              ['name', 'string', 'asdf1'],
              ['functionName', 'string', 'asdf2']]],
          [ 'nested2',
            [ ['id', 'elementid', 'e1dc7c15-75a9-43fa-8f27-20d5ce8993fb'],
              ['name', 'string', 'asdf3'],
              ['functionName', 'string', 'asdf4']]]]],
      ['blah', 'element_array', []],
      ['stringtest', 'string_array', ['foo', 'bar']]]]]
'''

# add something
# label it with the proper node type or it can't be serialized to string

new_item1 = kv2.NodeList(["n", "int", "v"], 'value_typed')
input_parsed.base[0][1].append(new_item1)

# to add something complicated it is better to do it through a string 
# and pass it to the parser

complicated = '''
"CustomObject"
{
	"a" "b" "c"
	"blah" "element_array"
	[
		"element" "asdffdsa"
		"foo"
		{
			"bar" "baz" "box"
		}
	]	
}
'''
complicated_array_form = kv2.KV2(complicated).base[0]
input_parsed.base.append(complicated_array_form)

# delete things how you would normally delete from a regular python list
input_parsed.base.pop()

# serialize back to a string
string_form = str(input_parsed)
#print(string_form)