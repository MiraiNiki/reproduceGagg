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
		#for i in range(len(data)):
		#	print(list(data)[i] + ":" + data[list(data)[i]]['value'], end=" , ")
		if data["author1"]['value'] not in node1:
			node1.append(data["author1"]['value'])
		elif data["author2"]['value'] not in node2:
			node2.append(data["author2"]['value'])
		str = data["author1"]['value'] + " :cite " + data["author2"]['value']
		if str not in edge:
			edge.append(str)
		measure1[data["author1"]['value']].append(data["paper1"]['value'])
		measure2[data["author2"]['value']].append(data["paper2"]['value'])
		measureEdge[].append(data["paper1"]['value'])
		#print()

	for r in node1:
		print(r,end=" , ")
	print()
	for r in node2:
		print(r,end=" , ")
	print()
	for r in edge:
		print(r,end=" , ")
	print()
	for r in measure1:
		print(r,end=" , ")
	print()
	for r in measure2:
		print(r,end=" , ")
	print()
	for r in measureEdge:
		print(r,end=" , ")
	print()

#use your endpoint at local
url = 'http://localhost:3030/paper_gagg/query'
#get together ??
response = requestResponseToFusekiServer(url, query)
if response['results'] != []:
	getResultArray(response)
