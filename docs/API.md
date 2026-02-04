# 📡 API Documentation

Complete REST API reference for SecurePass Dashboard.

**Base URL:** `http://localhost:8000/api`

---

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## Endpoints

### Auth Endpoints

#### Register User
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com"
}
```

**Errors:**
- `400` - Invalid data (username taken, weak password, etc.)

---

#### Login (Get Tokens)
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Token Lifetimes:**
- Access: 60 minutes
- Refresh: 7 days

**Errors:**
- `401` - Invalid credentials

---

#### Refresh Token
```http
POST /api/auth/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Password Endpoints

#### Check Password (Authenticated)
```http
POST /api/passwords/check/
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "password": "MyPassword123!",
  "label": "Gmail"
}
```

**Response (200 OK):**
```json
{
  "id": 42,
  "score": 80,
  "strength": "strong",
  "feedback": [
    "Consider using 12+ characters for better security"
  ],
  "criteria": {
    "length": true,
    "length_12": false,
    "length_16": false,
    "uppercase": true,
    "lowercase": true,
    "numbers": true,
    "special": true,
    "no_common": true,
    "no_sequential": true,
    "no_repeated": true
  },
  "is_breached": false,
  "breach_count": 0,
  "label": "Gmail"
}
```

**Notes:**
- Saves to user's history
- Updates user statistics
- Label is optional

---

#### Quick Check (No Auth Required)
```http
POST /api/passwords/quick-check/
```

**Request Body:**
```json
{
  "password": "test123"
}
```

**Response (200 OK):**
```json
{
  "score": 30,
  "strength": "fair",
  "feedback": [
    "Use at least 8 characters",
    "Add uppercase letters",
    "Add special characters (!@#$%)"
  ],
  "criteria": {
    "length": false,
    "length_12": false,
    "length_16": false,
    "uppercase": false,
    "lowercase": true,
    "numbers": true,
    "special": false,
    "no_common": true,
    "no_sequential": false,
    "no_repeated": true
  },
  "is_breached": true,
  "breach_count": 86453
}
```

**Notes:**
- No authentication required
- Does NOT save to history
- Perfect for anonymous/demo users

---

#### Get Password History
```http
GET /api/passwords/history/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": 42,
    "label": "Gmail",
    "strength_score": 80,
    "is_breached": false,
    "breach_count": 0,
    "checked_at": "2026-02-04T12:30:00Z"
  },
  {
    "id": 41,
    "label": "Facebook",
    "strength_score": 65,
    "is_breached": true,
    "breach_count": 1234,
    "checked_at": "2026-02-04T12:15:00Z"
  }
]
```

**Notes:**
- Returns last 50 checks
- Ordered by most recent first

---

### Statistics Endpoints

#### Get User Statistics
```http
GET /api/stats/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "total_checks": 25,
  "breached_count": 3,
  "avg_strength": 72.5,
  "last_check": "2026-02-04T12:30:00Z",
  "strength_distribution": {
    "weak": 2,
    "fair": 5,
    "good": 8,
    "strong": 7,
    "very_strong": 3
  },
  "recent_checks": [
    {
      "id": 42,
      "label": "Gmail",
      "strength_score": 80,
      "is_breached": false,
      "breach_count": 0,
      "checked_at": "2026-02-04T12:30:00Z"
    }
  ],
  "security_score": 78.5
}
```

**Security Score Calculation:**
- Starts at 100
- Penalized by breached password ratio (-40 max)
- Boosted by strong/very_strong ratio (+30 max)
- Adjusted by average strength

---

## Error Responses

### 400 Bad Request
```json
{
  "password": ["This field is required."]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

Or for invalid credentials:
```json
{
  "detail": "No active account found with the given credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Password Strength Scoring

| Criteria | Points |
|----------|--------|
| 8+ characters | +10 |
| 12+ characters | +10 |
| 16+ characters | +10 |
| Has uppercase | +10 |
| Has lowercase | +10 |
| Has numbers | +10 |
| Has special chars | +10 |
| Not common password | +10 |
| No sequences (123, abc) | +10 |
| No repeated chars (aaa) | +10 |
| **Maximum** | **100** |

**Strength Labels:**
| Score | Label |
|-------|-------|
| 0-29 | weak |
| 30-49 | fair |
| 50-69 | good |
| 70-89 | strong |
| 90-100 | very_strong |

---

## Rate Limiting (Planned)

| Endpoint | Limit |
|----------|-------|
| /auth/login/ | 5/minute |
| /passwords/quick-check/ | 30/minute |
| /passwords/check/ | 60/minute |
| Others | 100/minute |

---

## Code Examples

### JavaScript (Axios)
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Login
const { data } = await api.post('/auth/login/', {
  username: 'john',
  password: 'secret123',
});
const token = data.access;

// Check password
const result = await api.post(
  '/passwords/check/',
  { password: 'MyPass123!', label: 'Gmail' },
  { headers: { Authorization: `Bearer ${token}` } }
);
console.log(result.data.score); // 80
```

### Python (Requests)
```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Login
response = requests.post(f'{BASE_URL}/auth/login/', json={
    'username': 'john',
    'password': 'secret123'
})
token = response.json()['access']

# Check password
headers = {'Authorization': f'Bearer {token}'}
result = requests.post(
    f'{BASE_URL}/passwords/check/',
    json={'password': 'MyPass123!', 'label': 'Gmail'},
    headers=headers
)
print(result.json()['score'])  # 80
```

### cURL
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}'

# Check password (with token)
curl -X POST http://localhost:8000/api/passwords/check/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbG..." \
  -d '{"password":"MyPass123!","label":"Gmail"}'
```

---

*This documentation is part of the SecurePass Dashboard project.*
