from unittest import TestCase
from zoom.www.entities.application_state import ApplicationState


class TestApplicationState(TestCase):
    def setUp(self):
        self.state = ApplicationState(application_name="1",
                                      configuration_path="2",
                                      application_status="3",
                                      application_host=None,
                                      completion_time=1388556000,
                                      trigger_time="6",
                                      error_state="7",
                                      delete="8",
                                      local_mode="9",
                                      login_user="10",
                                      last_command="12",
                                      pd_disabled=False,
                                      grayed=True,
                                      read_only=True,
                                      platform=0)

    def test_to_dictionary(self):
        self.assertEquals(
            {
                'application_name': "1",
                'configuration_path': "2",
                'application_status': "unknown",
                'application_host': "",
                'completion_time': '2014-01-01 00:00:00',
                'trigger_time': "6",
                'error_state': "7",
                'delete': "8",
                'local_mode': "9",
                'login_user': "10",
                'last_command': "12",
                'pd_disabled': False,
                'grayed': True,
                'read_only': True,
                'platform': 0
            },
            self.state.to_dictionary()
        )
