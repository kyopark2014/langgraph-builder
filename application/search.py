import traceback
import boto3
import json
import utils

from langchain.docstore.document import Document
from tavily import TavilyClient  
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

logger = utils.CreateLogger("chat")

config = utils.load_config()

bedrock_region = config["region"] if "region" in config else "us-west-2"
projectName = config["projectName"] if "projectName" in config else "agentic-workflow"

# load secret
secretsmanager = boto3.client(
    service_name='secretsmanager',
    region_name=bedrock_region
)

# api key for tavily search
tavily_key = tavily_api_wrapper = ""
try:
    get_tavily_api_secret = secretsmanager.get_secret_value(
        SecretId=f"tavilyapikey-{projectName}"
    )
    #print('get_tavily_api_secret: ', get_tavily_api_secret)
    secret = json.loads(get_tavily_api_secret['SecretString'])
    #print('secret: ', secret)

    if "tavily_api_key" in secret:
        tavily_key = secret['tavily_api_key']
        #print('tavily_api_key: ', tavily_api_key)

        if tavily_key:
            tavily_api_wrapper = TavilySearchAPIWrapper(tavily_api_key=tavily_key)

        else:
            logger.info(f"tavily_key is required.")
except Exception as e: 
    logger.info(f"Tavily credential is required: {e}")
    raise e

def retrieve_documents_from_tavily(query, top_k):
    logger.info(f"###### retrieve_documents_from_tavily ######")

    relevant_documents = []        
    search = TavilySearchResults(
        max_results=top_k,
        include_answer=True,
        include_raw_content=True,        
        api_wrapper=tavily_api_wrapper,
        search_depth="advanced", 
        # include_domains=["google.com", "naver.com"]
    )
                    
    try: 
        output = search.invoke(query)
        logger.info(f"tavily output: {output}")

        if output[:9] == "HTTPError":
            logger.info(f"output: {output}")
            raise Exception ("Not able to request to tavily")
        else:        
            logger.info(f"-> tavily query: {query}")
            for i, result in enumerate(output):
                logger.info(f"{i}: {result}")
                if result:
                    content = result.get("content")
                    url = result.get("url")
                    
                    relevant_documents.append(
                        Document(
                            page_content=content,
                            metadata={
                                'name': 'WWW',
                                'url': url,
                                'from': 'tavily'
                            },
                        )
                    )                   
    
    except Exception:
        err_msg = traceback.format_exc()
        logger.info(f"error message: {err_msg}")     
        # raise Exception ("Not able to request to tavily")   

    return relevant_documents 

def retrieve_contents_from_tavily(queries, top_k):
    logger.info(f"###### retrieve_documents_from_tavily ######")

    contents = []       
    search = TavilySearchResults(
        max_results=top_k,
        include_answer=True,
        include_raw_content=True,        
        api_wrapper=tavily_api_wrapper,
        search_depth="advanced", 
        # include_domains=["google.com", "naver.com"]
    )
                    
    try: 
        for query in queries:
            output = search.invoke(query)
            logger.info(f"tavily output: {output}")

            if output[:9] == "HTTPError":
                logger.info(f"output: {output}")
                raise Exception ("Not able to request to tavily")
            else:        
                logger.info(f"-> tavily query: {query}")
                for i, result in enumerate(output):
                    logger.info(f"{i}: {result}")
                    if result and 'content' in result:
                        contents.append(result['content'])
    
    except Exception:
        err_msg = traceback.format_exc()
        logger.info(f"error message: {err_msg}")     
        # raise Exception ("Not able to request to tavily")   

    return contents 

def tavily_search(query, k):
    docs = []    
    try:
        tavily_client = TavilyClient(
            api_key=tavily_key
        )
        response = tavily_client.search(query, max_results=k)
        # print('tavily response: ', response)
            
        for r in response["results"]:
            name = r.get("title")
            if name is None:
                name = 'WWW'
            
            docs.append(
                Document(
                    page_content=r.get("content"),
                    metadata={
                        'name': name,
                        'url': r.get("url"),
                        'from': 'tavily'
                    },
                )
            )                   
    except Exception as e:
        logger.info(f"Exception: {e}")

    return docs

