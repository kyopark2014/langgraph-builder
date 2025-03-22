# LangGraph Builder로 App 개발하기

LangGraph로 Agent 설계시 Graph drawing은 아무래도 복잡하고 어려운 일입니다. 이를 위해 LangGraph에서 나온 LangGraph Builder에 대해 소개합니다. LangGraph에서는 No code 툴로 포지셔닝하고 있지만, 제 생각에는 LangGraph 경험이 있는 사람들이 편리하게 사용할 수 있을것 같습니다.

## LangGraph Builder의 활용

[LangGraph Builder](https://build.langchain.com/)에 접속합니다. 

<img src="https://github.com/user-attachments/assets/bf196f8e-4f43-47d1-9f4b-aba65579cbc6" width="600">

아래와 같이 Supervisor Node에서 RAG와 Websearch를 하는 Node들을 거느린 그래프를 생성합니다.

<img src="https://github.com/user-attachments/assets/43d2f3b9-a0c8-42f1-b45b-55169fc6638f" width="600">

그래프를 그리고 나서 생성을 하면 "spec.yml", "stub.py", "implementation.py" 파일이 생성됩니다.

"implementation.py"에서 아래와 같이 마지막 줄의 invoke를 하는 print문을 주석처리합니다.

<img src="https://github.com/user-attachments/assets/5b69dfe7-b641-4558-85b6-0cb7e4060dc4" width="400">

이제 langgraph.json 파일을 아래와 같이 생성합니다.

```java
{
    "dependencies": ["."],
    "graphs": {
      "agent": "implementation:compiled_agent"
    },
    "env": ".env"
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

생성된 LangGraph Agent Graph는 아래와 같습니다.

<img src="https://github.com/user-attachments/assets/ad220386-066b-43ab-ab56-1c25d2b23f8e" width="600">

[langgraph-gen](https://github.com/langchain-ai/langgraph-gen-py)는 LangGraph CLI로서 LangGraph stub를 생성할 수 있습니다. 아래와 같이 langgraph-gen을 설치합니다. 

```text
pip install langgraph-gen
```

아래와 같이 실행하면 supervisor-agent.py를 생성하여 활용할 수 있습니다.

```text
langgraph-gen spec.yml -o stub.py --implementation supervisor-agent.py
```

## CRAG 구현하기

[CRAG-Corrective RAG](https://github.com/kyopark2014/agentic-rag/blob/main/README.md#corrective-rag)는 RAG의 응답 정확도와 신뢰를 높이는 방법중에 하나 입니다. 먼저 아래와 같이 CRAG를 구성하였습니다.

![image](https://github.com/user-attachments/assets/18c11abf-b828-44df-8e2c-f07eaba67c0d)


LangGraph studio로 확인해보면 아래와 같이 graph가 잘 생성된것을 확인할 수 있습니다.

![image](https://github.com/user-attachments/assets/10b40b83-819d-405f-ba01-f9483f72cb9a)



## Reference 

[LangGraph Builder (YouTube)](https://www.youtube.com/watch?v=iwPeT_I_GEc)

[LangGraph Builder (Github)](https://github.com/langchain-ai/langgraph-builder)

[LangGraph Gen (Github)](https://github.com/langchain-ai/langgraph-gen-py)
