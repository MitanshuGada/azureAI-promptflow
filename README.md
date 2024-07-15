# azureAI-promptflow
Connect with LLM's deployed on AzureAI and use promptflow to manage the flow.

Prompty doesn't have support for serverless apis on azure. So we are not leveraging prompty yet.

When we have access to Azure-OpenAI model:
1. Create Prompty files according to the need.
2. Use promptflow and load the prompty and make the calls.
3. Create another evalutor prompty to evaluate the results. (We can also do manual testing of the results if we have sample json files to compare the results to.)


## Steps to run the code:
1. Clone the repository
2. Create a python virtual environment if you want to:
```python -m venv {name of env} ``` e.g. ```python -m venv .venv ```

3. Activate the virtual environment:
Windows: ```.\.venv\Scripts\activate``` Mac: ```source .\.venv\bin\activate```

4. Install the required libraries
```pip install -r requirements.txt```

5. Create a .env file and add the LLM endpoint and the api key
6. Modify the name of the environment variable in the file
7. Modify the prompt files accordingly
8. Run the rxpmoFlow.py
```python rxpmoFlow.py```

## rxpmoFlow.py

```
# Function to make the api call using the headers and body and url
def requestData(url: str, body: str, headers: dict):
```

```
# loads the url and apikey from the environment variables, creates the header for making the call.
# takes in the data, endpointName(name in the .env file), and apiKeyName(name in the .env file) and calls requestData function
@trace
def flow(data: dict, endpointName: str, apiKeyName: str) -> str:
```

```
# packs the product description string in messages list and reads the prompt from the fileName provided.
# creates a dictionary (data) with configuration information for the llm and calls the flow function
# input: 
# 	filename where the prompt is written
#	prompt_text: product description.
#	endpointName: name of endpoint in the .env file
# 	apiKeyName: name of apiKey in the .env file
# output:
#	returns a string output
def makePromptCall(file_name: str, prompt_text: str, endpointName: str, apiKeyName: str) -> str:

```

```
#Function to write data to a file with fileName and passed permissions
def writeToFile(filename: str, text: str, permissions: str) -> None:
```

```
# This function call is for a prompt that gets the entire assembly structure of a give product
combinedPromptOutput = makePromptCall(file_name='./prompt2.txt', 
											prompt_text=productDescription, 
											endpointName="PHI_3_MINI_128K_ENDPOINT", 
											apiKeyName="PHI_3_MINI_128K_API_KEY")

```
``` 
# We divided the prompts into two different prompts to test the performance. 

# get the list of components and sub-components needed for building a product
componentsJson = makePromptCall(file_name='./getComponentPrompt.txt', 
									prompt_text=productDescription, 
									endpointName="PHI_3_MEDIUM_128K_ENDPOINT", 
									apiKeyName="PHI_3_MEDIUM_128K_API_KEY")

# given a list of components and subcomponents, list down the manufacturing processes that can be used to make that component and sub-component		
separatePromptOutput = makePromptCall(file_name='./getManufacturingProcesses.txt', 
							prompt_text=componentsJson, 
							endpointName="PHI_3_MEDIUM_128K_ENDPOINT", 
							apiKeyName="PHI_3_MEDIUM_128K_API_KEY")										
```


### Sample Output for our prompt (JSON object):
```
{
	"components": [
		{
			"component_name": "Electric Kettle",
			"material": "Stainless Steel",
			"manufacturing_processes": [
				{
					"type": "Stamping"
				},
				{
					"type": "Welding"
				}
			],
			"subcomponents": [
			{
				"component_name": "Kettle Body",
				"material": "Stainless Steel",
				"manufacturing_processes": [
					{
						"type": "Stamping"
					},
					{
						"type": "Welding"
					},
					{
						"type": "Heat Treatment"
					}
				],
				"subcomponents": [
					{
						"component_name": "Lid",
						"material": "Plastic",
						"manufacturing_processes": [
						{
							"type": "Injection Molding"
						}
						]
					},
					{
						"component_name": "Spout",
						"material": "Stainless Steel",
						"manufacturing_processes": [
						{
							"type": "Stamping"
						},
						{
							"type": "Welding"
						}
						]
					},
					{
						"component_name": "Base",
						"material": "Stainless Steel",
						"manufacturing_processes": [
						{
							"type": "Stamping"
						},
						{
							"type": "Welding"
						},
						{
							"type": "Heat Treatment"
						},
						{
							"type": "Laser Cutting"
						}
						],
						"subcomponents": [
						{
							"component_name": "Heating Element",
							"material": "Copper",
							"manufacturing_processes": [
							{
								"type": "Wire Drawing"
							}
							]
						},
						{
							"component_name": "Power Switch",
							"material": "Plastic",
							"manufacturing_processes": [
							{
								"type": "Injection Molding"
							}
							]
						},
						{
							"component_name": "Thermostat",
							"material": "Plastic",
							"manufacturing_processes": [
							{
								"type": "Injection Molding"
							}
							]
						}
						]
					}
					]
				},
				{
					"component_name": "Handle",
					"material": "Plastic",
					"manufacturing_processes": [
					{
						"type": "Injection Molding"
					}
					]
				},
				{
					"component_name": "Power Cord",
					"material": "Corded Plastic",
					"manufacturing_processes": [
					{
						"type": "Injection Molding"
					}
					]
				}
			]
		}
	]
}
```