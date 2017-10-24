import requests

query = ("PREFIX : <http://example.org/#> \n"
 		+ "PREFIX author: <http://mirainiki/author/> \n"
 		+ "PREFIX paper: <http://mirainiki/paper/> \n"
 		+ "PREFIX ref: <http://mirainiki/ref/> \n"

		+ "SELECT ?paper1 ?paper2 ?author1 ?author2 ?member1 ?position1 ?member2 ?position2\n"
		+ "WHERE {\n"
  		#relation
		+ " ?paper1 paper:creator ?author1 .\n"
		+ " ?paper2 paper:creator ?author2 .\n"
		+ " ?paper1 paper:references ?refs .\n"
		+ " ?refs ref:ref ?paper2 .\n"
		#dimensions_x
		+ " ?author1 author:member ?member1 ;\n"
		+ "  author:position ?position1 .\n"
		#dimensions_y
		+ " ?author2 author:member ?member2 ;\n"
		+ "  author:position ?position2 .\n"
		#measures_x
		+ " ?paper1 paper:creator ?author1 .\n"
		#measures_y
		+ " ?paper2 paper:creator ?author2 .\n"
		+ "}")

dimension1 = []
dimension2 = []
edge = []
measure1 = []
measure2 = []
measureEdge = []
node = []
measure = []

#request response to fuseki server
#input: url, query
def requestResponseToFusekiServer(url, query):
	response = requests.post(url, data={'query': query})
	return response.json()

#get result array
#return s p o
def getResultArray(response):
	responseSparqlArray = response['results']['bindings']
	for data in responseSparqlArray:
		#dimension
		d1 = {"m": data["member1"]['value'], "p": data["position1"]['value']}
		if d1 not in dimension1:
			dimension1.append(d1)
			if d1 not in node:
				node.append(d1)
		d2 = {"m": data["member2"]['value'], "p": data["position2"]['value']}
		if d2 not in dimension2:
			dimension2.append(d2)
			if d2 not in node:
				node.append(d2)		
		#relation
		rel = {"from": node.index(d1), "to": node.index(d2)}
		if rel not in edge:
			edge.append(rel)
		#measure
		m1 = {"index":node.index(d1), "m":data['paper1']['value']}
		if m1 not in measure1:
			measure1.append(m1)
			if m1 not in measure:
				measure.append(m1)
		m2 = {"index":node.index(d2), "m":data['paper2']['value']}
		if m2 not in measure2:
			measure2.append(m2)
			if m2 not in measure:
				measure.append(m2)
		mrel = {"index":edge.index(rel), "o":data['paper1']['value']}
		measureEdge.append(mrel)

def printResult(dicList):
	for dic in dicList:
		for k, v in dic.items():
			print(k, v, end=" , ")
		print()

def testGroupedGraph():
	print("node :")
	node.sort(key=lambda x:x['m'])
	printResult(node)
	print("measure :")
	measure.sort(key=lambda x:x['index'])
	printResult(measure)
	edge.sort(key=lambda x:x['from'])
	print("edge :")
	printResult(edge)
	measureEdge.sort(key=lambda x:x['index'])
	print("measureEdge :")
	printResult(measureEdge)
	#print("----------------------------------------------------------------------------")
	#print("dimension1 :")
	#printResult(dimension1)
	#print("dimension2 :")
	#printResult(dimension2)
	#print("measure1 :")
	#printResult(measure1)
	#print("measure2 :")
	#printResult(measure2)

#use your endpoint at local
url = 'http://localhost:3030/paper_gagg/query'
#get together ??
response = requestResponseToFusekiServer(url, query)
if response['results'] != []:
	getResultArray(response)
	testGroupedGraph()

