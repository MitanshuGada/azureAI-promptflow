# azureAI-promptflow
Connect with LLM's deployed on AzureAI and use promptflow to manage the flow.


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