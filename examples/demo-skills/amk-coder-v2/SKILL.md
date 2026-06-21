# amk-coder-v2 — Myanmar Coding Agent

**Category:** AI/ML
**Priority:** 90
**Model:** [amkyawdev/amk-coder-v2](https://huggingface.co/amkyawdev/amk-coder-v2)

## Overview

A Myanmar-localized coding assistant fine-tuned from **Qwen2.5-Coder-1.5B** using LoRA (PEFT) technique. Supports full Myanmar Unicode text and code generation in multiple languages.

## Model Details

| Attribute | Value |
|---|---|
| **Base Model** | Qwen2.5-Coder-1.5B |
| **Parameters** | 2B (2,000M) |
| **Architecture** | Qwen2ForCausalLM |
| **Context Length** | 32,768 tokens |
| **Format** | Safetensors (BF16) |
| **Languages** | Burmese + English |

## Training Configuration

| Parameter | Value |
|---|---|
| **Framework** | Transformers + PEFT |
| **Training Method** | LoRA fine-tuning |
| **Target Modules** | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| **Optimizer** | paged_adamw_8bit |
| **Learning Rate** | 3e-5 |
| **Epochs** | 3 |
| **Batch Size** | 8 |
| **Max Length** | 2048 |
| **Precision** | FP16 mixed |
| **Hardware** | Kaggle Dual T4 GPU |

## Features

- 🇲🇲 **Myanmar Support** — Full support for Myanmar Unicode text
- 💻 **Code Generation** — Python, JavaScript, C++, Java, and more
- 🐛 **Debugging** — Bug detection and fixes
- 📖 **Code Explanation** — Line-by-line explanations
- 🔍 **Web Search** — Integration for latest documentation

## Chat Template (ChatML)

```
<|im_start|>system
You are an expert Myanmar AI coding agent with tool access.<|im_end|>
<|im_start|>user
{Instruction}
Tools available: {Tools}<|im_end|>
<|im_start|>assistant
Thought & Code:
```

## Usage

### Transformers (Python)

```python
from transformers import pipeline

pipe = pipeline("text-generation", model="amkyawdev/amk-coder-v2")
messages = [
    {"role": "user", "content": "Python function တစ်ခုရေးပါ။ list comprehension နဲ့ sorting လုပ်ပေးပါ။"}
]
result = pipe(messages, max_new_tokens=512, temperature=0.2)
print(result[0]['generated_text'])
```

### Direct Model Loading

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("amkyawdev/amk-coder-v2")
model = AutoModelForCausalLM.from_pretrained(
    "amkyawdev/amk-coder-v2",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Write a Python function to reverse a string"}
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

outputs = model.generate(inputs, max_new_tokens=512, temperature=0.2)
response = tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True)
print(response)
```

### vLLM (Production)

```bash
# Install vLLM
pip install vllm

# Start server
vllm serve "amkyawdev/amk-coder-v2" --tensor-parallel-size 1

# API call
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "amkyawdev/amk-coder-v2",
    "messages": [{"role": "user", "content": "Write Python code"}],
    "max_tokens": 512,
    "temperature": 0.2
  }'
```

### SGLang

```bash
# Install SGLang
pip install sglang

# Start server
python -m sglang.launch_server --model-path "amkyawdev/amk-coder-v2" --port 30000

# API call
curl -X POST "http://localhost:30000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "amkyawdev/amk-coder-v2",
    "messages": [{"role": "user", "content": "Write a hello world in Python"}]
  }'
```

## Best Practices

1. **Myanmar Text** — Use proper Myanmar Unicode (not Zawgyi) for best results
2. **Temperature** — Use 0.2-0.3 for code generation, higher for creative tasks
3. **Max Tokens** — Set 512-1024 for typical responses, up to 4096 for complex tasks
4. **System Prompt** — Include clear instructions about expected output format

## Resources

- [HuggingFace Model](https://huggingface.co/amkyawdev/amk-coder-v2)
- [Qwen2.5-Coder Documentation](https://qwenlm.github.io/blog/Qwen2.5-Coder/)
- [Transformers Library](https://huggingface.co/docs/transformers)