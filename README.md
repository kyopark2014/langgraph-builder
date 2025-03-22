# LangGraph Builder

LangGraph로 Agent 설계시 Graph drawing은 아무래도 복잡하고 어려운 일입니다. 이를 위해 LangGraph에서 나온 LangGraph Builder에 대해 소개합니다.

## 접속 방법

[LangGraph Builder](https://build.langchain.com/)에 접속합니다. 

<img src="https://github.com/user-attachments/assets/bf196f8e-4f43-47d1-9f4b-aba65579cbc6" width="600">



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
