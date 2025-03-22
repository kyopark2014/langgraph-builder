# LangGraph Builder로 Agent 개발하기

<p align="left">
    <a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fkyopark2014%2Fagentic-builder&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false")](https://hits.seeyoufarm.com"/></a>
    <img alt="License" src="https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square">
</p>


저의 경우에는 LangGraph에 경혐이 꽤 쌓일때까지 graph diagram을 그리는것이 매우 어려운 일이었습니다. 이후 LangGraph Studio가 나왔지만 여전히 어려웠는데요. 이번에 다시 [LangGraph Builder](https://github.com/langchain-ai/langgraph-builder)가 나옮으로 해서 이런 어려움을 상당부분 해소가 될것 같습니다. 여기에서는 [LangGraph Builder](https://build.langchain.com/)를 이용해 CRAG (Corrective RAG)를 지원하는 agent를 생성하는 방법에 대해 설명합니다. LangGraph에서는 No code 툴로 포지셔닝하고 있지만, 제 생각에는 LangGraph 경험이 있는 사람들이 더 편리하게 사용할 수 있을것 같습니다.

## CRAG 구현하기

[LangGraph Builder](https://build.langchain.com/)에 접속합니다. 

<img src="https://github.com/user-attachments/assets/bf196f8e-4f43-47d1-9f4b-aba65579cbc6" width="600">

[CRAG-Corrective RAG](https://github.com/kyopark2014/agentic-rag/blob/main/README.md#corrective-rag)는 RAG의 응답 정확도와 신뢰를 높이는 방법중에 하나 입니다. [LangGraph Builder](https://build.langchain.com/)에 접속하여 아래와 같이 CRAG를 구성하였습니다. 

<img src="https://github.com/user-attachments/assets/18c11abf-b828-44df-8e2c-f07eaba67c0d" width="400">

LangGraph Builder의 [Generate Code]를 선택하여 "spec.yml", "stub.py", "implementation.py"을 생성한 후에 다운로드 합니다. 이후 "implementation.py"의 마지막 print문을 주석처리합니다.

<img src="https://github.com/user-attachments/assets/1c8f048d-03e9-47fa-84fd-d8cbbe6984b0" width="400">

이제 langgraph.json 파일을 아래와 같이 생성합니다.

```java
{
   "dependencies":[
      "."
   ],
   "graphs":{
      "agent":"implementation:compiled_agent"
   },
   "env":".env"
}
```

아래와 같이 langgraph-cli을 설치합니다. 이렇게 하면 LangGraph Studio를 이용할 수 있습니다.

```text
pip install 'langgraph-cli[inmem]'
```

이후 아래와 같이 실행합니다.

```text
langgraph dev
```

이제 LangGraph studio로 graph가 잘 생성된것을 확인할 수 있습니다.


![image](https://github.com/user-attachments/assets/10b40b83-819d-405f-ba01-f9483f72cb9a)


[langgraph-gen](https://github.com/langchain-ai/langgraph-gen-py)는 LangGraph CLI로서 LangGraph stub를 생성할 수 있습니다. 아래와 같이 langgraph-gen을 설치합니다. 

```text
pip install langgraph-gen
```

아래 명령어로 crag.py 파일을 생성합니다.

```text
langgraph-gen spec.yml -o stub.py --implementation crag.py
```

[Corrective RAG](https://github.com/kyopark2014/agentic-rag?tab=readme-ov-file#corrective-rag)을 참조하여 [crag.py](./application/crag.py)을 수정합니다.

CRAG를 위한 State를 정의합니다.

```python
class State(TypedDict):
    question : str
    generation : str
    web_search : str
    documents : List[str]
```

Retrieve Node는 아래와 같습니다. 여기에서는 OpenSearch를 이용해 RAG를 구성하였고, 4개의 관련된 문서를 가져와서 활용합니다.

```python
def retrieve(state: State) -> dict:
    logger.info(f"###### retrieve ######")
    
    question = state["question"]

    documents = rag.retrieve_documents_from_opensearch(question, top_k=4)
    
    return {"documents": documents}
```

가져온 문서는 grade_documents에서 평가를 수행합니다.

```python
def grade_documents(state: State) -> dict:
    logger.info(f"###### grade_documents ######")

    filtered_docs = chat.grade_documents_using_llm(state["question"], state["documents"])

    web_search = "yes" if len(filtered_docs) < len(state["documents"]) else "no"

    return {"documents": filtered_docs, "web_search": web_search}
```

추가로 문서를 검색할 때에는 먼저 질문을 rewrite합니다.

```python
def rewrite(state: State) -> dict:
    logger.info(f"###### rewrite ######")
    question = state["question"]
    documents = state["documents"]
    
    question_rewriter = chat.get_rewrite()
    
    better_question = question_rewriter.invoke({"question": question})

    return {"question": better_question.question, "documents": documents}
```

인터넷 검색을 위한 websearch 노드는 아래와 같습니다.

```python
def websearch(state: State) -> dict:
    logger.info(f"###### web_search ######")
    question = state["question"]
    documents = state["documents"]
    
    docs = search.retrieve_documents_from_tavily(question, top_k=3)

    for doc in docs:
        documents.append(doc)
        
    return {"question": question, "documents": documents}
```

검색된 문서를 가지고 답변을 생성합니다.

```python
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
    
    output = result.content
    if output.find('<result>')!=-1:
        output = output[output.find('<result>')+8:output.find('</result>')]
        
    return {"generation": output}
```

Conditional edge는 아래와 같습니다.

```python
def conditional_edge(state: State) -> str:
    logger.info(f"###### decide_to_generate ######")
    web_search = state["web_search"]
    
    if web_search == "yes":
        return "rewrite"
    else:
        return "generate"
```

CRAG는 아래와 같이 실행합니다.

```python
def run_crag(question):
    inputs = {"question": question}    
    config = {
        "recursion_limit": 50
    }

    for output in compiled_agent.stream(inputs, config):   
        for key, value in output.items():
            logger.info(f"Finished running: {key}")

    return value["generation"]
```

### 실행하기

아래와 같이 streamlit을 실행합니다.

```python
streamlit run application/app.py
```

아래와 같이 Corrective RAG를 실행할 수 있습니다.

<img src="https://github.com/user-attachments/assets/2648c666-4e79-4a05-bdfb-02079e5436da" width="700">

아래 아래와 검색하면 RAG와 인터넷 검색을 통해 아래와 같은 결과를 얻습니다.

<img src="https://github.com/user-attachments/assets/069af2bf-ec9f-48b2-af24-a7ce4932d194" width="400">


## Reference 

[LangGraph Builder (YouTube)](https://www.youtube.com/watch?v=iwPeT_I_GEc)

[LangGraph Builder (Github)](https://github.com/langchain-ai/langgraph-builder)

[LangGraph Gen (Github)](https://github.com/langchain-ai/langgraph-gen-py)
