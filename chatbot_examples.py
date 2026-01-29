#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chatbot Usage Examples - How to Use the Chatbot Module

This file shows various ways to use the PhishingChatbot class
both standalone and within Streamlit applications.

Usage:
    python chatbot_examples.py
"""

from chatbot import PhishingChatbot, render_chatbot_interface, initialize_chatbot_session
import streamlit as st

# ============================================================================
# EXAMPLE 1: BASIC USAGE (Standalone)
# ============================================================================

def example_basic_usage():
    """
    Basic example: Initialize and get a response.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage (Standalone)")
    print("="*60 + "\n")
    
    # Initialize chatbot (API key from environment or secrets)
    bot = PhishingChatbot()
    
    # Get a response
    user_query = "What is phishing?"
    print(f"User: {user_query}")
    
    response = bot.get_response(user_query)
    print(f"Bot: {response}\n")


# ============================================================================
# EXAMPLE 2: CUSTOM API KEY
# ============================================================================

def example_custom_api_key():
    """
    Example: Use a custom API key directly.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom API Key")
    print("="*60 + "\n")
    
    # Initialize with specific API key
    bot = PhishingChatbot(api_key="hf_YOUR_API_KEY_HERE")
    
    # You can also set it later
    # bot.set_api_key("hf_YOUR_API_KEY_HERE")
    
    user_query = "How do I detect phishing URLs?"
    print(f"User: {user_query}")
    
    response = bot.get_response(user_query)
    print(f"Bot: {response}\n")


# ============================================================================
# EXAMPLE 3: CONVERSATION HISTORY
# ============================================================================

def example_conversation_history():
    """
    Example: Maintain conversation history.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Conversation History")
    print("="*60 + "\n")
    
    bot = PhishingChatbot()
    
    # Multi-turn conversation
    queries = [
        "What is phishing?",
        "How can I protect myself?",
        "What about HTTPS?"
    ]
    
    for query in queries:
        print(f"User: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}\n")
        print("-" * 40)
    
    # View conversation history
    print("\nConversation History:")
    history = bot.get_history()
    for msg in history:
        print(f"{msg['role'].upper()}: {msg['content'][:100]}...")


# ============================================================================
# EXAMPLE 4: FALLBACK RESPONSES
# ============================================================================

def example_fallback_responses():
    """
    Example: Use fallback responses without API.
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Fallback Responses (No API)")
    print("="*60 + "\n")
    
    # Initialize without API key
    bot = PhishingChatbot(api_key="")
    
    test_queries = [
        "What is phishing?",
        "How do I detect URLs?",
        "How do I stay safe online?",
        "Tell me about HTTPS",
        "Random question about something"
    ]
    
    for query in test_queries:
        print(f"User: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")
        print()


# ============================================================================
# EXAMPLE 5: STREAMLIT INTEGRATION
# ============================================================================

def example_streamlit_integration():
    """
    Example: Embed chatbot in Streamlit app.
    """
    
    st.set_page_config(page_title="Chatbot Example", page_icon="🤖")
    st.title("🤖 Chatbot Example")
    
    # Initialize chatbot in session state
    initialize_chatbot_session()
    
    # Render the full chatbot interface
    render_chatbot_interface()


# ============================================================================
# EXAMPLE 6: CUSTOM WRAPPER
# ============================================================================

def example_custom_wrapper():
    """
    Example: Create a custom wrapper around chatbot.
    """
    
    class CustomChatbot:
        """Wrapper with additional features."""
        
        def __init__(self, api_key=None):
            self.bot = PhishingChatbot(api_key=api_key)
            self.session_start = None
            self.message_count = 0
        
        def ask(self, query):
            """Ask a question and track metrics."""
            self.message_count += 1
            response = self.bot.get_response(query)
            return response
        
        def get_stats(self):
            """Get conversation statistics."""
            return {
                "messages_sent": self.message_count,
                "history_length": len(self.bot.get_history()),
                "history": self.bot.get_history()
            }
    
    print("\n" + "="*60)
    print("EXAMPLE 6: Custom Wrapper")
    print("="*60 + "\n")
    
    # Use custom wrapper
    chat = CustomChatbot()
    
    # Ask questions
    for query in ["What is phishing?", "How do I stay safe?"]:
        response = chat.ask(query)
        print(f"User: {query}")
        print(f"Bot: {response}\n")
    
    # Get stats
    stats = chat.get_stats()
    print(f"Stats: {stats}")


# ============================================================================
# EXAMPLE 7: BATCH PROCESSING
# ============================================================================

def example_batch_processing():
    """
    Example: Process multiple queries in batch.
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: Batch Processing")
    print("="*60 + "\n")
    
    bot = PhishingChatbot()
    
    queries = [
        "What is phishing?",
        "How to detect phishing?",
        "How to stay safe?",
    ]
    
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] Processing: {query}")
        response = bot.get_response(query)
        results.append({
            "query": query,
            "response": response
        })
    
    print(f"\nProcessed {len(results)} queries successfully!")


