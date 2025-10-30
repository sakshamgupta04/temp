"""
Utility script to check available Gemini models for your API key
Run this to find the correct model name to use
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"🔑 Using API key: {api_key[:10]}...")

# Configure Gemini
genai.configure(api_key=api_key)

print("\n" + "="*60)
print("🔍 CHECKING AVAILABLE GEMINI MODELS")
print("="*60 + "\n")

try:
    # List all models
    models = genai.list_models()
    
    # Filter models that support generateContent
    content_models = []
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            content_models.append(model)
            print(f"✅ Model: {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Supported Methods: {', '.join(model.supported_generation_methods)}")
            print(f"   Input Token Limit: {model.input_token_limit}")
            print(f"   Output Token Limit: {model.output_token_limit}")
            print("-" * 60)
    
    if content_models:
        print(f"\n✅ Found {len(content_models)} model(s) that support text generation\n")
        print("📝 RECOMMENDED MODEL TO USE:")
        # Get the model name without 'models/' prefix
        recommended = content_models[0].name.replace('models/', '')
        print(f"   {recommended}")
        print(f"\n💡 Update your resume_parser.py to use: '{recommended}'")
    else:
        print("\n❌ No models found that support generateContent")
        print("   Please check your API key and try again")

except Exception as e:
    print(f"\n❌ Error checking models: {str(e)}")
    print("\n💡 Common issues:")
    print("   1. Invalid API key")
    print("   2. API key doesn't have proper permissions")
    print("   3. Network connectivity issues")
    print("   4. API quota exceeded")
    print("\n🔗 Get your API key at: https://makersuite.google.com/app/apikey")

print("\n" + "="*60)