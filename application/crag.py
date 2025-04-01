import utils
import search 
import chat
import rag_opensearch as rag

from typing_extensions import TypedDict
from stub import Agent
from typing import List

logger = utils.CreateLogger("crag")

config = utils.load_config()

class State(TypedDict):
    question : str
    generation : str
    web_search : str
    documents : List[str]

def retrieve(state: State) -> dict:
    logger.info(f"###### retrieve ######")
    logger.info(f"state: {state}")
    
    question = state["question"]
    logger.info(f"question: {question}")

    documents = rag.retrieve_documents_from_opensearch(question, top_k=4)
    logger.info(f"documents: {len(documents)}")
    
    return {"documents": documents}

def grade_documents(state: State) -> dict:
    logger.info(f"###### grade_documents ######")
    logger.info(f"start grading...")

    filtered_docs = chat.grade_documents_using_llm(state["question"], state["documents"])

    logger.info(f"filtered_docs: {len(filtered_docs)}")

    web_search = "yes" if len(filtered_docs) < len(state["documents"]) else "no"
    logger.info(f"web_search: {web_search}")

    return {"documents": filtered_docs, "web_search": web_search}

def generate(state: State) -> dict:
    logger.info(f"###### generate ######")
    question = state["question"]
    documents = state["documents"]

    rag_chain = chat.get_rag_prompt(question)
    relevant_context = ""
    for document in documents:
        relevant_context = relevant_context + document.page_content + "\n\n"    
    
    result = rag_chain.invoke(
        {
            "question": question, 
            "context": relevant_context
        }
    )
    logger.info(f"result: {result}")
    
    output = result.content
    if output.find('<result>')!=-1:
        output = output[output.find('<result>')+8:output.find('</result>')]
    logger.info(f"output: {output}")
        
    return {"generation": output}

def rewrite(state: State) -> dict:
    logger.info(f"###### rewrite ######")
    question = state["question"]
    documents = state["documents"]
    
    question_rewriter = chat.get_rewrite()
    
    better_question = question_rewriter.invoke({"question": question})
    logger.info(f"better_question: {better_question.question}")

    return {"question": better_question.question, "documents": documents}

def websearch(state: State) -> dict:
    logger.info(f"###### web_search ######")
    question = state["question"]
    documents = state["documents"]
    
    docs = search.retrieve_documents_from_tavily(question, top_k=3)

    for doc in docs:
        documents.append(doc)
        
    return {"question": question, "documents": documents}

def decide_to_generate(state: State) -> str:
    logger.info(f"###### decide_to_generate ######")
    web_search = state["web_search"]
    
    if web_search == "yes":
        logger.info(f"---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---")
        return "rewrite"
    else:
        logger.info(f"---DECISION: GENERATE---")
        return "generate"

agent = Agent(
    state_schema=State,
    impl=[
        ("retrieve", retrieve),
        ("grade_documents", grade_documents),
        ("generate", generate),
        ("rewrite", rewrite),
        ("websearch", websearch),
        ("decide_to_generate", decide_to_generate),
    ],
)

compiled_agent = agent.compile()

def run_crag(question):
    inputs = {"question": question}    
    config = {
        "recursion_limit": 50
    }

    for output in compiled_agent.stream(inputs, config):   
        for key, value in output.items():
            logger.info(f"Finished running: {key}")
    
    logger.info(f"value: {value}")

    return value["generation"]