import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random
import time

# Load environment variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- Milestone 3: Joke Generation ---
def get_joke():
    """Returns a random programmer joke."""
    jokes = [
        "Why did the programmer quit his job? Didn't get arrays.",
        "Why do programmers prefer dark mode? Light attracts bugs.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "What is a programmer's favorite hangout place? Foo Bar.",
        "Why do Java programmers wear glasses? Because they don't C#.",
        "What do you call a programmer from Finland? Nerdic.",
        "0 is false and 1 is true, right? 1.",
        "Why was the JavaScript developer sad? Because he didn't strictly equal happy.",
        "Why did the database administrator leave his wife? She had one-to-many relationships.",
        "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'"
    ]
    return random.choice(jokes)

# --- Milestone 4: Recipe Generation ---
def recipe_generation(topic, word_count):
    """
    Generates a recipe blog post using Gemini 1.5 Flash.
    """
    if not api_key:
        st.error("Error: Google API Key not found. Please set GOOGLE_API_KEY in .env file.")
        return None

    # Try multiple model names for robustness
    # Try multiple model names for robustness
    # prioritizing newer flash/lite models which are faster and often have separate quotas
    model_names = ['gemini-2.5-flash', 'gemini-flash-lite-latest', 'gemini-2.0-flash-lite-001']
    last_exception = None

    import time # Ensure time is imported (it is not at top level, checking... wait, I need to check imports)
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            
            # Construct prompt
            prompt = (
                f"Generate a complete, engaging recipe blog post on the topic '{topic}'. "
                f"Make it exactly {word_count} words. "
                "Structure: Title, intro, ingredients list, step-by-step instructions, tips, serving suggestions, garnish. "
                "Make it detailed, flavorful, professional like a food blog. "
                "Include prep/cook time, servings 4-6."
            )
            
            # Helper to attempt generation
            def attempt_generate():
                return model.generate_content(prompt, stream=True)

            try:
                # First attempt
                response = attempt_generate()
                return response
            except Exception as e:
                # Check for rate limit
                if "429" in str(e):
                    st.warning(f"High traffic (Rate Limit). Retrying in 20 seconds with {model_name}...")
                    time.sleep(20) # Wait 20 seconds
                    try:
                        # Retry once
                        response = attempt_generate()
                        st.success("Retry successful!")
                        return response
                    except Exception as retry_e:
                        # If retry fails, log it and continue to next model
                        last_exception = retry_e
                        continue
                else:
                    raise e # Re-raise other errors to be caught by outer except
                
        except Exception as e:
            last_exception = e
            # Continue to the next model if accessible
            continue

    # If all attempts fail, handle the last exception
    if last_exception:
        error_msg = str(last_exception)
        if "404" in error_msg:
            st.error(f"Error: Model not found ({model_name}). Please check your API key permissions.")
        elif "429" in error_msg:
            st.error("Error: Rate limit exceeded (Quota exceeded). Please try again later.")
        else:
            st.error(f"Error generating recipe: {error_msg}")
    else:
        st.error("Error: Failed to generate recipe. Please try again.")
        
    return None

