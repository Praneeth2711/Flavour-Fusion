import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback
import time

with open("diagnostic_log.txt", "w", encoding="utf-8") as log_file:
    def log(msg):
        print(msg)
        log_file.write(msg + "\n")
        log_file.flush()

    try:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        log(f"API Key loaded: {bool(api_key)}")
        if api_key:
            log(f"Key start: {api_key[:5]}...")
            genai.configure(api_key=api_key)
        else:
            log("ERROR: No API Key found.")

        topic = "Paneer Masala"
        word_count = 500
        prompt = (
            f"Generate a complete, engaging recipe blog post on the topic '{topic}'. "
            f"Make it exactly {word_count} words."
        )

        model_names = ['gemini-2.0-flash-lite-001', 'gemini-2.0-flash-001', 'gemini-exp-1206']
        
        for model_name in model_names:
            log(f"\n--- Testing model: {model_name} ---")
            try:
                model = genai.GenerativeModel(model_name)
                log("Model initialized.")
                
                log("Starting generation (stream=True)...")
                start_time = time.time()
                response = model.generate_content(prompt, stream=True)
                log("Request sent. Iterating stream...")
                
                chunk_count = 0
                for chunk in response:
                    chunk_count += 1
                    if chunk_count % 10 == 0:
                        log(f"Received chuck {chunk_count}...")
                
                duration = time.time() - start_time
                log(f"Success! Received {chunk_count} chunks in {duration:.2f} seconds.")
                break # Stop if successful
                
            except Exception as e:
                log(f"ERROR with {model_name}: {e}")
                traceback.print_exc(file=log_file)
                continue

    except Exception:
        log("\nFATAL ERROR:")
        traceback.print_exc(file=log_file)

