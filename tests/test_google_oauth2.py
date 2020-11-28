

class TestGoogleAuth:


    def test_init(self):
        pass

    # def test_get_google_oauth_args(self, test_client):
    #     rv = test_client.get("/api/v1/google_login?google_oauth=true")
    #
    def test_oauth_login(self, test_client):
        rv = test_client.get("/api/v1/google_login?google_oauth=true")



    # def test_oauth_refresh(self, test_client):
    #     pass
