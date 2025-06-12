import json
import logging
from openai import OpenAI
from config import OPENAI_API_KEY
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("OpenAI service initialized successfully")

    def summarize_document(self, text: str) -> Dict[str, Any]:
        """
        Summarize document content using OpenAI
        
        Args:
            text (str): Document text content
            
        Returns:
            Dict[str, Any]: Summary result
        """
        try:
            prompt = f"""
            Please summarize the following document into a concise paragraph that captures the main points and key information:
            
            {text}
            
            Provide a clear, informative summary that maintains the essential details while being significantly shorter than the original.
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary)
            }
            
        except Exception as e:
            logger.error(f"Error in document summarization: {e}")
            return {
                "success": False,
                "error": f"Summarization failed: {str(e)}"
            }

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of document content
        
        Args:
            text (str): Document text content
            
        Returns:
            Dict[str, Any]: Sentiment analysis result
        """
        try:
            prompt = f"""
            Analyze the sentiment of the following text and provide:
            1. Overall sentiment (positive, negative, or neutral)
            2. Confidence score (0.0 to 1.0)
            3. Brief explanation of the sentiment analysis
            
            Text to analyze:
            {text}
            
            Respond in JSON format with the following structure:
            {{
                "sentiment": "positive/negative/neutral",
                "confidence": 0.85,
                "explanation": "Brief explanation of the sentiment analysis"
            }}
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=300,
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "sentiment": result.get("sentiment"),
                "confidence": result.get("confidence"),
                "explanation": result.get("explanation")
            }
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                "success": False,
                "error": f"Sentiment analysis failed: {str(e)}"
            }

    def extract_keywords(self, text: str) -> Dict[str, Any]:
        """
        Extract important keywords from document content
        
        Args:
            text (str): Document text content
            
        Returns:
            Dict[str, Any]: Keywords extraction result
        """
        try:
            prompt = f"""
            Extract the most important keywords and key phrases from the following text.
            Focus on:
            - Important nouns and proper nouns
            - Key concepts and themes
            - Technical terms
            - Names of people, places, organizations
            
            Text to analyze:
            {text}
            
            Respond in JSON format with a list of keywords:
            {{
                "keywords": ["keyword1", "keyword2", "keyword3", ...]
            }}
            
            Limit to the top 15 most important keywords.
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=400,
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "keywords": result.get("keywords", []),
                "count": len(result.get("keywords", []))
            }
            
        except Exception as e:
            logger.error(f"Error in keyword extraction: {e}")
            return {
                "success": False,
                "error": f"Keyword extraction failed: {str(e)}"
            }

    def translate_text(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translate document content to target language
        
        Args:
            text (str): Document text content
            target_language (str): Target language for translation
            
        Returns:
            Dict[str, Any]: Translation result
        """
        try:
            prompt = f"""
            Translate the following text to {target_language}.
            Maintain the original meaning, tone, and structure as much as possible.
            
            Text to translate:
            {text}
            
            Provide only the translated text without any additional commentary.
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "translated_text": translated_text,
                "source_language": "auto-detected",
                "target_language": target_language,
                "original_length": len(text),
                "translated_length": len(translated_text)
            }
            
        except Exception as e:
            logger.error(f"Error in translation: {e}")
            return {
                "success": False,
                "error": f"Translation failed: {str(e)}"
            }

    def structure_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured data from document content
        
        Args:
            text (str): Document text content
            
        Returns:
            Dict[str, Any]: Structured data extraction result
        """
        try:
            prompt = f"""
            Extract structured data from the following text. Look for and extract:
            - Names (people, organizations, locations)
            - Dates and times
            - Numbers and amounts (monetary, quantities, percentages)
            - Contact information (emails, phone numbers, addresses)
            - Key entities and their relationships
            
            Text to analyze:
            {text}
            
            Respond in JSON format with the following structure:
            {{
                "names": {{
                    "people": ["person1", "person2"],
                    "organizations": ["org1", "org2"],
                    "locations": ["location1", "location2"]
                }},
                "dates": ["date1", "date2"],
                "amounts": {{
                    "monetary": ["$100", "$200"],
                    "quantities": ["50 units", "25%"],
                    "numbers": ["100", "200"]
                }},
                "contact_info": {{
                    "emails": ["email1", "email2"],
                    "phones": ["phone1", "phone2"],
                    "addresses": ["address1", "address2"]
                }},
                "key_entities": ["entity1", "entity2"]
            }}
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "structured_data": result
            }
            
        except Exception as e:
            logger.error(f"Error in data structuring: {e}")
            return {
                "success": False,
                "error": f"Data structuring failed: {str(e)}"
            }

    def detect_topics(self, text: str) -> Dict[str, Any]:
        """
        Identify primary topics in document content
        
        Args:
            text (str): Document text content
            
        Returns:
            Dict[str, Any]: Topic detection result
        """
        try:
            prompt = f"""
            Identify the primary topics and themes discussed in the following text.
            Categorize the content and provide:
            - Main topics (up to 8 topics)
            - Brief description for each topic
            - Confidence score for each topic (0.0 to 1.0)
            
            Text to analyze:
            {text}
            
            Respond in JSON format:
            {{
                "topics": [
                    {{
                        "name": "Topic Name",
                        "description": "Brief description of the topic",
                        "confidence": 0.85
                    }}
                ]
            }}
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=600,
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "topics": result.get("topics", []),
                "topic_count": len(result.get("topics", []))
            }
            
        except Exception as e:
            logger.error(f"Error in topic detection: {e}")
            return {
                "success": False,
                "error": f"Topic detection failed: {str(e)}"
            }
