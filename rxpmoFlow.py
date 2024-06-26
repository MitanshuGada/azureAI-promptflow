import os
from dotenv import load_dotenv
# from promptflow.tracing import trace
import urllib.request
import json
# from promptflow.core import tool

# Function to make the api call using the headers and body and url
def requestData(url: str, body: str, headers: dict):
	req = urllib.request.Request(url, body, headers)

	try:
		print("making the api call...")
		response = urllib.request.urlopen(req)
		print("response received...")
		result = response.read()
		return result
	except urllib.error.HTTPError as error:
		print("The request failed with status code: " + str(error.code))

		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())
		print(error.read().decode("utf8", 'ignore'))

# returns a string 
# @trace
def flow(data: dict) -> str:
	body = str.encode(json.dumps(data))

	load_dotenv()
	# url = os.getenv("PHI_3_MINI_4K_ENDPOINT")
	# api_key = os.getenv("PHI_3_MINI_4K_API_KEY")
	url = os.getenv("PHI_3_MEDIUM_4K_ENDPOINT")
	api_key = os.getenv("PHI_3_MEDIUM_4K_API_KEY")
	print("endpoint and api key loaded...")
	
	headers = {"Content-Type": "application/json", "Authorization" :('Bearer '+ api_key)}
	result = json.loads(requestData(url, body, headers).decode('utf-8'))['choices'][0]['message']['content']

	return result


if __name__ == "__main__":
	background = """
	You are a detailed and knowledgeable manufacturing assistant. Your task is to generate a comprehensive bill of materials (BOM) in a hierarchical assembly tree and list all possible manufacturing processes that could be used for each component of a given product. Each entry in the BOM should include the component name, quantity, material, and a list of possible manufacturing processes. The output should be formatted as a JSON object.

	If the query is not related to providing a BOM or manufacturing process for a product, respond with: "I can only provide information about the bill of materials and manufacturing processes for products."

	Additionally, if the query involves products related to adult entertainment, self-harm, violence, or any other unsafe or inappropriate context, respond with: "I cannot provide information on this topic."

	If an image of a product is provided, analyze the image to identify the components, then generate the BOM and manufacturing processes as described.

	Ensure the information is organized, accurate, and clearly presented in the following JSON format:
	{
		"components": [
			{
				"component_name": "string",
				"quantity": "integer",
				"material": "string",
				"manufacturing_processes": [
					{
						"type": "string"
					}
				],
				"subcomponents": [
					{
						"component_name": "string",
						"quantity": "integer",
						"material": "string",
						"manufacturing_processes": [
							{
							"type": "string"
							}
						]
					}
				]
			}
		]
	}
	Here is a sample list of manufacturing processes to include:

	Stereolithography (SL)
	Multi-Jet Modelling (MJM)
	Fused Deposition Modeling (FDM)
	Selective Laser Sintering (SLS)
	Three-Dimensional Printing (3DP)
	Electron-beam Melting (EBM)
	Laminated-object Manufacturing (LOM)
	Laser-Engineered Net Shaping (LENS)
	Extrusion
	Plastic Injection Molding (PIM)
	Structural Foam Molding
	Blow Molding
	Rotational Molding
	Thermoforming
	Compression Molding (CM)
	Transfer Molding
	Casting
	Please provide the bill of materials and manufacturing processes for the specified product in the above JSON format.

	If the query is unrelated, respond with: "I can only provide information about the bill of materials and manufacturing processes for products."

	If the query involves unsafe or inappropriate content, respond with: "I cannot provide information on this topic."
	Name of the Product: 
	"""
	product_description= "An elastomeric half mask respirator"
	messages=[
		{"role": "user", "content": (background + product_description)},
		# {"role": "assistant", "content": "Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:\n\n1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.\n2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.\n3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.\n\nThese are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world."},
		# {"role": "user", "content": product_description}
	]
	
	data =  {
		"messages": messages,
		"max_tokens": 3000,
		"temperature": 0.2,
		"top_p": 1
	}

	result = flow(data)
	# result_dict = json.loads(result)

	print(result)


"""
Sample Output
{
	"components": [
		{
			"component_name": "Elastomeric Half Mask Respirator",
			"quantity": 1,
			"material": "Silicone",
			"manufacturing_processes": [
				{
					"type": "Extrusion"
				},
				{
					"type": "Thermoforming"
				},
				{
					"type": "Casting"
				}
			],
			"subcomponents": [
				{
					"component_name": "Filter Cartridge",
					"quantity": 1,
					"material": "Polypropylene",
					"manufacturing_processes": [
						{
							"type": "Extrusion"
						},
						{
							"type": "Structural Foam Molding"
						}
					]
				},
				{
					"component_name": "Exhalation Valve",
					"quantity": 1,
					"material": "Silicone",
					"manufacturing_processes": [
						{
							"type": "Molding"
						}
					]
				},
				{
					"component_name": "Head Harness",
					"quantity": 1,
					"material": "Nylon",
					"manufacturing_processes": [
						{
							"type": "Weaving"
						},
						{
							"type": "Knitting"
						}
					]
				},
				{
					"component_name": "Eye Cup",
					"quantity": 2,
					"material": "Silicone",
					"manufacturing_processes": [
						{
							"type": "Extrusion"
						},
						{
							"type": "Thermoforming"
						}
					]
				}
			]
		}
	]
}
"""