# --- Milestone 5: Streamlit UI ---
def main():
    st.set_page_config(page_title="Flavour Fusion: AI-Driven Recipe Blogging", layout="wide", initial_sidebar_state="expanded", page_icon="🍳")

    # Custom CSS for "Antigravity" Theme
    st.markdown("""
        <style>
        /* Import Futuristic Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@300;400;600&display=swap');

        :root {
            --primary-neon: #a855f7; /* Purple Neon */
            --secondary-neon: #06b6d4; /* Cyan Neon */
            --bg-deep: #030712;
            --glass-bg: rgba(17, 24, 39, 0.6);
            --glass-border: rgba(168, 85, 247, 0.3);
            --text-glow: 0 0 10px rgba(168, 85, 247, 0.5);
        }

        /* Deep Space Background */
        .stApp {
            background-color: var(--bg-deep);
            background-image: 
                radial-gradient(at 0% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.15) 0px, transparent 50%);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar Glass */
        [data-testid="stSidebar"] {
            background-color: rgba(3, 7, 18, 0.8);
            backdrop-filter: blur(12px);
            border-right: 1px solid var(--glass-border);
        }

        /* Typography - Sci-Fi Headers */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            background: linear-gradient(90deg, #fff, #a855f7, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
            letter-spacing: 1px;
        }
        
        div[class*="stMarkdown"] p {
            color: #d1d5db;
        }

        /* Floating Inputs */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 12px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus, 
        .stNumberInput > div > div > input:focus {
            border-color: var(--secondary-neon);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
            background: rgba(255, 255, 255, 0.1);
        }

        /* Neon Buttons */
        .stButton > button {
            background: linear-gradient(45deg, var(--primary-neon), var(--secondary-neon));
            border: none;
            color: white;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            padding: 0.8rem;
            border-radius: 12px;
            transition: all 0.4s ease;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.6);
        }

        /* Antigravity Card Effect */
        .recipe-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 2.5rem;
            margin-top: 2rem;
            box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5);
            animation: float 6s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }

        /* Glowing Border on Card */
        .recipe-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 20px;
            padding: 2px;
            background: linear-gradient(45deg, transparent, var(--primary-neon), transparent);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0.5;
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        </style>
    """, unsafe_allow_html=True)

    # Header with Center Alignment
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'>FLAVOUR FUSION</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a855f7; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;'>AI-Driven Recipe Blogging</p>", unsafe_allow_html=True)
    
    st.markdown("---")

    # Layout: Main Page Inputs
    st.markdown("### 🍳 Recipe Details")
    
    # Create columns for better layout
    input_col1, input_col2 = st.columns([3, 1])
    
    with input_col1:
        topic = st.text_input("Topic", placeholder="e.g., Malai Kofta", help="Enter the name of the dish you want a recipe for.")
    
    with input_col2:
        word_count = st.number_input("Number of words", min_value=100, max_value=2000, value=500, step=50, help="Length of your blog post.")
    
    st.markdown("###") # Spacer
    generate_btn = st.button("Generate Recipe")
    
    st.markdown("---")

    # Initialize session state for recipe
    if 'recipe' not in st.session_state:
        st.session_state.recipe = None
    if 'generated_topic' not in st.session_state:
        st.session_state.generated_topic = ""

    # Main Content Area
    if generate_btn:
        if not topic:
            st.warning("Please enter a recipe topic first!")
        else:
            # Show loading message and joke
            joke = get_joke()
            st.info(f"Cooking up your recipe... 🍳")
            st.success(f"While you wait: {joke}")
            
            # Create a placeholder for the streaming output
            recipe_placeholder = st.empty()
            full_recipe_text = ""
            
            try:
                # Get response iterator (stream)
                response_stream = recipe_generation(topic, word_count)
                
                if response_stream:
                    # Iterate through the stream and update the UI
                    for chunk in response_stream:
                        if chunk.text:
                            full_recipe_text += chunk.text
                            # Update the placeholder with the current accumulated text
                            # Wrapping in div for styling continuity during stream
                            recipe_placeholder.markdown(f'<div class="recipe-card">{full_recipe_text}</div>', unsafe_allow_html=True)
                    
                    # Store the complete recipe in session state
                    st.session_state.recipe = full_recipe_text.strip()
                    st.session_state.generated_topic = topic
                    
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")

    # Display Recipe if it exists in session state (and we are not currently generating)
    # If we just generated (generate_btn is True), the placeholder above handled the display.
    # On rerun (generate_btn is False), this block handles the display.
    if st.session_state.recipe and not generate_btn:
        st.markdown(f"### Recipe for: {st.session_state.generated_topic}")
        st.markdown(f'<div class="recipe-card">{st.session_state.recipe}</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #888;">
            <p>Hello I'm recipeMaster, your friendly robot. Let's create a fantastic recipe together!</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
