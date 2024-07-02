import os
from dotenv import load_dotenv
from promptflow.tracing import trace
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
@trace
def flow(data: dict, endpoint_name: str, api_key_name: str) -> str:
	body = str.encode(json.dumps(data))

	load_dotenv()
	# url = os.getenv("PHI_3_MINI_4K_ENDPOINT")
	# api_key = os.getenv("PHI_3_MINI_4K_API_KEY")
	url = os.getenv(endpoint_name)
	api_key = os.getenv(api_key_name)
	print("endpoint and api key loaded...")
	
	headers = {"Content-Type": "application/json", "Authorization" :('Bearer '+ api_key)}
	result = json.loads(requestData(url, body, headers).decode('utf-8'))['choices'][0]['message']['content']

	return result

# makes a call to an azure endpoint.
# input: 
# 	filename where the prompt is written
#	prompt_text: product description.
#	endpoint_name: name of endpoint in the .env file
# 	api_key_name: name of api_key in the .env file
# output:
#	returns a string output
# calls another function 
def makePromptCall(file_name: str, prompt_text: str, endpoint_name: str, api_key_name: str) -> str:
	prompt = open(file_name).read()
	messages=[
		{"role": "user", "content": (prompt + prompt_text)},
		# {"role": "user", "content": product_description}
	]
	
	data =  {
		"messages": messages,
		"max_tokens": 3000,
		"temperature": 0.2,
		"top_p": 1
	}

	result = flow(data, endpoint_name, api_key_name)
	return result



if __name__ == "__main__":
	# firstPrompt = open('./prompt1.txt').read()
	prompt = open('./prompt2.txt').read()
	product_description="Bluetooth Speaker"
	# product_description="An elastomeric half mask respirator tight-fitting facepiece"

	combined_prompt_output = makePromptCall(file_name='./prompt2.txt', 
										 prompt_text=product_description, 
										 endpoint_name="PHI_3_MEDIUM_128K_ENDPOINT", 
										 api_key_name="PHI_3_MEDIUM_128K_API_KEY")
	print(f"\n\n{'~'*10} Combined Prompt Output {'~'*10}")
	print(combined_prompt_output)
	combined_file = open('./combinedOutput.txt', 'w+')
	combined_file.write(combined_prompt_output)
	combined_file.close()

	componentsJson = makePromptCall(file_name='./getComponentPrompt.txt', 
								 prompt_text=product_description, 
								 endpoint_name="PHI_3_MEDIUM_128K_ENDPOINT", 
								 api_key_name="PHI_3_MEDIUM_128K_API_KEY")
	result = makePromptCall(file_name='./getManufacturingProcesses.txt', 
						 prompt_text=componentsJson, 
						 endpoint_name="PHI_3_MINI_128K_ENDPOINT", 
						 api_key_name="PHI_3_MINI_128K_API_KEY")

	# result_dict = json.loads(result)
	print(f"\n\n{'~'*10} Separate Prompt Output {'~'*10}")
	print(result)
	# separate_file = open('./separateOutput4K.txt', 'w+')
	separate_file = open('./separateOutput128K.txt', 'w+')
	separate_file.write(componentsJson + result)
	# separate_file.write(result)
	separate_file.close()
	
	print("system.close()")


"""
Sample Output using the first prompt
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