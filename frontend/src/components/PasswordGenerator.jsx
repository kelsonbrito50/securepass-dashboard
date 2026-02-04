import { useState } from 'react';
import { Shuffle, Copy, Check } from 'lucide-react';

export default function PasswordGenerator() {
  const [password, setPassword] = useState('');
  const [length, setLength] = useState(16);
  const [options, setOptions] = useState({
    uppercase: true,
    lowercase: true,
    numbers: true,
    symbols: true,
  });
  const [copied, setCopied] = useState(false);

  const generatePassword = () => {
    let charset = '';
    if (options.uppercase) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if (options.lowercase) charset += 'abcdefghijklmnopqrstuvwxyz';
    if (options.numbers) charset += '0123456789';
    if (options.symbols) charset += '!@#$%^&*()_+-=[]{}|;:,.<>?';

    if (charset === '') {
      setPassword('');
      return;
    }

    let newPassword = '';
    for (let i = 0; i < length; i++) {
      newPassword += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    setPassword(newPassword);
    setCopied(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(password);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Shuffle className="w-6 h-6 text-primary-500" />
        Password Generator
      </h2>

      {/* Generated Password Display */}
      {password && (
        <div className="mb-4 relative">
          <input
            type="text"
            value={password}
            readOnly
            className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 pr-12 font-mono text-lg"
          />
          <button
            onClick={copyToClipboard}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
            title="Copy to clipboard"
          >
            {copied ? (
              <Check className="w-5 h-5 text-green-500" />
            ) : (
              <Copy className="w-5 h-5" />
            )}
          </button>
        </div>
      )}

      {/* Length Slider */}
      <div className="mb-4">
        <label className="block text-sm text-gray-400 mb-2">
          Length: <span className="text-white font-medium">{length}</span>
        </label>
        <input
          type="range"
          min="8"
          max="64"
          value={length}
          onChange={(e) => setLength(Number(e.target.value))}
          className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>8</span>
          <span>64</span>
        </div>
      </div>

      {/* Options */}
      <div className="space-y-2 mb-4">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={options.uppercase}
            onChange={(e) => setOptions({ ...options, uppercase: e.target.checked })}
            className="w-4 h-4 rounded accent-primary-500"
          />
          <span className="text-gray-300">Uppercase (A-Z)</span>
        </label>

        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={options.lowercase}
            onChange={(e) => setOptions({ ...options, lowercase: e.target.checked })}
            className="w-4 h-4 rounded accent-primary-500"
          />
          <span className="text-gray-300">Lowercase (a-z)</span>
        </label>

        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={options.numbers}
            onChange={(e) => setOptions({ ...options, numbers: e.target.checked })}
            className="w-4 h-4 rounded accent-primary-500"
          />
          <span className="text-gray-300">Numbers (0-9)</span>
        </label>

        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={options.symbols}
            onChange={(e) => setOptions({ ...options, symbols: e.target.checked })}
            className="w-4 h-4 rounded accent-primary-500"
          />
          <span className="text-gray-300">Symbols (!@#$%...)</span>
        </label>
      </div>

      {/* Generate Button */}
      <button
        onClick={generatePassword}
        disabled={!options.uppercase && !options.lowercase && !options.numbers && !options.symbols}
        className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
      >
        <Shuffle className="w-5 h-5" />
        Generate Password
      </button>

      {!options.uppercase && !options.lowercase && !options.numbers && !options.symbols && (
        <p className="text-red-400 text-sm mt-2 text-center">
          Please select at least one character type
        </p>
      )}
    </div>
  );
}
