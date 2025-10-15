"""
HubSpot API integration service
"""

import requests
import time
from datetime import datetime
from flask import current_app
from app.core.security import SecurityService
from app.models import User, Log, ChatSession, ChatMessage
from app.db.database import db

class HubSpotService:
    """Service for HubSpot API interactions"""

    @staticmethod
    def get_hubspot_token():
        """Get HubSpot PAT from environment"""
        token = current_app.config.get('HUBSPOT_ACCESS_TOKEN')
        if not token:
            raise ValueError('HUBSPOT_ACCESS_TOKEN not configured in environment')
        return token

    @staticmethod
    def get_base_url():
        """Get HubSpot base URL"""
        return current_app.config.get('HUBSPOT_API_URL', 'https://api.hubapi.com')

    @staticmethod
    def get_headers():
        """Get standard HubSpot API headers"""
        token = HubSpotService.get_hubspot_token()
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def make_request(method, endpoint, data=None, params=None):
        """Make authenticated request to HubSpot API"""
        url = f"{HubSpotService.get_base_url()}{endpoint}"
        headers = HubSpotService.get_headers()

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params
        )

        return response

    # ========== CONTACT OPERATIONS ==========

    @staticmethod
    def get_contacts(limit=10, **filters):
        """Get HubSpot contacts"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/contacts', params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def create_contact(contact_data, session_id=None, message_id=None, user_id=None):
        """Create contact in HubSpot"""
        response = HubSpotService.make_request('POST', '/crm/v3/objects/contacts', {'properties': contact_data})

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'contact_action', hubspot_id,
                f"Contact created: {contact_data.get('email', 'N/A')}"
            )
            return {'success': True, 'hubspot_id': hubspot_id, 'data': response.json()}
        else:
            error_msg = response.text
            HubSpotService._create_failed_log(
                user_id, session_id, message_id, 'contact_action', error_msg
            )
            return {'success': False, 'error': error_msg}

    @staticmethod
    def get_contact_properties():
        """Get available contact properties"""
        response = HubSpotService.make_request('GET', '/crm/v3/properties/contacts')
        return response

    # ========== DEAL OPERATIONS ==========

    @staticmethod
    def get_deals(limit=10, **filters):
        """Get HubSpot deals"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/deals', params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def create_deal(deal_data, associations=None, session_id=None, message_id=None, user_id=None):
        """Create deal in HubSpot"""
        payload = {'properties': deal_data}
        if associations:
            payload['associations'] = associations

        response = HubSpotService.make_request('POST', '/crm/v3/objects/deals', payload)

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'deal', hubspot_id,
                f"Deal created: {deal_data.get('dealname', 'N/A')}"
            )
            return {'success': True, 'hubspot_id': hubspot_id, 'data': response.json()}
        else:
            error_msg = response.text
            HubSpotService._create_failed_log(
                user_id, session_id, message_id, 'deal', error_msg
            )
            return {'success': False, 'error': error_msg}

    @staticmethod
    def get_deal_pipelines():
        """Get deal pipelines"""
        response = HubSpotService.make_request('GET', '/crm/v3/pipelines/deals')
        return response

    # ========== NOTE OPERATIONS ==========

    @staticmethod
    def get_notes(limit=10, **filters):
        """Get HubSpot notes"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/notes', params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def create_note(note_data, associations=None, session_id=None, message_id=None, user_id=None):
        """Create note in HubSpot"""
        payload = {'properties': note_data}
        if associations:
            payload['associations'] = associations

        response = HubSpotService.make_request('POST', '/crm/v3/objects/notes', payload)

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'note', hubspot_id,
                f"Note created: {note_data.get('hs_note_body', 'N/A')[:50]}..."
            )
            return {'success': True, 'hubspot_id': hubspot_id, 'data': response.json()}
        else:
            error_msg = response.text
            HubSpotService._create_failed_log(
                user_id, session_id, message_id, 'note', error_msg
            )
            return {'success': False, 'error': error_msg}

    # ========== TASK OPERATIONS ==========

    @staticmethod
    def get_tasks(limit=10, **filters):
        """Get HubSpot tasks"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/tasks', params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def create_task(task_data, associations=None, session_id=None, message_id=None, user_id=None):
        """Create task in HubSpot"""
        payload = {'properties': task_data}
        if associations:
            payload['associations'] = associations

        response = HubSpotService.make_request('POST', '/crm/v3/objects/tasks', payload)

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'task', hubspot_id,
                f"Task created: {task_data.get('hs_task_subject', 'N/A')}"
            )
            return {'success': True, 'hubspot_id': hubspot_id, 'data': response.json()}
        else:
            error_msg = response.text
            HubSpotService._create_failed_log(
                user_id, session_id, message_id, 'task', error_msg
            )
            return {'success': False, 'error': error_msg}

    # ========== MEETING OPERATIONS ==========

    @staticmethod
    def get_meetings(limit=10, **filters):
        """Get HubSpot meetings"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/meetings', params=params)
        return response

    @staticmethod
    def create_meeting(meeting_data, associations=None, session_id=None, message_id=None, user_id=None):
        """Create meeting in HubSpot"""
        payload = {'properties': meeting_data}
        if associations:
            payload['associations'] = associations

        response = HubSpotService.make_request('POST', '/crm/v3/objects/meetings', payload)

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'call_meeting', hubspot_id,
                f"Meeting created: {meeting_data.get('hs_meeting_title', 'N/A')}"
            )
            return {'success': True, 'hubspot_id': hubspot_id, 'data': response.json()}
        else:
            error_msg = response.text
            HubSpotService._create_failed_log(
                user_id, session_id, message_id, 'call_meeting', error_msg
            )
            return {'success': False, 'error': error_msg}

    # ========== COMPANY OPERATIONS ==========

    @staticmethod
    def get_companies(limit=10, **filters):
        """Get HubSpot companies"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/companies', params=params)
        return response

    @staticmethod
    def create_company(company_data, session_id=None, message_id=None, user_id=None):
        """Create company in HubSpot"""
        response = HubSpotService.make_request('POST', '/crm/v3/objects/companies', {'properties': company_data})

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'contact_action', hubspot_id,
                f"Company created: {company_data.get('name', 'N/A')}"
            )
            return {'success': True, 'hubspot_id': hubspot_id, 'data': response.json()}
        else:
            error_msg = response.text
            HubSpotService._create_failed_log(
                user_id, session_id, message_id, 'contact_action', error_msg
            )
            return {'success': False, 'error': error_msg}

    # ========== OWNER OPERATIONS ==========

    @staticmethod
    def get_owners(limit=10):
        """Get HubSpot owners"""
        params = {'limit': limit}
        response = HubSpotService.make_request('GET', '/crm/v3/owners', params=params)
        return response

    # ========== LOGGING OPERATIONS ==========

    @staticmethod
    def _create_success_log(user_id, session_id, message_id, log_type, hubspot_id, description=None):
        """Create successful sync log"""
        if not user_id:
            return  # Skip if no user context

        log = Log(
            user_id=user_id,
            session_id=session_id,
            chat_message_id=message_id,
            log_type=log_type
        )
        log.mark_as_synced(hubspot_id)

        if description:
            log.sync_error = description  # Store description in sync_error field for reference

        db.session.add(log)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Failed to save success log: {e}")

    @staticmethod
    def _create_failed_log(user_id, session_id, message_id, log_type, error_message):
        """Create failed sync log"""
        if not user_id:
            return  # Skip if no user context

        log = Log(
            user_id=user_id,
            session_id=session_id,
            chat_message_id=message_id,
            log_type=log_type
        )
        log.mark_as_failed(error_message)

        db.session.add(log)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Failed to save failed log: {e}")

    # ========== UTILITY OPERATIONS ==========

    @staticmethod
    def get_contact_schemas():
        """Get contact object schemas"""
        response = HubSpotService.make_request('GET', '/crm/v3/schemas/contacts')
        return response

    @staticmethod
    def test_connection():
        """Test HubSpot API connection"""
        try:
            response = HubSpotService.get_contacts(limit=1)
            return response.status_code in [200, 201]
        except Exception:
            return False
