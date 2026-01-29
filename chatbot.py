#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Phishing Detection Chatbot - Hugging Face Powered
Interactive chatbot for answering user queries about phishing detection and cybersecurity

Author: Phishing Detection Team
Version: 1.0
Updated: January 2026
"""

import requests
import logging
from typing import Optional, Dict, List
import streamlit as st
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CHATBOT CONFIGURATION
# ============================================================================

class PhishingChatbot:
    """
    Hugging Face powered chatbot for phishing detection queries.
    Uses conversational AI to provide helpful responses.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the chatbot with Hugging Face API.
        
        Args:
            api_key: Hugging Face API key (can also be set via environment variable HF_API_KEY)
        """
        self.api_key = api_key or st.secrets.get("HF_API_KEY", "")
        self.api_url = "https://api-inference.huggingface.co/models/gpt2"
        self.conversation_history: List[Dict] = []
        self.context_added = False
        
    def set_api_key(self, api_key: str):
        """Set or update the API key."""
        self.api_key = api_key
        
    def _add_system_context(self):
        """Add system context to conversation history once."""
        if not self.context_added:
            system_message = {
                "role": "system",
                "content": "You are an expert cybersecurity specialist helping users understand phishing detection, URL security, and online safety. Provide accurate, helpful, and educational responses. Keep answers clear and concise."
            }
            self.conversation_history.insert(0, system_message)
            self.context_added = True
    
    def build_conversation_prompt(self, user_query: str) -> str:
        """
        Build a conversation prompt from history.
        
        Args:
            user_query: Current user question
            
        Returns:
            str: Formatted prompt for the API
        """
        self._add_system_context()
        
        # Build conversation context (limit to last 5 exchanges to avoid token limits)
        recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 1 else []
        
        prompt = ""
        for msg in recent_history:
            if msg["role"] != "system":
                prompt += f"{msg['role'].upper()}: {msg['content']}\n"
        
        prompt += f"USER: {user_query}\nASSISTANT:"
        
        return prompt
    
    def get_response(self, user_query: str, use_alternative: bool = False) -> str:
        """
        Get a response from Hugging Face API.
        
        Args:
            user_query: User's question
            use_alternative: Use alternative model if primary fails
            
        Returns:
            str: Response from the API or default message
        """
        if not self.api_key or self.api_key.strip() == "":
            return self._get_fallback_response(user_query)
        
        try:
            # Build the prompt with conversation history
            prompt = self.build_conversation_prompt(user_query)
            
            # Choose model based on parameter
            if use_alternative:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 200,
                        "top_k": 50,
                        "top_p": 0.95,
                        "temperature": 0.7,
                    }
                }
                api_url = "https://api-inference.huggingface.co/models/distilgpt2"
            else:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 200,
                        "top_k": 50,
                        "top_p": 0.95,
                        "temperature": 0.7,
                    }
                }
                api_url = self.api_url
            
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse response based on model type
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    # Extract only the assistant response (remove the prompt)
                    if "ASSISTANT:" in generated_text:
                        assistant_response = generated_text.split("ASSISTANT:")[-1].strip()
                    else:
                        assistant_response = generated_text.replace(prompt, "").strip()
                    
                    response_text = assistant_response[:500]  # Limit response length
                else:
                    response_text = self._get_fallback_response(user_query)
                    
            elif response.status_code == 429:
                # Rate limited - try alternative model
                if not use_alternative:
                    logger.warning("Rate limited on primary model, trying alternative...")
                    return self.get_response(user_query, use_alternative=True)
                else:
                    response_text = self._get_fallback_response(user_query)
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                response_text = self._get_fallback_response(user_query)
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_query})
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text
            
        except requests.exceptions.Timeout:
            logger.warning("API request timeout")
            return self._get_fallback_response(user_query)
        except requests.exceptions.ConnectionError:
            logger.warning("Connection error to API")
            return self._get_fallback_response(user_query)
        except Exception as e:
            logger.error(f"Chatbot error: {str(e)}")
            return self._get_fallback_response(user_query)
    
    def _get_fallback_response(self, query: str) -> str:
        """
        Provide intelligent fallback responses when API is unavailable.
        
        Args:
            query: User's question
            
        Returns:
            str: Relevant response based on keywords
        """
        query_lower = query.lower()
        
        # Phishing-related keywords and responses
        responses = {
            "phishing": (
                "Phishing is a cyber attack where attackers impersonate legitimate organizations "
                "to steal sensitive information like passwords and credit card details. "
                "Always verify URLs, check for HTTPS, and never click suspicious links."
            ),
            "detect": (
                "To detect phishing URLs, look for: IP addresses instead of domain names, "
                "@symbols in the URL, unusually long URLs, HTTPS tokens in domain names, "
                "and unknown shortening services. Our tool analyzes 17 security features."
            ),
            "url": (
                "URLs can reveal phishing attempts through various indicators: the domain name, "
                "protocol (HTTPS vs HTTP), length, presence of special characters, "
                "and how well-established the domain is. Always hover over links to see the true URL."
            ),
            "safe": (
                "To stay safe online: enable two-factor authentication, use strong unique passwords, "
                "verify website URLs before entering information, keep software updated, "
                "and use security tools like our Phishing Detector."
            ),
            "how": (
                "Our Phishing Website Detector uses machine learning to analyze 17 security features of URLs, "
                "including domain information, traffic patterns, and structural characteristics. "
                "It then classifies URLs as legitimate or phishing with a confidence score."
            ),
            "feature": (
                "We analyze features like: IP presence, @ symbol, URL length, directory depth, "
                "redirection patterns, HTTPS in domain, URL shorteners, prefix/suffix dashes, "
                "DNS records, web traffic, domain age, and security indicators."
            ),
            "https": (
                "HTTPS (Hypertext Transfer Protocol Secure) encrypts data between your browser and the website. "
                "Always look for the padlock icon in your address bar. However, HTTPS alone doesn't guarantee "
                "a site is legitimate - phishing sites can use HTTPS too."
            ),
            "attack": (
                "Common phishing attack methods include: spoofed emails, fake login pages, "
                "malicious links, social engineering, credential harvesting, and drive-by downloads. "
                "Stay vigilant and verify sender information."
            ),
        }
        
        # Find best matching response
        for keyword, response in responses.items():
            if keyword in query_lower:
                return response
        
        # Default response
        return (
            "Great question! I'm a cybersecurity assistant specialized in phishing detection. "
            "I can help you understand URL security, phishing tactics, and how our detection system works. "
            "Feel free to ask me about any security concerns!"
        )
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.context_added = False
    
    def get_history(self) -> List[Dict]:
        """Get conversation history excluding system messages."""
        return [msg for msg in self.conversation_history if msg["role"] != "system"]
    
    def get_suggested_questions(self) -> List[str]:
        """Get list of suggested questions users can ask."""
        return [
            "What is phishing and how does it work?",
            "How can I detect a phishing URL?",
            "What features do you analyze in URLs?",
            "How do I stay safe online?",
            "What's the difference between HTTP and HTTPS?",
            "Can phishing sites use HTTPS?",
            "How does your ML model detect phishing?",
            "What are common phishing attack methods?",
            "How accurate is phishing detection?",
            "What should I do if I click a suspicious link?",
        ]


# ============================================================================
# STREAMLIT SESSION STATE MANAGEMENT
# ============================================================================

def initialize_chatbot_session():
    """Initialize chatbot in Streamlit session state."""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = PhishingChatbot()
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = False


def render_chatbot_interface():
    """
    Render the complete chatbot interface.
    This function should be called from your main Streamlit app.
    """
    initialize_chatbot_session()
    
    chatbot = st.session_state.chatbot
    
    # API Key Configuration
    with st.expander("⚙️ API Configuration", expanded=False):
        col1, col2 = st.columns([4, 1])
        with col1:
            api_key = st.text_input(
                "Hugging Face API Key",
                type="password",
                placeholder="hf_...",
                help="Get your free API key from https://huggingface.co/settings/tokens"
            )
        with col2:
            if st.button("✓ Set Key", use_container_width=True):
                if api_key:
                    chatbot.set_api_key(api_key)
                    st.session_state.api_key_set = True
                    st.success("✓ API key configured!")
                    st.rerun()
                else:
                    st.warning("Please enter an API key")
        
        st.info(
            "**Note:** Free Hugging Face API is rate-limited. For production use, "
            "consider setting up a paid API key or hosting your own model."
        )
    
    # Chat Display Area
    st.subheader("💬 Chat Interface")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])
    
    # Input Area
    st.divider()
    
    col1, col2 = st.columns([1, 20])
    
    # Suggested questions
    if len(st.session_state.chat_messages) == 0:
        st.subheader("💡 Quick Questions")
        suggested = chatbot.get_suggested_questions()
        
        cols = st.columns(2)
        for i, question in enumerate(suggested):
            with cols[i % 2]:
                if st.button(question, use_container_width=True, key=f"suggest_{i}"):
                    st.session_state.user_input = question
                    st.rerun()
    
    # User input
    user_input = st.chat_input(
        "Ask me anything about phishing detection and cybersecurity...",
        key="chat_input_field"
    )
    
    if user_input:
        # Add user message to chat
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        # Get bot response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                response = chatbot.get_response(user_input)
            st.markdown(response)
        
        # Add bot response to chat history
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
    
    # Sidebar controls
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            chatbot.clear_history()
            st.success("Chat cleared!")
            st.rerun()
    
    with col2:
        if st.button("📥 Export Chat", use_container_width=True):
            # Create exportable text
            export_text = "=== Phishing Detection Chatbot Conversation ===\n"
            export_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            export_text += "=" * 50 + "\n\n"
            
            for msg in st.session_state.chat_messages:
                export_text += f"{msg['role'].upper()}:\n{msg['content']}\n\n"
            
            st.download_button(
                label="Download Chat",
                data=export_text,
                file_name=f"phishing_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )


# ============================================================================
# STANDALONE USAGE
# ============================================================================

if __name__ == "__main__":
    st.set_page_config(page_title="Phishing Chatbot", page_icon="💬", layout="wide")
    st.title("🤖 Phishing Detection Chatbot")
    
    render_chatbot_interface()
