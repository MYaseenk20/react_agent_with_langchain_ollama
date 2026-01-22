# 🧠 ReAct Agent with LangChain & Ollama

This project demonstrates a **manual implementation of the ReAct (Reason + Act) agent pattern** using **LangChain**, **Ollama**, and a **custom tool execution loop**.

Instead of relying on `AgentExecutor`, this example shows **how ReAct works internally**, giving you full control and understanding of the agent’s reasoning and tool usage.

---

## 🚀 Features

- ✅ Custom **ReAct prompt**  
  *(Thought → Action → Observation → Final Answer)*
- ✅ Tool calling **without `AgentExecutor`**
- ✅ Manual agent loop using `AgentAction` and `AgentFinish`
- ✅ Uses **Ollama local models** (`gemma2`)
- ✅ Callback support for debugging agent behavior
- ✅ Simple example tool: `get_text_length`

---

## 🧠 How the ReAct Agent Works

1. **LLM receives the question**
2. **LLM reasons** (`Thought`)
3. **LLM selects a tool** (`Action`)
4. **Tool is executed**
5. **Observation is added to the scratchpad**
6. **LLM continues reasoning**
7. **Final answer is produced**

This loop continues until the LLM returns **`Final Answer`**.

---

## 🤖 Tech Stack

- **Python**
- **LangChain**
- **Ollama**
- **ReAct prompting pattern**


- Debug tool-calling behavior
- Experiment with local LLMs using Ollama
