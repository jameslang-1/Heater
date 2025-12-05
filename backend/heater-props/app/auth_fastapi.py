# app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os

# Initialize Firebase Admin SDK
# You'll need to download your service account key from Firebase Console
# and save it as 'firebase-adminsdk.json' in your backend folder
try:
    # Check if already initialized
    firebase_admin.get_app()
except ValueError:
    # Initialize if not already done
    cred = credentials.Certificate('firebase-adminsdk.json')
    firebase_admin.initialize_app(cred)

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """
    Verify Firebase ID token and return user info
    """
    token = credentials.credentials
    
    try:
        # Verify the ID token
        decoded_token = firebase_auth.verify_id_token(token)
        
        # Extract user info
        user_id = decoded_token['uid']
        email = decoded_token.get('email')
        
        # Return user dict that matches our database structure
        # You might need to create/lookup user in your database here
        return {
            'id': user_id,
            'email': email,
            'firebase_uid': user_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_optional(credentials: HTTPAuthCredentials = Depends(security)):
    """
    Optional authentication - returns None if no token provided
    """
    if not credentials:
        return None
    
    return get_current_user(credentials)
