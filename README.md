# LangGraph Builder로 App 개발하기

LangGraph로 Agent 설계시 Graph drawing은 아무래도 복잡하고 어려운 일입니다. 이를 위해 LangGraph에서 나온 LangGraph Builder에 대해 소개합니다.

## 상세 개발 하기 

### LangGraph Builder

[LangGraph Builder](https://build.langchain.com/)에 접속합니다. 

<img src="https://github.com/user-attachments/assets/bf196f8e-4f43-47d1-9f4b-aba65579cbc6" width="600">

아래와 같이 Supervisor Node에서 RAG와 Websearch를 하는 Node들을 거느린 그래프를 생성합니다.

![image](https://github.com/user-attachments/assets/43d2f3b9-a0c8-42f1-b45b-55169fc6638f)

그래프를 그리고 나서 생성을 하면 "spec.yml", "stub.py", "implementation.py" 파일이 생성됩니다.

### 개발환경 설정

아래와 같이 langgraph-cli을 설치합니다. 이렇게 하면 LangGraph Studio를 이용할 수 있습니다.


```text
pip install 'langgraph-cli[inmem]'
```

## langgraph-gen

[langgraph-gen](https://github.com/langchain-ai/langgraph-gen-py)는 LangGraph CLI로서 LangGraph stub를 생성할 수 있습니다. 아래와 같이 langgraph-gen을 설치합니다. 

```text
pip install langgraph-gen
```

실제 사용은 아래와 같습니다.

```text
langgraph-gen spec.yml -o custom_output.py --implementation custom_impl.py
```

## Reference 

[LangGraph Builder (YouTube)](https://www.youtube.com/watch?v=iwPeT_I_GEc)

[LangGraph Builder (Github)](https://github.com/langchain-ai/langgraph-builder)

[LangGraph Gen (Github)](https://github.com/langchain-ai/langgraph-gen-py)