# ============================================================================
# EXAMPLE 8: ADVANCED STREAMLIT
# ============================================================================

def example_advanced_streamlit():
    """
    Example: Advanced Streamlit integration with custom UI.
    """
    
    st.set_page_config(page_title="Advanced Chatbot", layout="wide")
    
    # Sidebar configuration
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        api_key = st.text_input(
            "Hugging Face API Key",
            type="password",
            help="Get from https://huggingface.co/settings/tokens"
        )
        
        if api_key:
            st.session_state.api_key = api_key
    
    # Main content
    st.title("🤖 Advanced Chatbot Demo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Chat History")
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        
        # Display messages
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    
    with col2:
        st.subheader("Statistics")
        st.metric("Messages", len(st.session_state.chat_messages))
        st.metric("Turn Count", len(st.session_state.chat_messages) // 2)
    
    # Input
    user_input = st.chat_input("Ask me anything...")
    
    if user_input:
        # Initialize chatbot
        if "chatbot" not in st.session_state:
            api_key = st.session_state.get("api_key")
            st.session_state.chatbot = PhishingChatbot(api_key=api_key)
        
        # Get response
        response = st.session_state.chatbot.get_response(user_input)
        
        # Add to messages
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Run examples menu."""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║         PHISHING CHATBOT - USAGE EXAMPLES                 ║
║                                                            ║
║  This script demonstrates various ways to use the         ║
║  PhishingChatbot class both standalone and with Streamlit ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📋 Available Examples:\n")
    print("  1. Basic Usage (Standalone)")
    print("  2. Custom API Key")
    print("  3. Conversation History")
    print("  4. Fallback Responses (No API)")
    print("  5. Streamlit Integration")
    print("  6. Custom Wrapper Class")
    print("  7. Batch Processing")
    print("  8. Advanced Streamlit (Run with 'streamlit run')")
    print("  0. Exit")
    
    while True:
        print()
        choice = input("Select example (0-8): ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            example_basic_usage()
        elif choice == "2":
            example_custom_api_key()
        elif choice == "3":
            example_conversation_history()
        elif choice == "4":
            example_fallback_responses()
        elif choice == "5":
            print("\n⚠️  Run this example with: streamlit run chatbot_examples.py --logger.level=debug")
            # Uncomment below to run as Streamlit app
            # example_streamlit_integration()
        elif choice == "6":
            example_custom_wrapper()
        elif choice == "7":
            example_batch_processing()
        elif choice == "8":
            print("\n⚠️  Run this example with: streamlit run chatbot_examples.py")
            # Uncomment below to run as Streamlit app
            # example_advanced_streamlit()
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    # Check if running as Streamlit app
    try:
        if st.session_state:
            # Running as Streamlit
            example_advanced_streamlit()
    except:
        # Running as standalone script
        main()
