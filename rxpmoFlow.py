import os
from dotenv import load_dotenv
from promptflow.tracing import trace
import urllib.request
import json
import time
# from promptflow.core import tool

# Function to make the api call using the headers and body and url
def requestData(url: str, body: str, headers: dict):
	req = urllib.request.Request(url, body, headers)

	try:
		# print("making the api call...")
		response = urllib.request.urlopen(req)
		# print("response received...")
		result = response.read()
		return result
	except urllib.error.HTTPError as error:
		print("The request failed with status code: " + str(error.code))

		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())
		print(error.read().decode("utf8", 'ignore'))


# returns a string 
@trace
def flow(data: dict, endpointName: str, apiKeyName: str) -> str:
	body = str.encode(json.dumps(data))

	load_dotenv()
	# url = os.getenv("PHI_3_MINI_4K_ENDPOINT")
	# apiKey = os.getenv("PHI_3_MINI_4K_API_KEY")
	url = os.getenv(endpointName)
	apiKey = os.getenv(apiKeyName)
	# print("endpoint and api key loaded...")
	
	headers = {"Content-Type": "application/json", "Authorization" : ('Bearer '+ apiKey)}
	result = json.loads(requestData(url, body, headers).decode('utf-8'))['choices'][0]['message']['content']

	return result

# makes a call to an azure endpoint.
# input: 
# 	filename where the prompt is written
#	prompt_text: product description.
#	endpointName: name of endpoint in the .env file
# 	apiKeyName: name of apiKey in the .env file
# output:
#	returns a string output
# calls another function 
def makePromptCall(file_name: str, prompt_text: str, endpointName: str, apiKeyName: str) -> str:
	prompt = open(file_name).read()
	messages=[
		{"role": "user", "content": (prompt + prompt_text)},
		# {"role": "user", "content": productDescription}
	]
	
	data =  {
		"messages": messages,
		"max_tokens": 3000,
		"temperature": 0.2,
		"top_p": 1
	}

	result = flow(data, endpointName, apiKeyName)
	return result


def writeToFile(filename: str, text: str, permissions: str) -> None:
	try:
		file = open(filename, permissions)
		file.write(text)
		file.close()

	except:
		print("error")


if __name__ == "__main__":
	listOfAllProducts = ['Elastomeric Half Mask Respirator',
					#   'SmartPhone', 'Electric Kettle', 'Laptop',
					#   'Bluetooth Speaker', 'Solar Panel', 
					#   'LED Light Bulb', 'Washing Machine'
					#   'Air Conditioner', 'Electric Toothbrush', 'Drone',
					#   'Fitness Tracker', 'Tablet', 'Electric Scooter',
					#   'Microwave Oven', 'Digital Camera'
					  ]
	
	for productDescription in listOfAllProducts:
		startTime = time.time()
		timeWhenRan = str(int(startTime))

		prompt = open('./prompt2.txt').read()
		
		combinedPromptOutput = makePromptCall(file_name='./prompt2.txt', 
											prompt_text=productDescription, 
											endpointName="PHI_3_MINI_128K_ENDPOINT", 
											apiKeyName="PHI_3_MINI_128K_API_KEY")
		
		cFileName = './output/combinedOutput_' + timeWhenRan + '.txt'
		textToWrite = productDescription + '\n' + combinedPromptOutput
		writeToFile(cFileName, textToWrite, 'w+')
		
		# Evaluate the output of combined prompt output
		promptStr = "Product Description: " + productDescription + "\nJSON file: " + combinedPromptOutput
		# cEvalResult = makePromptCall(file_name='./evalPrompt.txt', 
		# 					   prompt_text=promptStr,
		# 					   endpointName="PHI_3_MINI_128K_ENDPOINT",
		# 					   apiKeyName="PHI_3_MINI_128K_API_KEY")
		# print(f"{'~'*10} Evaluation Result {'~'*10}")
		# print(cEvalResult)

		
		# two separate prompts, targeting individual tasks
		componentsJson = makePromptCall(file_name='./getComponentPrompt.txt', 
									prompt_text=productDescription, 
									endpointName="PHI_3_MEDIUM_128K_ENDPOINT", 
									apiKeyName="PHI_3_MEDIUM_128K_API_KEY")
		
		separatePromptOutput = makePromptCall(file_name='./getManufacturingProcesses.txt', 
							prompt_text=componentsJson, 
							endpointName="PHI_3_MEDIUM_128K_ENDPOINT", 
							apiKeyName="PHI_3_MEDIUM_128K_API_KEY")

		
		promptStr = "Product Description: " + productDescription + "\nJSON file: " + separatePromptOutput
		sEvalResult = makePromptCall(file_name='./evalPrompt.txt', 
							   prompt_text=promptStr,
							   endpointName="PHI_3_MEDIUM_128K_ENDPOINT",
							   apiKeyName="PHI_3_MEDIUM_128K_API_KEY")
		# print(f"{'~'*10} Evaluation Result {'~'*10}")
		# print(sEvalResult)

		sFileName = './output/separateOutput128K_' + timeWhenRan + '.txt'
		textToWrite = productDescription + '\n' + componentsJson + '\n' + separatePromptOutput
		writeToFile(sFileName, textToWrite, 'w+')

		endTime = time.time()

		print(f"{productDescription} \n{endTime} - {startTime} = {endTime - startTime} s")
		
		# evalResults = makePromptCall(file_name='./evalPrompt.txt', 
		# 							prompt_text=separatePromptOutput, 
		# 							endpointName="PHI_3_MEDIUM_128K_ENDPOINT", 
		# 							apiKeyName="PHI_3_MEDIUM_128K_API_KEY")

		# print(evalResults)


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