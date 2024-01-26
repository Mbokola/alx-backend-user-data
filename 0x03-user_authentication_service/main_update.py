#!/usr/bin/env python3

from app import app, AUTH

user = AUTH.register_user(
    'test@test.com',
    'test'
)

reset_token = AUTH.get_reset_password_token(
    'test@test.com'
)

with app.test_client() as c:
    payload = {
        'email': "test@test.com",
        'reset_token': "bad_reset_token",
        'new_password': 'test'
    }
    resp = c.put('/reset_password', data=payload)
    if resp.status_code != 403:
        print("Status code not 403")
        exit(0)

print("OK", end='')
