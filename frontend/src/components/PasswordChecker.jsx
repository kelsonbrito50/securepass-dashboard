import { useState } from 'react';
import { Eye, EyeOff, Shield, ShieldAlert, ShieldCheck, Loader2 } from 'lucide-react';
import api from '../api/axios';

const strengthColors = {
  weak: 'bg-red-500',
  fair: 'bg-orange-500',
  good: 'bg-yellow-500',
  strong: 'bg-green-500',
  very_strong: 'bg-emerald-500',
};

const strengthLabels = {
  weak: 'Weak',
  fair: 'Fair',
  good: 'Good',
  strong: 'Strong',
  very_strong: 'Very Strong',
};

export default function PasswordChecker({ onCheck }) {
  const [password, setPassword] = useState('');
  const [label, setLabel] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleCheck = async (e) => {
    e.preventDefault();
    if (!password) return;

    setLoading(true);
    setError('');

    try {
      const endpoint = localStorage.getItem('access_token') 
        ? '/passwords/check/' 
        : '/passwords/quick-check/';
      
      const response = await api.post(endpoint, { password, label });
      setResult(response.data);
      if (onCheck) onCheck(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error checking password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Shield className="w-6 h-6 text-primary-500" />
        Check Password
      </h2>

      <form onSubmit={handleCheck} className="space-y-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Password</label>
          <div className="relative">
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password to check"
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 pr-12 focus:outline-none focus:border-primary-500 transition-colors"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Label (optional)
          </label>
          <input
            type="text"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            placeholder="E.g., Gmail, Facebook, Bank..."
            className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:border-primary-500 transition-colors"
          />
        </div>

        <button
          type="submit"
          disabled={loading || !password}
          className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Checking...
            </>
          ) : (
            <>
              <Shield className="w-5 h-5" />
              Check Security
            </>
          )}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 space-y-4">
          {/* Strength Score */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Password Strength</span>
              <span className={`font-bold ${
                result.score >= 70 ? 'text-green-500' : 
                result.score >= 50 ? 'text-yellow-500' : 'text-red-500'
              }`}>
                {result.score}/100
              </span>
            </div>
            <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${strengthColors[result.strength]}`}
                style={{ width: `${result.score}%` }}
              />
            </div>
            <div className="text-center">
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${strengthColors[result.strength]} bg-opacity-20`}>
                {strengthLabels[result.strength]}
              </span>
            </div>
          </div>

          {/* Breach Status */}
          <div className={`p-4 rounded-lg ${result.is_breached ? 'bg-red-500/20 border border-red-500/50' : 'bg-green-500/20 border border-green-500/50'}`}>
            <div className="flex items-center gap-3">
              {result.is_breached ? (
                <>
                  <ShieldAlert className="w-8 h-8 text-red-500" />
                  <div>
                    <p className="font-bold text-red-400">⚠️ Password Breached!</p>
                    <p className="text-sm text-red-300">
                      Found {result.breach_count.toLocaleString()}x in data breaches
                    </p>
                  </div>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-8 h-8 text-green-500" />
                  <div>
                    <p className="font-bold text-green-400">✓ Password Safe</p>
                    <p className="text-sm text-green-300">
                      Not found in known data breaches
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Feedback */}
          <div className="space-y-2">
            <h3 className="font-medium text-gray-300">Recommendations:</h3>
            <ul className="space-y-1">
              {result.feedback.map((item, index) => (
                <li key={index} className="text-sm text-gray-400 flex items-start gap-2">
                  <span className={item.includes('Excellent') ? 'text-green-500' : 'text-yellow-500'}>
                    {item.includes('Excellent') ? '✓' : '→'}
                  </span>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Criteria Checklist */}
          <div className="grid grid-cols-2 gap-2 text-sm">
            {Object.entries(result.criteria).map(([key, value]) => (
              <div key={key} className={`flex items-center gap-2 ${value ? 'text-green-400' : 'text-gray-500'}`}>
                <span>{value ? '✓' : '✗'}</span>
                <span>{criteriaLabels[key] || key}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const criteriaLabels = {
  length: '8+ characters',
  length_12: '12+ characters',
  length_16: '16+ characters',
  uppercase: 'Uppercase',
  lowercase: 'Lowercase',
  numbers: 'Numbers',
  special: 'Special chars',
  no_common: 'Not common',
  no_sequential: 'No sequences',
  no_repeated: 'No repetition',
};
