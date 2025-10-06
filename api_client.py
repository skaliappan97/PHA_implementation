import google.generativeai as genai
import os

# --- 1. INITIALIZE THE GEMINI CLIENT ---
# This code securely reads your API key from the environment variables.
# It's wrapped in a try-except block to give a helpful message if the key is missing.
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    print("✅ Gemini API client initialized successfully")
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please make sure your GOOGLE_API_KEY environment variable is set.")

# --- 2. CREATE A REUSABLE FUNCTION ---
def call_gemini(system_prompt: str, user_prompt: str, model: str = "gemini-2.5-flash", temperature: float = 0.5, max_tokens: int = 8192):
    """
    A wrapper function to call the Google Gemini API with system prompt support.

    Args:
        system_prompt (str): Defines the agent's role, personality, and high-level instructions.
                             This is where you'll put the prompts from the paper.
        user_prompt (str): The specific task or query for the agent in this turn.
        model (str): The Gemini model to use (default: gemini-1.5-pro).
        temperature (float): Controls randomness (0.0-1.0). Lower is more predictable, higher is more creative.
        max_tokens (int): Maximum length of the response.

    Returns:
        str: The text content of Gemini's response, or an error message.
    """
    try:
        # Initialize the model with generation config
        gen_model = genai.GenerativeModel(
            model_name=model,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )

        # Gemini doesn't have a separate system parameter, so we prepend it to the user message
        # This is a common pattern for models without explicit system prompt support
        combined_prompt = f"{system_prompt}\n\n---\n\nUser Query: {user_prompt}"

        # Generate response
        response = gen_model.generate_content(combined_prompt)

        # Extract and return the text
        return response.text

    except Exception as e:
        # Return a clear error message if the API call fails for any reason.
        return f"An error occurred with the Gemini API call: {e}"

# --- 3. (OPTIONAL) ADD A TEST BLOCK ---
# This part allows you to run this file directly to test if your setup is working.
if __name__ == "__main__":
    print("\nTesting the Gemini API client...")

    # A simple test to see if we can get a response.
    test_system_prompt = "You are a helpful assistant specializing in health and wellness."
    test_user_prompt = "Hello! In one sentence, what is the key to a good API client?"

    response = call_gemini(test_system_prompt, test_user_prompt)

    print("\n--- Test Response ---")
    print(response)
    print("---------------------\n")

    if "An error occurred" in response:
        print("❌ Test Failed. Please check your API key and environment setup.")
    else:
        print("✅ Test Successful! Your Gemini API client is ready to be used by your agents.")
