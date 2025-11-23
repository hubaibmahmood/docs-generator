"""Agent module for AI interaction."""

import json
import logging
import os
from pathlib import Path

# Corrected imports as per user request
from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    gen_trace_id,
)
from agents.run import RunConfig

from src.models.doc_gen import DocumentJob, GeneratedDocumentation

logger = logging.getLogger(__name__)

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

config = RunConfig(model=model, model_provider=external_client, trace_id=gen_trace_id())

doc_gen_agent = Agent(
    name="DocGenAgent",
    instructions=(
        "You are an AI assistant specialized in generating technical documentation "
        "for software projects. Your task is to generate a summary, API reference, "
        "and examples for a given source code file. "
        "Use the provided 'Project Context' to understand relationships between files "
        "and generate accurate cross-references where applicable. "
        "\n\n"
        "CRITICAL FORMATTING REQUIREMENTS:\n"
        "- Write natural markdown text with actual newlines between paragraphs\n"
        "- DO NOT use escaped characters like \\n or \\t in your output\n"
        "- Format multi-paragraph content naturally as you would in a text editor\n"
        "- Use proper markdown syntax: # for headers, * for lists, ``` for code blocks\n"
        "- The summary, api_reference, and examples fields should contain readable markdown\n"
        "\n"
        "When writing:\n"
        "- summary: The 'summary' field MUST be formatted with multiple paragraphs, separated by double newlines, to provide a clear and readable overview. This is a strict requirement.\n"
        "- api_reference: Document functions/classes with markdown formatting. DO NOT include a top-level '# API Reference' header in this field.\n"
        "- examples: Show code usage with markdown code blocks. DO NOT include a top-level '# Examples' header in this field.\n"
        "\n"
        "Remember: Write as if you're typing in a markdown editor, not creating JSON strings."
    ),
    output_type=GeneratedDocumentation,
)


async def generate_documentation_from_job(job: DocumentJob, retry_count: int = 0) -> GeneratedDocumentation:  # noqa: C901
    """
    Constructs a prompt, calls the LLM via Runner.run, and returns the structured output.
    """
    # Basic Context Handling: If content is too large, truncate it.
    max_content_chars = 500_000  # Arbitrary safety limit for this simplified agent

    file_content = job.content
    if len(file_content) > max_content_chars:
        logger.warning(f"File content for {job.file_path} exceeds limit. Truncating.")
        file_content = file_content[:max_content_chars] + "\n...[TRUNCATED]..."

    user_prompt = (
        f"Generate documentation for the following file:\n\n"
        f"File Path: {job.file_path}\n\n"
        f"Project Context: {json.dumps(job.context, indent=2)}\n\n"
        f"File Content:\n```\n{file_content}\n```\n\n"
        f"Code Analysis Result (relevant parts):\n```json\n"
        f"{job.analysis.model_dump_json(indent=2)}\n```\n\n"
    )

    try:
        # Use Runner.run to get structured output directly
        result = await Runner.run(doc_gen_agent, input=user_prompt, run_config=config)

        if isinstance(result.final_output, GeneratedDocumentation):
            doc = result.final_output

            # Debug: Print the raw content to see what we're working with
            # print("DEBUG - Raw summary repr:", repr(doc.summary[:100]))
            # print("DEBUG - Summary type:", type(doc.summary))

            # Try decoding if it's somehow double-encoded
            import codecs

            def decode_escapes(s: str) -> str:
                """Decode escape sequences in a string."""
                try:
                    # Try to decode unicode escape sequences
                    decoded = codecs.decode(s, "unicode_escape")
                    return decoded
                except Exception as e:
                    # If that fails, manually replace common escapes
                    return (
                        s.replace("\\n", "\n")
                        .replace("\\t", "\t")
                        .replace("\\r", "\r")
                        .replace('\\"', '"')
                        .replace("\\'", "'")
                    )

            doc.summary = decode_escapes(doc.summary)
            doc.api_reference = decode_escapes(doc.api_reference)
            doc.examples = decode_escapes(doc.examples)

            return doc
        else:
            # Fallback or error if the output isn't what we expect (shouldn't happen with output_type)
            raise ValueError(f"Unexpected output type: {type(result.final_output)}")

    except Exception as e:
        # Handle errors
        logger.error(f"Error generating documentation for {job.file_path}: {e}")
        if retry_count < 1:
            logger.info("Retrying generation...")
            return await generate_documentation_from_job(job, retry_count=1)
        raise
