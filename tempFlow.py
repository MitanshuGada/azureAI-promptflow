import os

from dotenv import load_dotenv
from pathlib import Path
from promptflow.tracing import trace
from promptflow.core import tool, Prompty, AzureOpenAIModelConfiguration

# BASE_DIR = Path(__file__).parent.absolute().as_posix()
BASE_DIR = Path(__file__).absolute().parent
"""
Tracing is a powerful tool that offers developers an in-depth understanding of the execution process of their generative AI applications such as agents, AutoGen, and retrieval augmented generation (RAG) use cases. It provides a detailed view of the execution flow, including the inputs and outputs of each node within the application.
"""
@trace
def chat(product_description: str = "An elastomeric half mask respirator tight-fitting facepiece made of synthetic or natural rubber materials.") -> str:
    """Flow entry function."""
    # print(product_description)
    # if "AZURE_OPENAI_API_KEY" not in os.environ and "AZURE_OPENAI_ENDPOINT" not in os.environ:
    #     print("nope")
    #     # load environment variables from .env file
    #     load_dotenv()
    #     print(os.environ["AZURE_OPENAI_ENDPOINT"])
    #     print(os.environ["AZURE_OPENAI_API_KEY"])
        
    # configuration = AzureOpenAIModelConfiguration (
    #     azure_deployment="${AZURE_OPENAI_DEPLOYMENT}",
    #     api_key="${env:AZURE_OPENAI_API_KEY}",
    #     api_version="${env:AZURE_OPENAI_API_VERSION}",
    #     azure_endpoint="https://Phi-3-mini-128k-instruct-hipdk-serverless.eastus2.inference.ai.azure.com/v1/chat/completions"
    # )
    # print(configuration)
    
    # override_model = {
    #     "configuration": configuration,
    #     "parameters": {"max_tokens": 1024}
    # }
    
    # print(override_model)
    
    prompty = Prompty.load(source=BASE_DIR / "chat.prompty")
    # trigger a llm call with the prompty obj
    output = prompty(product_description=product_description)
    print(output)
    return output

# @tool
# def flow_entry(product_description: any) -> str:
#     path_to_prompty = BASE_DIR + './chat.prompty'
#     flow = Prompty.load(path_to_prompty)

#     result = flow(product_description)

#     return(result)
# if __name__ == "__main__":
#     print(flow_entry("What is the capital of France?"))