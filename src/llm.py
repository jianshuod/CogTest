import os
import time
import json
from tqdm import tqdm
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  base_url=os.getenv("OPENAI_BASE_URL"),
  api_key=os.getenv("OPENAI_API_KEY"),
)

from anthropic import Anthropic

anthropic_client = Anthropic(
  base_url=os.getenv("ANTHROPIC_BASE_URL"), 
  api_key=os.getenv("ANTHROPIC_API_KEY"),
)

def model_name_normalize(model_name: str) -> str:
    return model_name.replace("/", "-").replace(" ", "-").replace(".", "-")

# TODO: You may need to adjust the interfaces according to the API you use.

models = [
    "Qwen/Qwen3-235B-A22B",
    "Qwen/Qwen3-30B-A3B", 
    "Qwen/Qwen3-32B",
    "Qwen/Qwen3-14B",
    "Qwen/Qwen3-8B",
    "DeepSeek-R1",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "Doubao-1.5-thinking-pro",
    "gpt/o4-mini",
    "gpt/o3",
    "claude-3-7-sonnet-20250219",
    "DeepSeek-V3",
    "gpt-4o",
    "Qwen/Qwen2.5-32B-Instruct"
]

def parse_reasoning_content_from_response(response, model_name):
    if model_name == "Qwen/Qwen3-235B-A22B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif "deepseek-r1" in model_name.lower():
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "Qwen/QwQ-32B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "Qwen/Qwen3-30B-A3B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "Qwen/Qwen3-32B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "Qwen/Qwen3-14B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "Qwen/Qwen3-8B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif model_name == "deepseek-r1-distill-llama-70b":
        return response.choices[0].message.content.split("<think>")[1].split("</think>")[0].strip(), response.choices[0].message.content.split("</think>")[-1].strip()
    elif model_name == "DeepSeek-V3":
        return response.choices[0].message.content.split("<think>")[1].split("</think>")[0].strip(), response.choices[0].message.content.split("</think>")[-1].strip()
    elif model_name == "gpt-4o":
        return response.choices[0].message.content.split("<think>")[1].split("</think>")[0].strip(), response.choices[0].message.content.split("</think>")[-1].strip()
    elif model_name == "Qwen/Qwen2.5-32B-Instruct":
        return response.choices[0].message.content.split("<think>")[1].split("</think>")[0].strip(), response.choices[0].message.content.split("</think>")[-1].strip()
    elif model_name == "Doubao-1.5-thinking-pro":
        return response.choices[0].message.reasoning_content, response.choices[0].message.content
    elif "gpt" in model_name:
        reasoning_content = ""
        print(response)
        for idx, output in enumerate(response.output):
            if output.type == "reasoning":
                if len(output.summary) > 0:
                    reasoning_content = output.summary[0].text
            else:
                continue
        return reasoning_content, response.output_text
    elif "claude" in model_name:
        reasoning_content = ""
        response_content = ""
        for block in response.content:
            if block.type == "thinking":
                reasoning_content += block.thinking
            elif block.type == "text":
                response_content = block.text
        return reasoning_content, response_content
    else:
        raise ValueError(f"Unsupported model: {model_name}")


def query_llms_with_instructions(
    models: list[str],
    instructions: list[str],
    reasoning_effort: str = "medium",
    **gen_kwargs,
) -> list[dict]:
    
    results = []
    for instruction in tqdm(instructions):
        result = {"instruction": instruction, "thinking": {}, "response": {}}
        for model_name in models:
            if "o4-mini" in model_name or "o3" in model_name:
                gen_kwargs.pop("temperature", None)
                gen_kwargs.pop("top_p", None)
                
            if "gpt" in model_name:
                if "gpt-4o" in model_name:
                    response = client.responses.create(
                        model=model_name.split("/")[-1],
                        input=instruction,
                        **gen_kwargs
                    )
                else:
                    response = client.responses.create(
                        model=model_name.split("/")[-1],
                        input=instruction,
                        reasoning={
                            "effort": reasoning_effort,
                            "summary": "detailed"
                        },
                        **gen_kwargs
                    )
            elif "claude" in model_name:
                gen_kwargs.pop("temperature", None)
                gen_kwargs.pop("top_p", None)
                gen_kwargs.pop("top_k", None)
                response = anthropic_client.messages.create(
                    model=model_name,
                    max_tokens=20000,
                    thinking={
                        "type": "enabled",
                        "budget_tokens": 16000
                    },
                    messages=[{
                        "role": "user",
                        "content": instruction
                    }],
                    **gen_kwargs
                )
            else:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "user", "content": instruction},
                    ],
                    **gen_kwargs,
                )
            reasoning_content, response_content = parse_reasoning_content_from_response(response, model_name)
            result["thinking"][model_name] = reasoning_content
            result["response"][model_name] = response_content
        results.append(result)
    
    return results


