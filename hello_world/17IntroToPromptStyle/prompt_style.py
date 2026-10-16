# Prompt Style

## 1. Alpaca Prompt Style

###Instruction: <SYSTEM_PROMPT>\n
###Input: <USER_QUERY>
###Response: \n

## 2. ChatML 
###(What we did now with openai (that role: user|assistant, content: who are you) is actually chatML)
"""###Object - {"role": "system" | "user" | "assistant"
   Key -   "content": "string"}
"""

## 3. INST Propting (used by Llama 2)
### [INST] What is the time now? [/INST]

# Use help of chatgpt to konw about these prompt styles and try to convert those prev SYSTEM_PROMPT into these styles