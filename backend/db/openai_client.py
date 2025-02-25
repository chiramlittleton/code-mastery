import openai

def generate_code_variations(code_snippet: str, num_variations: int = 5):
    """
    Uses OpenAI's GPT model to generate code variations.

    Args:
        code_snippet (str): The original code snippet.
        num_variations (int): Number of variations to generate.

    Returns:
        List[str]: A list of code variations.
    """
    prompt = f"Generate {num_variations} variations of this Python code:\n\n{code_snippet}\n\nEach variation should be slightly different but preserve the functionality."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    # Fix: New OpenAI API requires accessing choices differently
    variations = [choice.message.content for choice in response.choices]
    return variations
