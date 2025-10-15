"""
AI service for message analysis and action detection
"""

import re
from typing import Dict, List, Tuple
from app.models import ChatMessage, Log
from app.db.database import db

class AIService:
    """Service for analyzing chat messages and suggesting actions"""

    # Keywords that indicate different types of actions
    CONTACT_KEYWORDS = [
        'client', 'customer', 'prospect', 'lead', 'contact',
        'met with', 'spoke to', 'talked to', 'called'
    ]

    DEAL_KEYWORDS = [
        'deal', 'opportunity', 'sale', 'purchase', 'buy',
        'price', 'pricing', 'cost', 'budget', 'proposal'
    ]

    NOTE_KEYWORDS = [
        'notes', 'summary', 'discussed', 'mentioned', 'conversation',
        'meeting notes', 'call notes', 'follow up'
    ]

    TASK_KEYWORDS = [
        'todo', 'task', 'follow up', 'call back', 'email',
        'send', 'remind', 'schedule', 'meeting'
    ]

    @staticmethod
    def analyze_message(message_text: str) -> Dict[str, List[str]]:
        """Analyze message and return suggested actions"""
        message_lower = message_text.lower()

        suggestions = {
            'contacts': [],
            'deals': [],
            'notes': [],
            'tasks': []
        }

        # Check for contact mentions
        if any(keyword in message_lower for keyword in AIService.CONTACT_KEYWORDS):
            suggestions['contacts'].append('Potential client mentioned - consider creating contact')

        # Check for deal opportunities
        if any(keyword in message_lower for keyword in AIService.DEAL_KEYWORDS):
            suggestions['deals'].append('Business opportunity detected - consider creating deal')

        # Check for notes/summaries
        if any(keyword in message_lower for keyword in AIService.NOTE_KEYWORDS):
            suggestions['notes'].append('Meeting/conversation summary - create note')

        # Check for tasks
        if any(keyword in message_lower for keyword in AIService.TASK_KEYWORDS):
            suggestions['tasks'].append('Action items detected - create tasks')

        return suggestions

    @staticmethod
    def extract_contact_info(message_text: str) -> Dict[str, str]:
        """Extract potential contact information from message"""
        contact_info = {}

        # Look for phone numbers
        phone_pattern = r'\+?\d{10,15}'
        phone_match = re.search(phone_pattern, message_text)
        if phone_match:
            contact_info['phone'] = phone_match.group()

        # Look for email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, message_text)
        if email_match:
            contact_info['email'] = email_match.group()

        # Look for names (basic pattern)
        name_pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
        name_match = re.search(name_pattern, message_text)
        if name_match:
            contact_info['firstname'] = name_match.group(1)
            contact_info['lastname'] = name_match.group(2)

        return contact_info

    @staticmethod
    def extract_deal_info(message_text: str) -> Dict[str, str]:
        """Extract potential deal information from message"""
        deal_info = {}

        # Look for amounts
        amount_pattern = r'\$?\d{1,3}(?:,?\d{3})*(?:\.\d{2})?'
        amount_match = re.search(amount_pattern, message_text)
        if amount_match:
            deal_info['amount'] = amount_match.group().replace('$', '').replace(',', '')

        # Look for company names (basic pattern)
        company_pattern = r'\b(?:at|@|for)\s+([A-Z][a-zA-Z\s&]+)'
        company_match = re.search(company_pattern, message_text)
        if company_match:
            deal_info['company'] = company_match.group(1).strip()

        return deal_info

    @staticmethod
    def should_create_log(message: ChatMessage) -> bool:
        """Determine if message should generate a log"""
        suggestions = AIService.analyze_message(message.message_text)

        # Create log if any suggestions are found
        return any(suggestions.values())

    @staticmethod
    def suggest_log_type(message_text: str) -> str:
        """Suggest the most appropriate log type for a message"""
        suggestions = AIService.analyze_message(message_text)

        # Priority order for log types
        if suggestions['tasks']:
            return 'task'
        elif suggestions['notes']:
            return 'note'
        elif suggestions['deals']:
            return 'deal'
        elif suggestions['contacts']:
            return 'contact_action'
        else:
            return 'communication'
