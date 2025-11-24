"""Agent module for AI interaction."""

import json
import logging
import os
from typing import Union

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    gen_trace_id,
)
from agents.run import RunConfig

from src.models.doc_gen import DocSectionJob, GeneratedSection

logger = logging.getLogger(__name__)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

config = RunConfig(model=model, model_provider=external_client, trace_id=gen_trace_id())

doc_gen_agent = Agent(
    name="DocGenAgent",
    instructions=(
        "You are an Expert Technical Writer specialized in creating cohesive software documentation. "
        "Your goal is to generate high-quality Markdown documentation based on the provided Project Context. "
        "\n\n"
        "GUIDELINES:\n"
        "- Output PURE MARKDOWN only. Do not wrap in JSON.\n"
        "- Use proper headers (#, ##, ###) to structure the document.\n"
        "- Ensure code blocks use correct syntax highlighting (e.g., ```python).\n"
        "- Be concise but thorough.\n"
        "- Do not include conversational filler (e.g., 'Here is the README'). Start directly with the content.\n"
        "- If the context is insufficient, state clearly what is missing or infer reasonable defaults based on standard Python/Software practices."
    ),
    # No output_type means we get raw text
)


async def generate_section(job: DocSectionJob, retry_count: int = 0) -> GeneratedSection:
    """
    Constructs a prompt, calls the LLM via Runner.run, and returns the Markdown content.
    """
    # Safety truncation for context
    max_context_chars = 800_000 
    
    context_content = job.context_content
    if len(context_content) > max_context_chars:
        logger.warning(f"Context for {job.section_name} exceeds limit. Truncating.")
        context_content = context_content[:max_context_chars] + "\n...[TRUNCATED]..."

    user_prompt = (
        f"TASK: {job.prompt_instruction}\n\n"
        f"--- PROJECT CONTEXT START ---\n"
        f"{context_content}\n"
        f"--- PROJECT CONTEXT END ---\n\n"
        f"Please generate the {job.output_filename} file content now."
    )

    try:
        result = await Runner.run(doc_gen_agent, input=user_prompt, run_config=config)
        
        # The result.final_output should be a string for text-only agents
        content = str(result.final_output)

        # Basic cleanup: Remove markdown fences if the model wrapped the whole thing
        if content.strip().startswith("```markdown"):
            content = content.strip()[11:]
            if content.endswith("```"):
                content = content[:-3]
        elif content.strip().startswith("```"):
             content = content.strip()[3:]
             if content.endswith("```"):
                content = content[:-3]

        return GeneratedSection(content=content, title=job.section_name)

    except Exception as e:
        logger.error(f"Error generating section {job.section_name}: {e}")
        if retry_count < 1:
            logger.info("Retrying generation...")
            return await generate_section(job, retry_count=1)
        raise