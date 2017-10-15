import requests

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
		print(data['s']['value'] + " -> " + data['p']['value'] + " -> " + data['o']['value'])




#use your endpoint at local
url = 'http://localhost:3030/paper_gagg/query'
query = 'select * {?s ?p ?o}'
#get together ??
response = requestResponseToFusekiServer(url, query)
getResultArray(response)