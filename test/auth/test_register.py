'''
Test Register Route
'''
from datetime import datetime
from app.models import User

def test_register_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid.
    """
    response = test_client.get('/auth/register')
    
    assert response.status_code == 200
    
    response_data = response.data.decode()
    print(response_data)
    assert 'Notes' in response_data
    assert 'Register Account' in response_data
    assert 'Name' in response_data
    assert 'Username' in response_data
    assert 'Email' in response_data
    assert 'Password' in response_data
    assert 'Re-enter password' in response_data
    assert 'value="Register"' in response_data
    
    
def test_register_new_user(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted with valid values (POST)
    THEN check that the response is valid and if the data was saved correctly
         on the database. 
    """
    username = 'testTuser03'
    name = 'Third Test User'
    email = 'tird_user@test.com'
    password = 'badTestPassword'
    
    response = test_client.post('/auth/register',
                                data=dict(username=username,
                                          name=name,
                                          email=email,
                                          password=password,
                                          confirm=password),
                                follow_redirects=True)
    
    assert response.status_code == 200

    response_data = response.data.decode()
    print(response_data)
    assert 'Flask Notes' in response_data
    assert 'Register' in response_data
    assert 'Username' in response_data
    assert 'Password' in response_data
    assert 'Remember me' in response_data
    assert '<a href="/auth/login">Login</a>' not in response_data
     
    
def test_register_new_user_repeated_username(test_client, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted with a repeated username 
    THEN check that the response is valid and
    """
    username = test_user.username
    name = 'New Test User'
    email = 'newUser@test.com'
    password='newBadPassword'
    response = test_client.post('/auth/register',
                                data=dict(username=username,
                                          name=name,
                                          email=email,
                                          password=password,
                                          confirm=password),
                                follow_redirects=True)
    assert response.status_code == 200
    
    response_data = response.data.decode()
    assert 'Username already taken.' in response_data
    
    

def test_register_new_user_repeated_email(test_client, test_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted with a repeated email 
    THEN check that the response is valid and
    """
    username = 'New Test User'
    name = 'New Test User'
    email = test_user.email
    password='newBadPassword'
    response = test_client.post('/auth/register',
                                data=dict(username=username,
                                          name=name,
                                          email=email,
                                          password=password,
                                          confirm=password),
                                follow_redirects=True)
    assert response.status_code == 200
    
    response_data = response.data.decode()
    assert 'Email already in use.' in response_data
    