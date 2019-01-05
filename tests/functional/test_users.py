def test_updates(test_client):
    '''
    GIVEN an instance of LibrePatron
    WHEN the updates page is requested
    THEN check to make sure updates page is protected
    '''
    response = test_client.get('/updates')
    assert response.status_code != 200