def query_llm_with_instructions_parallel(
    model_name: str,
    instructions: list[str],
    reasoning_effort: str = "medium",
    num_workers: int = 4,
    output_dir_base: str = "assets/results/default",
    **gen_kwargs,
) -> list[dict]:
    output_path = f"{output_dir_base}/{model_name_normalize(model_name)}.jsonl"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    extra_system_prompt = (
        "A conversation between User and Assistant. The user asks a question, "
        "and the Assistant solves it. The assistant first thinks about the reasoning "
        "process in the mind and then provides the user with the answer. "
        "The reasoning process and answer are enclosed within <think> </think> and "
        "<answer> </answer> tags, respectively, i.e., <think> reasoning process here </think> "
        "<answer> answer here </answer>."
    )
    
    SYSTEM_PROMPT_MODELS = {
        "DeepSeek-V3",
        "gpt-4o",
        "Qwen/Qwen2.5-32B-Instruct"
    }

    existing_instructions = set()
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    existing_instructions.add(obj.get("instruction"))
                except json.JSONDecodeError:
                    continue

    new_instructions = [inst for inst in instructions if inst not in existing_instructions]
    
    if not new_instructions:
        print(f"All {len(instructions)} instructions already processed for model {model_name}. Nothing to do.")
        return []

    chunk_size = max(len(new_instructions) // num_workers, 1)

    def process_instruction_chunk(chunk):
        results = []
        local_gen_kwargs = gen_kwargs.copy()
        
        if "o4-mini" in model_name or "gpt/o4-mini" in model_name:
            local_gen_kwargs.pop("temperature", None)
            local_gen_kwargs.pop("top_p", None)

        for instruction in chunk:
            result = {"instruction": instruction, "thinking": {}, "response": {}}
            success = False
            max_retries = 1

            for attempt in range(max_retries):
                try:
                    if model_name in SYSTEM_PROMPT_MODELS:
                        messages = [
                            {"role": "system", "content": extra_system_prompt},
                            {"role": "user", "content": instruction}
                        ]
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=messages,
                            **local_gen_kwargs,
                        )
                        print(response)
                    elif "gpt" in model_name and model_name not in SYSTEM_PROMPT_MODELS:
                        response = client.responses.create(
                            model=model_name.split("/")[-1],
                            input=instruction,
                            reasoning={"effort": reasoning_effort, "summary": "detailed"},
                            **local_gen_kwargs
                        )
                    
                    elif "claude" in model_name:
                        local_gen_kwargs.pop("temperature", None)
                        local_gen_kwargs.pop("top_p", None)
                        local_gen_kwargs.pop("top_k", None)
                        response = anthropic_client.messages.create(
                            model=model_name,
                            max_tokens=20000,
                            thinking={"type": "enabled", "budget_tokens": 16000},
                            messages=[{"role": "user", "content": instruction}],
                            **local_gen_kwargs
                        )
                        print(response)
                    else:
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=[{"role": "user", "content": instruction}],
                            **local_gen_kwargs,
                        )
                        print(response)
                    if model_name in SYSTEM_PROMPT_MODELS and "harmbench" in output_dir_base:
                        try:
                            reasoning_content, response_content = parse_reasoning_content_from_response(response, model_name)
                            result["thinking"][model_name] = reasoning_content
                            result["response"][model_name] = response_content
                            print(result)
                        except Exception:
                            result["thinking"] = {}
                            result["response"][model_name] = response.choices[0].message.content
                        success = True
                        break
                    
                    else:
                        reasoning_content, response_content = parse_reasoning_content_from_response(response, model_name)
                        result["thinking"][model_name] = reasoning_content
                        result["response"][model_name] = response_content
                        success = True
                        break

                except Exception as e:
                    print(f"[{model_name}] Error processing instruction: {instruction[:50]}... | Attempt {attempt + 1}/{max_retries} | Error: {e}")
                    time.sleep(2 ** attempt)

            if success:
                results.append(result)
                with open(output_path, 'a', encoding='utf-8') as f_out:
                    f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
            else:
                print(f"❌ Skipping instruction due to repeated failure: {instruction[:50]}...")

    instruction_chunks = [
        new_instructions[i:i + chunk_size] for i in range(0, len(new_instructions), chunk_size)
    ]

    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(process_instruction_chunk, chunk): chunk
            for chunk in instruction_chunks
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Instruction Chunks"):
            try:
                chunk_results = future.result()
                results.extend(chunk_results)
            except Exception as e:
                print(f"Error processing instruction chunk: {e}")

    return results
