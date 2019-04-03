import requests,json
import jsonify
import re
import datetime
import flask


url = "http://0.0.0.0:5000/outbreaktable/show/"
headers = {'Content-Type': 'application/json'}

def testCase1():
	# test case where input is correct and there is a possible output
	url2 = "2018-12-19T05:45:10/2019-12-19T05:45:10/California/salmonella"
	r = requests.get(url+url2 , headers=headers)
	print("Test 1: Base test when input is correct and output is also present")
	assert(r.status_code == 200)
	print("Test 1: Pass")

def testCase2():
	url2 = "2018-12-19T05:45:10/2019-12-19T05:45:10/Iowa/salmonella"
	r = requests.get(url+url2 , headers=headers)
	print("Test 2: Test when input is correct and output is not present")
	assert(r.status_code == 404)
	print("Test 2: Pass")

def testCase3():
	url2 = "2018-12-19T05:45:10/2019-12-19T45:10/Iowa/salmonella"
	r = requests.get(url+url2 , headers=headers)
	print("Test 3: Test when input is incorrect (date) ")
	assert(r.status_code == 400)
	print("Test 3: Pass")

def testCase4():
	url2 = "2018-12-19T05:45:10/2019-12-19T05:45:10/Chicago/salmonella"
	r = requests.get(url+url2 , headers=headers)
	print("Test 4: Test when input is incorrect (location) ")
	assert(r.status_code == 400)
	print("Test 4: Pass")

def testCase5():
	url2 = "2018-12-19T05:45:10/2019-12-19T05:45:10"
	r = requests.get(url+url2 , headers=headers)
	print("Test 5: Test when no location or keywords ")
	assert(r.status_code == 200)
	print("Test 5: Pass")

def testCase6():
	url2 = "2018-12-19T05:45:10/2019-12-19T05:45:10/Chicago/salmon"
	r = requests.get(url+url2 , headers=headers)
	print("Test 6: Test when input is incorrect (keywords) ")
	assert(r.status_code == 400)
	print("Test 6: Pass")

def testCase7():
	url2 = "2018-12-19T05:45:10/2019-12-19T05:45:10//salmonella"
	r = requests.get(url+url2 , headers=headers)
	print("Test 7: Test when no location")
	assert(r.status_code == 200)
	print("Test 7: Pass")

def testCase8():
	url2 = "2018-12-19T05:45:10/2019-12-19T05:45:10/Minnesota"
	r = requests.get(url+url2 , headers=headers)
	print("Test 8: Test when no keywords")
	assert(r.status_code == 200)
	print("Test 8: Pass")



testCase1()
testCase2()
testCase3()
testCase4()
testCase5()
testCase6()
testCase7()
testCase8()
