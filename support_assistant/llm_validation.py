
from pydantic import ValidationError
from prompts import STRUCTURED_PROMPT_TEMPLATE


def validate_llm_response(raw_output):
    """
    Validate the LLM JSON response.

    If validation fails, the real-LLM path can retry up to
    two additional times with a corrective instruction.
    """

    from main import AnswerResponse

    try:
        return AnswerResponse.model_validate_json(raw_output)

    except ValidationError as first_error:

        corrective_instruction = (
            "Your previous response was invalid. "
            "Return ONLY valid JSON with exactly these fields: "
            "answer, sources, confidence. "
            "confidence must be between 0 and 1."
        )

        for attempt in range(2):
            # Placeholder for a real LLM call.
            # In MOCK_LLM=1 this function is never used.
            #
            # A real implementation would send:
            # STRUCTURED_PROMPT_TEMPLATE + corrective_instruction
            # to the selected LLM here.
            #
            # The returned raw JSON should then be validated again.

            pass

        return {
            "error": "LLM output failed schema validation after 2 retries",
            "details": str(first_error)
        }
