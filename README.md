# azureAI-promptflow
Connect with LLM's deployed on AzureAI and use promptflow to manage the flow.


## Steps to run the code:
1. Clone the repository
2. Create a python virtual environment if you want to:
```python -m venv {name of env} ``` e.g. ```python -m venv .venv ```

3. Activate the virtual environment:
Windows: ```.\\.venv\Scripts\activate``` Mac: ```source .\\.venv\bin\activate```

4. Install the required libraries
```pip install -r requirements.txt```

5. Create a .env file and add the LLM endpoint and the api key
6. Modify the name of the environment variable in the file
7. Modify the prompt according to your requirements
8. Run the rxpmoFlow.py
```python rxpmoFlow.py```

### Sample Output for our prompt (JSON object):
```
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
```