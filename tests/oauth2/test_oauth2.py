from tests.fixtures.main_fixture import test_client


class TestGoogleAuth:

    def test_init(self):
        pass

    # def test_get_google_oauth_args(self, test_client):
    #     rv = test_client.get("/api/v1/google_login?google_oauth=true")
    #
    def test_oauth_login(self, test_client):
        data = {
            "code": "<CODE>",
            "scope": "SCOPE",
            "email": "<EMAIL>",
        }
        rv = test_client.get(
            "/api/v1/google_login?google_oauth=true",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        assert {} in rv.json()



    # def test_oauth_refresh(self, test_client):
    #     pass
