#!/usr/bin/env python3
"""
Unit tests for HubSpot Service

Tests the HubSpotService class methods in isolation
"""

import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.hubspot_service import HubSpotService

class TestHubSpotService:
    """Test class for HubSpotService"""

    def test_get_hubspot_token_from_env(self):
        """Test getting token from environment"""
        with patch.dict(os.environ, {'HUBSPOT_ACCESS_TOKEN': 'test-token'}):
            token = HubSpotService.get_hubspot_token()
            assert token == 'test-token'

    def test_get_hubspot_token_missing(self):
        """Test error when token not in environment"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match='HUBSPOT_ACCESS_TOKEN not configured'):
                HubSpotService.get_hubspot_token()

    def test_get_base_url_default(self):
        """Test default base URL"""
        url = HubSpotService.get_base_url()
        assert url == 'https://api.hubapi.com'

    def test_get_base_url_from_config(self):
        """Test base URL from config"""
        with patch('app.services.hubspot_service.current_app') as mock_app:
            mock_app.config = {'HUBSPOT_API_URL': 'https://custom.api.com'}
            url = HubSpotService.get_base_url()
            assert url == 'https://custom.api.com'

    def test_get_headers(self):
        """Test getting headers"""
        with patch.dict(os.environ, {'HUBSPOT_ACCESS_TOKEN': 'test-token'}):
            with patch('app.services.hubspot_service.current_app') as mock_app:
                mock_app.config = {}
                headers = HubSpotService.get_headers()

                assert 'Authorization' in headers
                assert 'Content-Type' in headers
                assert headers['Authorization'] == 'Bearer test-token'
                assert headers['Content-Type'] == 'application/json'

    @patch('app.services.hubspot_service.requests.request')
    def test_make_request_success(self, mock_request):
        """Test successful API request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {'HUBSPOT_ACCESS_TOKEN': 'test-token'}):
            with patch('app.services.hubspot_service.current_app') as mock_app:
                mock_app.config = {}
                response = HubSpotService.make_request('GET', '/test/endpoint')

                assert response == mock_response
                mock_request.assert_called_once()

    @patch('app.services.hubspot_service.requests.request')
    def test_make_request_with_data(self, mock_request):
        """Test API request with data"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {'HUBSPOT_ACCESS_TOKEN': 'test-token'}):
            with patch('app.services.hubspot_service.current_app') as mock_app:
                mock_app.config = {}
                test_data = {'key': 'value'}
                response = HubSpotService.make_request('POST', '/test/endpoint', data=test_data)

                assert response == mock_response
                mock_request.assert_called_once()
                call_args = mock_request.call_args
                assert call_args[1]['json'] == test_data

    @patch('app.services.hubspot_service.requests.request')
    def test_make_request_with_params(self, mock_request):
        """Test API request with query parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {'HUBSPOT_ACCESS_TOKEN': 'test-token'}):
            with patch('app.services.hubspot_service.current_app') as mock_app:
                mock_app.config = {}
                test_params = {'limit': '10', 'offset': '0'}
                response = HubSpotService.make_request('GET', '/test/endpoint', params=test_params)

                assert response == mock_response
                mock_request.assert_called_once()
                call_args = mock_request.call_args
                assert call_args[1]['params'] == test_params

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_contacts(self, mock_make_request):
        """Test getting contacts"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_contacts(limit=5)

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/objects/contacts', params={'limit': 5})

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_create_contact_success(self, mock_make_request):
        """Test successful contact creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': '12345'}
        mock_make_request.return_value = mock_response

        with patch('app.services.hubspot_service.HubSpotService._create_success_log'):
            result = HubSpotService.create_contact(
                contact_data={'email': 'test@example.com'},
                session_id=1,
                message_id=1,
                user_id=1
            )

            assert result['success'] is True
            assert result['hubspot_id'] == '12345'
            assert 'data' in result

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_create_contact_failure(self, mock_make_request):
        """Test failed contact creation"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Bad Request'
        mock_make_request.return_value = mock_response

        with patch('app.services.hubspot_service.HubSpotService._create_failed_log'):
            result = HubSpotService.create_contact(
                contact_data={'email': 'test@example.com'},
                session_id=1,
                message_id=1,
                user_id=1
            )

            assert result['success'] is False
            assert 'error' in result

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_contact_properties(self, mock_make_request):
        """Test getting contact properties"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_contact_properties()

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/properties/contacts')

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_deals(self, mock_make_request):
        """Test getting deals"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_deals(limit=10)

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/objects/deals', params={'limit': 10})

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_create_deal_success(self, mock_make_request):
        """Test successful deal creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': '67890'}
        mock_make_request.return_value = mock_response

        with patch('app.services.hubspot_service.HubSpotService._create_success_log'):
            result = HubSpotService.create_deal(
                deal_data={'dealname': 'Test Deal'},
                session_id=1,
                message_id=1,
                user_id=1
            )

            assert result['success'] is True
            assert result['hubspot_id'] == '67890'

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_notes(self, mock_make_request):
        """Test getting notes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_notes(limit=5)

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/objects/notes', params={'limit': 5})

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_create_note_success(self, mock_make_request):
        """Test successful note creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'note123'}
        mock_make_request.return_value = mock_response

        with patch('app.services.hubspot_service.HubSpotService._create_success_log'):
            result = HubSpotService.create_note(
                note_data={'hs_note_body': 'Test note'},
                session_id=1,
                message_id=1,
                user_id=1
            )

            assert result['success'] is True
            assert result['hubspot_id'] == 'note123'

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_tasks(self, mock_make_request):
        """Test getting tasks"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_tasks(limit=10)

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/objects/tasks', params={'limit': 10})

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_create_task_success(self, mock_make_request):
        """Test successful task creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'task456'}
        mock_make_request.return_value = mock_response

        with patch('app.services.hubspot_service.HubSpotService._create_success_log'):
            result = HubSpotService.create_task(
                task_data={'hs_task_subject': 'Test Task'},
                session_id=1,
                message_id=1,
                user_id=1
            )

            assert result['success'] is True
            assert result['hubspot_id'] == 'task456'

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_companies(self, mock_make_request):
        """Test getting companies"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_companies(limit=5)

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/objects/companies', params={'limit': 5})

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_owners(self, mock_make_request):
        """Test getting owners"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_owners(limit=10)

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/objects/owners', params={'limit': 10})

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_deal_pipelines(self, mock_make_request):
        """Test getting deal pipelines"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_deal_pipelines()

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/pipelines/deals')

    @patch('app.services.hubspot_service.HubSpotService.make_request')
    def test_get_contact_schemas(self, mock_make_request):
        """Test getting contact schemas"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        response = HubSpotService.get_contact_schemas()

        assert response == mock_response
        mock_make_request.assert_called_once_with('GET', '/crm/v3/schemas/contacts')

    @patch('app.services.hubspot_service.HubSpotService.get_contacts')
    def test_test_connection_success(self, mock_get_contacts):
        """Test successful connection test"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get_contacts.return_value = mock_response

        connected = HubSpotService.test_connection()

        assert connected is True

    @patch('app.services.hubspot_service.HubSpotService.get_contacts')
    def test_test_connection_failure(self, mock_get_contacts):
        """Test failed connection test"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get_contacts.return_value = mock_response

        connected = HubSpotService.test_connection()

        assert connected is False

    @patch('app.services.hubspot_service.HubSpotService.get_contacts')
    def test_test_connection_exception(self, mock_get_contacts):
        """Test connection test with exception"""
        mock_get_contacts.side_effect = Exception("Connection error")

        connected = HubSpotService.test_connection()

        assert connected is False

if __name__ == "__main__":
    pytest.main([__file__])
