# file: test/auth/test_login.py
'''
Test Login Route
'''

def test_auth_login_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid.
    """
    response = test_client.get('/auth/login',
                               follow_redirects=True)
    
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Notes' in response_data
    assert 'Login' in response_data
    assert 'Password' in response_data
    assert '<a href="/auth/login">Login</a>' not in response_data
    assert 'value="Login"' in response_data
    
def test_auth_login_invalid_username(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted (POST) with an invalid username
    THEN check that the response is valid.
    """
    response = test_client.post('/auth/login',
                     data=dict(username='indalidUser',
                               password='badTestPassword'),
                     follow_redirects=True)
    
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Username not found.' in response_data
    
    
def test_auth_login_invalid_password(test_client, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted (POST) with an invalid password
    THEN check that the response is valid.
    """
    response = test_client.post('/auth/login',
                     data=dict(username=test_user.username,
                               password='invalidPasswors'),
                     follow_redirects=True)
    
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Password is incorrect' in response_data
    
    
def test_auth_login_with_valid_credentials(test_client, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted (POST) with a valid username and password
    THEN check that the response is valid.
    """
    response = test_client.post('/auth/login',
                     data=dict(username=test_user.username,
                               password='badTestPassword'),
                     follow_redirects=True)
    
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Flask Notes' in response_data
    assert '<title>Flask Notes | Home</title>' in response_data
    assert 'href="/profile">Profile</a>' in response_data
    assert 'href="/auth/logout">Logout</a>' in response_data 
    
    
    
def test_auth_logout_logged_in_user(test_client, test_logged_user, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET) with a valid user logged in
    THEN check that the response is valid.
    """
    response = test_client.get('/home',
                               follow_redirects=True)
    
    assert response.status_code == 200
    response_data = response.data.decode()
    
    # Verify if user is logged in
    assert 'Flask Notes' in response_data
    assert '<title>Flask Notes | Home</title>' in response_data
    assert 'href="/profile">Profile</a>' in response_data
    assert 'href="/auth/logout">Logout</a>' in response_data 
    
    # Verify Logout Response
    response = test_client.get('/auth/logout',
                               follow_redirects=True)
    
    assert response.status_code == 200
    response_data = response.data.decode()
    u_name = test_user.username
    assert f'{u_name} Logged off.' in response_data
    assert 'Flask Notes' in response_data
    assert '<title>Flask Notes | Login</title>' in response_data
    assert 'href="/auth/register">Register</a>' in response_data 
    