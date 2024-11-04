## LocaL LLM + RAG with Kotaemon & Ollama

<img src="assets/image.png" alt="drawing" style="width:500px;height:500px"/>

### Kotaemon Docker
- [run kotaemon docker](https://github.com/Cinnamon/kotaemon)

```
docker run \
-e GRADIO_SERVER_NAME=0.0.0.0 \
-e GRADIO_SERVER_PORT=7860 \
-p 7860:7860 -it --rm \
-v /Users/takis/Documents/sckool/kotaemon-hybrid-rag/ktm-mnt-vol:/app/ktem_app_data \
ghcr.io/cinnamon/kotaemon:main-lite
```

### Ollama - local LLMs
<br>

- [download ollama](https://ollama.com/download)
- [ollama llm list](https://github.com/ollama/ollama)
```
ollama list
ollama run llama3.2
ollama rm llama3.2
/bye
```

<br>

### Fun Fact :)
- [Github is where you can find free OpenAI keys](https://x.com/sirifu4k1/status/1640717220040040455)
```
/"sk-[a-zA-Z0-9]{20,50}"/ language:Shell
```
