# 🛠️ Technology Stack Deep Dive

This document explains the technologies used in SecurePass Dashboard and why each was chosen.

---

## Backend Technologies

### Django (Python Web Framework)
**Version:** 4.2+  
**Official Docs:** https://docs.djangoproject.com/

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

**Why Django for this project:**
- Built-in admin interface for data management
- ORM (Object-Relational Mapping) for database operations
- Excellent security features out of the box
- Large ecosystem and community support
- Perfect for REST API development with DRF

**Key concepts used:**
- Models (database schema definition)
- Migrations (database version control)
- Views (request handling)
- URL routing

---

### Django REST Framework (DRF)
**Official Docs:** https://www.django-rest-framework.org/

DRF is a powerful toolkit for building Web APIs in Django.

**Why DRF:**
- Serialization (converting complex data to JSON)
- Authentication & permissions
- Browsable API for development
- Pagination, filtering, throttling

**Key components used:**
```python
# Serializers - Convert models to JSON
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Views - Handle HTTP requests
class PasswordCheckView(APIView):
    def post(self, request):
        # Process password check
        return Response(data)
```

---

### SimpleJWT (JSON Web Tokens)
**Official Docs:** https://django-rest-framework-simplejwt.readthedocs.io/

JWT is a standard for secure token-based authentication.

**How it works:**
1. User logs in with credentials
2. Server returns access + refresh tokens
3. Client includes token in Authorization header
4. Server validates token on each request

**Token structure:**
```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VyX2lkIjoxLCJleHAiOjE2MTIzNDU2Nzh9.
abc123signature
```

**Security benefits:**
- Stateless (no server-side session storage)
- Expiration built-in
- Can be verified without database lookup

---

### Have I Been Pwned API
**Official Docs:** https://haveibeenpwned.com/API/v3

HIBP is a service that aggregates data breaches and allows checking if passwords have been exposed.

**K-Anonymity Model:**
We never send the full password or hash to HIBP. Instead:

1. Hash password with SHA-1
2. Send only first 5 characters of hash
3. HIBP returns all hashes starting with those 5 chars
4. We check locally if our full hash is in the list

```python
# Example
password = "test123"
sha1_hash = "7288EDD0FC3FFCBE93A0CF06E3568E28521687BC"
prefix = "7288E"  # Only this is sent to HIBP
suffix = "DD0FC3FFCBE93A0CF06E3568E28521687BC"  # Checked locally
```

**Privacy:** The API never sees the actual password or full hash.

---

## Frontend Technologies

### React 18
**Official Docs:** https://react.dev/

React is a JavaScript library for building user interfaces with a component-based architecture.

**Key concepts used:**
- **Components:** Reusable UI pieces
- **Hooks:** useState, useEffect, useContext
- **Context API:** Global state management (AuthContext)
- **React Router:** Client-side navigation

**Example component:**
```jsx
function PasswordChecker() {
  const [password, setPassword] = useState('');
  const [result, setResult] = useState(null);
  
  const handleCheck = async () => {
    const response = await api.post('/passwords/check/', { password });
    setResult(response.data);
  };
  
  return (
    <div>
      <input value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleCheck}>Check</button>
      {result && <StrengthMeter score={result.score} />}
    </div>
  );
}
```

---

### Vite
**Official Docs:** https://vitejs.dev/

Vite is a modern build tool that provides extremely fast development experience.

**Why Vite over Create React App:**
- ⚡ Instant server start (no bundling in dev)
- 🔥 Hot Module Replacement (HMR)
- 📦 Optimized production builds
- 🛠️ Native ES modules support

**Commands:**
```bash
npm run dev    # Start dev server
npm run build  # Production build
npm run preview # Preview production build
```

---

### TailwindCSS
**Official Docs:** https://tailwindcss.com/

Tailwind is a utility-first CSS framework for rapid UI development.

**Why Tailwind:**
- No custom CSS files needed
- Consistent design system
- Responsive design built-in
- Dark mode support
- Small production bundle (purges unused styles)

**Example usage:**
```jsx
// Traditional CSS
<div className="card">
  <h1 className="card-title">Hello</h1>
</div>

// TailwindCSS
<div className="bg-gray-800 rounded-xl p-6 shadow-lg">
  <h1 className="text-xl font-bold text-white">Hello</h1>
</div>
```

**Responsive design:**
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* 1 col on mobile, 2 on tablet, 4 on desktop */}
</div>
```

---

### Chart.js + react-chartjs-2
**Official Docs:** https://www.chartjs.org/

Chart.js is a flexible JavaScript charting library.

**Charts used in this project:**
- **Doughnut:** Password strength distribution
- **Bar:** Recent checks comparison

**Example:**
```jsx
import { Doughnut } from 'react-chartjs-2';

const data = {
  labels: ['Weak', 'Fair', 'Good', 'Strong'],
  datasets: [{
    data: [10, 20, 30, 40],
    backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e'],
  }],
};

<Doughnut data={data} options={{ responsive: true }} />
```

---

### Axios
**Official Docs:** https://axios-http.com/

Axios is a promise-based HTTP client for making API requests.

**Why Axios over fetch:**
- Automatic JSON transformation
- Request/response interceptors
- Better error handling
- Request cancellation

**Interceptors used:**
```javascript
// Add auth token to all requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-refresh token on 401
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Refresh token logic
    }
    return Promise.reject(error);
  }
);
```

---

### Lucide React (Icons)
**Official Docs:** https://lucide.dev/

Lucide provides beautiful, consistent icons as React components.

```jsx
import { Shield, Lock, Eye } from 'lucide-react';

<Shield className="w-6 h-6 text-blue-500" />
```

---

## Security Concepts

### Password Hashing (SHA-1)
SHA-1 produces a 160-bit (40 character hex) hash. While not recommended for new security applications, it's used by HIBP for compatibility.

```python
import hashlib
hash = hashlib.sha1("password".encode()).hexdigest()
# "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"
```

### K-Anonymity
A privacy model where individual records cannot be distinguished from at least k-1 other records. In HIBP:
- We send 5 hex chars = 16^5 = 1,048,576 possible prefixes
- Each prefix returns ~500 hashes on average
- Our specific hash is hidden among hundreds of others

### JWT Security Best Practices
1. **Short access token lifetime** (60 minutes)
2. **Longer refresh token lifetime** (7 days)
3. **Rotate refresh tokens** on use
4. **Store tokens securely** (httpOnly cookies in production)
5. **Validate on every request**

---

## Database Schema

```
User (Django built-in)
├── id
├── username
├── email
└── password (hashed)

PasswordCheck
├── id
├── user_id (FK → User)
├── hash_prefix (5 chars, k-anonymity)
├── label (optional, e.g., "Gmail")
├── strength_score (0-100)
├── is_breached (boolean)
├── breach_count (integer)
└── checked_at (datetime)

UserStats
├── id
├── user_id (FK → User, OneToOne)
├── total_checks
├── breached_count
├── avg_strength
└── last_check
```

---

## Learning Resources

### Django & DRF
- [Django for Beginners](https://djangoforbeginners.com/)
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)

### React
- [React Official Tutorial](https://react.dev/learn)
- [React Hooks](https://react.dev/reference/react)

### Security
- [OWASP Password Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [JWT Introduction](https://jwt.io/introduction)

### TailwindCSS
- [Tailwind Docs](https://tailwindcss.com/docs)
- [Tailwind UI Examples](https://tailwindui.com/)

---

*This documentation is part of the SecurePass Dashboard project.*
