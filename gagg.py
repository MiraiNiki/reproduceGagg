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
		#demensions_x
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

node1 = []
node2 = []
edge = []
#measure is hash structure
measure1 = []
measure2 = []
measureEdge = []

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
		if d1 not in node1:
			node1.append(d1)
		d2 = {"m": data["member2"]['value'], "p": data["position2"]['value']}
		if d2 not in node2:
			node2.append(d2)		
		#relation
		rel = {"from": data["author1"]['value'], "to": data["author2"]['value']}
		if rel not in edge:
			edge.append(rel)
		#measure
		m1 = {"index":node1.index(d1), "m":data['paper1']['value']}
		if m1 not in measure1:
			measure1.append(m1)
		m2 = {"index":node2.index(d2), "m":data['paper2']['value']}
		if m2 not in measure2:
			measure2.append(m2)
		mrel = {"index":edge.index(rel), "o":data['paper1']['value']}
		if mrel not in edge:
			measureEdge.append(mrel)

def printResult(dicList):
	for dic in dicList:
		for k, v in dic.items():
			print(k, v, end=" , ")
		print()

#use your endpoint at local
url = 'http://localhost:3030/paper_gagg/query'
#get together ??
response = requestResponseToFusekiServer(url, query)
if response['results'] != []:
	getResultArray(response)
	print("node1 :")
	printResult(node1)
	print("node2 :")
	printResult(node2)
	print("edge :")
	printResult(edge)
	print("measure1 :")
	printResult(measure1)
	print("measure2 :")
	printResult(measure2)
	print("measureEdge :")
	printResult(measureEdge)


