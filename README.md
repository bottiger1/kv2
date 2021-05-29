# kv2
Python Valve KeyValues2 Parser

By Bottiger from skial.com

## Summary

This is a Valve KeyValues2 parser written in Python. 

With this library you can turn a KeyValues 2 string into a list of lists which can be modified. Then
you can turn it back to a string.

Speed and ease of use may not be the best, but there are very few people in the world that would 
find it useful to parse Valve KV2 outside of Valve. If you are one of them, you probably have 
the ability to improve this. Pull requests are welcome.

I will not be using this much myself, that is why this library is not too optimized or friendly to use.
It didn't make sense for me to spend more time on this than I would save. But I was surprised there 
wasn't one available already when I was looking for one.

If you want a rough estimate of how fast this library is, parsing a 600 kb file takes around 2 seconds 
and around 200 mb RAM on my computer.

## How to Use

Put kv2.py in your project folder and import it. You will need to install the parsimonious lirary 
with **pip install parsimonious**.

See test.py for example usage. It is fully commented.

## Warning

C style comments are not supported except for a multiline one at the top. Unquoted values are not supported.
I have never seen a KeyValues2 sample with unquoted values.

There is no formal or informal reference of the KV2 format anywhere. Syntax is based on the few samples 
I have access to, so the parsing may not be 100% correct. But I have used this library to parse 
several megabytes worth without any issues.