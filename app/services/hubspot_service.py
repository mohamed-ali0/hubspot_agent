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
    def get_hubspot_token(user_id=None):
        """Get HubSpot PAT from user or environment"""
        if user_id:
            # Get token from user's database record
            user = User.query.get(user_id)
            if user and user.hubspot_pat_token:
                return user.hubspot_pat_token
            else:
                raise ValueError(f'User {user_id} does not have a HubSpot token configured')
        else:
            # Fallback to environment variable for backward compatibility
            token = current_app.config.get('HUBSPOT_ACCESS_TOKEN')
            if not token:
                raise ValueError('HUBSPOT_ACCESS_TOKEN not configured in environment')
            return token

    @staticmethod
    def get_base_url():
        """Get HubSpot base URL"""
        return current_app.config.get('HUBSPOT_API_URL', 'https://api.hubapi.com')

    @staticmethod
    def get_headers(user_id=None):
        """Get standard HubSpot API headers"""
        token = HubSpotService.get_hubspot_token(user_id)
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def make_request(method, endpoint, data=None, params=None, user_id=None):
        """Make authenticated request to HubSpot API"""
        url = f"{HubSpotService.get_base_url()}{endpoint}"
        headers = HubSpotService.get_headers(user_id)

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
    def get_contacts(limit=10, user_id=None, **filters):
        """Get HubSpot contacts"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/contacts', params=params, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def create_contact(contact_data, session_id=None, message_id=None, user_id=None):
        """Create contact in HubSpot"""
        response = HubSpotService.make_request('POST', '/crm/v3/objects/contacts', {'properties': contact_data}, user_id=user_id)

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
    def update_contact(contact_id, contact_data, session_id=None, message_id=None, user_id=None):
        """Update contact in HubSpot"""
        response = HubSpotService.make_request('PATCH', f'/crm/v3/objects/contacts/{contact_id}', {'properties': contact_data}, user_id=user_id)

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'contact_action', hubspot_id,
                f"Contact updated: {contact_data.get('email', 'N/A')}"
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
    def get_deals(limit=10, user_id=None, **filters):
        """Get HubSpot deals"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/deals', params=params, user_id=user_id)
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

        response = HubSpotService.make_request('POST', '/crm/v3/objects/deals', payload, user_id=user_id)

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
    def get_notes(limit=10, user_id=None, **filters):
        """Get HubSpot notes"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/notes', params=params, user_id=user_id)
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

        response = HubSpotService.make_request('POST', '/crm/v3/objects/notes', payload, user_id=user_id)

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
    def get_tasks(limit=10, user_id=None, **filters):
        """Get HubSpot tasks"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/tasks', params=params, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    # ========== ADDITIONAL METHODS FOR NEW API STRUCTURE ==========
    
    @staticmethod
    def get_companies(limit=10, user_id=None, **filters):
        """Get HubSpot companies"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/companies', params=params, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_company_by_id(company_id, user_id=None):
        """Get specific company by ID"""
        response = HubSpotService.make_request('GET', f'/crm/v3/objects/companies/{company_id}', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_contact_by_id(contact_id, user_id=None):
        """Get specific contact by ID"""
        response = HubSpotService.make_request('GET', f'/crm/v3/objects/contacts/{contact_id}', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_deal_by_id(deal_id, user_id=None):
        """Get specific deal by ID"""
        response = HubSpotService.make_request('GET', f'/crm/v3/objects/deals/{deal_id}', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_note_by_id(note_id, user_id=None):
        """Get specific note by ID"""
        response = HubSpotService.make_request('GET', f'/crm/v3/objects/notes/{note_id}', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_task_by_id(task_id, user_id=None):
        """Get specific task by ID"""
        response = HubSpotService.make_request('GET', f'/crm/v3/objects/tasks/{task_id}', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_contact_properties(user_id=None):
        """Get contact properties"""
        response = HubSpotService.make_request('GET', '/crm/v3/properties/contacts', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_company_properties(user_id=None):
        """Get company properties"""
        response = HubSpotService.make_request('GET', '/crm/v3/properties/companies', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_deal_pipelines(user_id=None):
        """Get deal pipelines"""
        response = HubSpotService.make_request('GET', '/crm/v3/pipelines/deals', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_deal_stages(pipeline_id, user_id=None):
        """Get deal stages for a specific pipeline"""
        response = HubSpotService.make_request('GET', f'/crm/v3/pipelines/deals/{pipeline_id}', user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def update_deal_stage(deal_id, new_stage, user_id=None):
        """Update deal stage"""
        payload = {'properties': {'dealstage': new_stage}}
        response = HubSpotService.make_request('PATCH', f'/crm/v3/objects/deals/{deal_id}', payload, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    # ========== LEAD OPERATIONS ==========

    @staticmethod
    def create_lead(lead_data, session_id=None, message_id=None, user_id=None):
        """Create a lead (contact with lead properties)"""
        # In HubSpot, leads are typically contacts with specific properties
        lead_properties = {
            'firstname': lead_data.get('firstname', ''),
            'lastname': lead_data.get('lastname', ''),
            'email': lead_data.get('email', ''),
            'phone': lead_data.get('phone', ''),
            'company': lead_data.get('company', ''),
            'lead_status': lead_data.get('lead_status', 'NEW'),
            'lead_source': lead_data.get('lead_source', 'WhatsApp'),
            'lifecyclestage': 'lead'
        }
        
        response = HubSpotService.make_request('POST', '/crm/v3/objects/contacts', {'properties': lead_properties}, user_id=user_id)
        
        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'contact_action', hubspot_id,
                f"Lead created: {lead_data.get('email', 'N/A')}"
            )
            return {'success': True, 'hubspot_id': hubspot_id, 'data': response.json()}
        else:
            error_msg = response.text
            HubSpotService._create_failed_log(
                user_id, session_id, message_id, 'contact_action', error_msg
            )
            return {'success': False, 'error': error_msg}

    @staticmethod
    def qualify_lead(contact_id, qualification_data, user_id=None):
        """Qualify a lead and potentially create a deal"""
        # Update lead status
        update_payload = {
            'properties': {
                'lead_status': qualification_data.get('lead_status', 'QUALIFIED'),
                'lifecyclestage': 'opportunity'
            }
        }
        
        response = HubSpotService.make_request('PATCH', f'/crm/v3/objects/contacts/{contact_id}', update_payload, user_id=user_id)
        
        if response.status_code == 200:
            # If qualification includes deal creation
            if qualification_data.get('create_deal'):
                deal_data = {
                    'dealname': qualification_data.get('deal_name', f'Deal for Contact {contact_id}'),
                    'amount': qualification_data.get('deal_amount', ''),
                    'dealstage': qualification_data.get('deal_stage', 'appointmentscheduled'),
                    'closedate': qualification_data.get('close_date', '')
                }
                
                # Create deal and associate with contact
                deal_result = HubSpotService.create_deal(
                    deal_data=deal_data,
                    associations={'contacts': [contact_id]},
                    user_id=user_id
                )
                
                return {
                    'success': True,
                    'contact_updated': True,
                    'deal_created': deal_result.get('success', False),
                    'deal_id': deal_result.get('hubspot_id') if deal_result.get('success') else None
                }
            else:
                return {'success': True, 'contact_updated': True, 'deal_created': False}
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_leads(limit=10, user_id=None, **filters):
        """Get leads (contacts with lead status)"""
        params = {
            'limit': limit,
            'properties': 'firstname,lastname,email,phone,company,lead_status,lead_source,lifecyclestage',
            'filterGroups': [{
                'filters': [{
                    'propertyName': 'lifecyclestage',
                    'operator': 'EQ',
                    'value': 'lead'
                }]
            }]
        }
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/contacts', params=params, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_calls(limit=10, user_id=None, **filters):
        """Get HubSpot calls"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/calls', params=params, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_meetings(limit=10, user_id=None, **filters):
        """Get HubSpot meetings"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/meetings', params=params, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_emails(limit=10, user_id=None, **filters):
        """Get HubSpot emails"""
        params = {'limit': limit}
        if filters:
            params.update(filters)

        response = HubSpotService.make_request('GET', '/crm/v3/objects/emails', params=params, user_id=user_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HubSpot API error: {response.status_code} - {response.text}")

    @staticmethod
    def get_association_types(user_id=None):
        """Get association types"""
        # HubSpot doesn't have a direct endpoint for association types
        # Return a mock response with common association types
        return {
            "results": [
                {
                    "type": "contact_to_company",
                    "name": "Contact to Company",
                    "description": "Associate contacts with companies"
                },
                {
                    "type": "contact_to_deal",
                    "name": "Contact to Deal", 
                    "description": "Associate contacts with deals"
                },
                {
                    "type": "company_to_deal",
                    "name": "Company to Deal",
                    "description": "Associate companies with deals"
                },
                {
                    "type": "deal_to_task",
                    "name": "Deal to Task",
                    "description": "Associate deals with tasks"
                },
                {
                    "type": "contact_to_note",
                    "name": "Contact to Note",
                    "description": "Associate contacts with notes"
                }
            ]
        }

    @staticmethod
    def create_task(task_data, associations=None, session_id=None, message_id=None, user_id=None):
        """Create task in HubSpot"""
        payload = {'properties': task_data}
        if associations:
            payload['associations'] = associations

        response = HubSpotService.make_request('POST', '/crm/v3/objects/tasks', payload, user_id=user_id)

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
    def create_meeting(meeting_data, associations=None, session_id=None, message_id=None, user_id=None):
        """Create meeting in HubSpot"""
        payload = {'properties': meeting_data}
        if associations:
            payload['associations'] = associations

        response = HubSpotService.make_request('POST', '/crm/v3/objects/meetings', payload, user_id=user_id)

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

    @staticmethod
    def create_call(call_data, associations=None, session_id=None, message_id=None, user_id=None):
        """Create call in HubSpot"""
        payload = {'properties': call_data}
        if associations:
            payload['associations'] = associations

        response = HubSpotService.make_request('POST', '/crm/v3/objects/calls', payload, user_id=user_id)

        if response.status_code in [200, 201]:
            hubspot_id = response.json().get('id')
            HubSpotService._create_success_log(
                user_id, session_id, message_id, 'call_meeting', hubspot_id,
                f"Call created: {call_data.get('hs_call_title', 'N/A')}"
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
    def create_company(company_data, session_id=None, message_id=None, user_id=None):
        """Create company in HubSpot"""
        response = HubSpotService.make_request('POST', '/crm/v3/objects/companies', {'properties': company_data}, user_id=user_id)

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
