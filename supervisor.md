# Supervisor 

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

