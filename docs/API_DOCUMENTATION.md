# API Documentation

## Base URL
`http://localhost:8000`

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer {access_token}
```

### Register User
**POST** `/auth/register`

Request:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Login
**POST** `/auth/login`

Request:
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Get Current User
**GET** `/users/me`

Headers: `Authorization: Bearer {access_token}`

Response:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "bio": "Bio text",
  "avatar_url": "https://...",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## Conversations

### Create Conversation
**POST** `/conversations/`

Request:
```json
{
  "title": "Python Help",
  "description": "Getting help with Python programming"
}
```

Response:
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Python Help",
  "description": "Getting help with Python programming",
  "is_archived": false,
  "is_pinned": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Get All Conversations
**GET** `/conversations/?skip=0&limit=10`

Response: Array of conversation objects

### Get Single Conversation
**GET** `/conversations/{conversation_id}`

Response: Conversation object with messages

### Update Conversation
**PUT** `/conversations/{conversation_id}`

Request:
```json
{
  "title": "Updated Title",
  "is_archived": false,
  "is_pinned": true
}
```

### Delete Conversation
**DELETE** `/conversations/{conversation_id}`

Response: 204 No Content

### Search Conversations
**GET** `/conversations/search/{query}`

Response: Array of matching conversations

## Messages

### Get Conversation Messages
**GET** `/messages/conversation/{conversation_id}`

Response: Array of message objects

### Send Message
**POST** `/messages/conversation/{conversation_id}/send`

Request:
```json
{
  "content": "How do I learn Python?"
}
```

Response:
```json
{
  "id": 1,
  "conversation_id": 1,
  "role": "user",
  "content": "How do I learn Python?",
  "is_edited": false,
  "tokens_used": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Stream Message
**POST** `/messages/conversation/{conversation_id}/stream`

Request:
```json
{
  "content": "How do I learn Python?"
}
```

Response: Server-sent events stream

### Delete Message
**DELETE** `/messages/message/{message_id}`

Response: 204 No Content

## File Upload

### Upload File
**POST** `/files/upload`

Request: FormData with file
```
file: <binary data>
```

Response:
```json
{
  "id": 1,
  "user_id": 1,
  "original_filename": "document.pdf",
  "stored_filename": "uuid-here.pdf",
  "file_type": "pdf",
  "file_size": 102400,
  "extracted_text": "Text extracted from PDF...",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Get User Files
**GET** `/files/?skip=0&limit=10`

Response: Array of file objects

### Get File
**GET** `/files/{file_id}`

Response: File object

### Delete File
**DELETE** `/files/{file_id}`

Response: 204 No Content

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message here"
}
```

Common HTTP Status Codes:
- `200` OK
- `201` Created
- `204` No Content
- `400` Bad Request
- `401` Unauthorized
- `404` Not Found
- `422` Validation Error
- `500` Internal Server Error
