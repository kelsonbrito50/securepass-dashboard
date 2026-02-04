import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Shield, Loader2, Mail, Lock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Credenciais inválidas');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-500/20 rounded-xl mb-4">
            <Shield className="w-8 h-8 text-primary-500" />
          </div>
          <h1 className="text-3xl font-bold">SecurePass</h1>
          <p className="text-gray-400 mt-2">Entre na sua conta</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-gray-800 rounded-xl p-6 space-y-4">
          {error && (
            <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400 text-sm">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm text-gray-400 mb-1">Usuário</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="seu.usuario"
                className="w-full bg-gray-700 border border-gray-600 rounded-lg pl-10 pr-4 py-3 focus:outline-none focus:border-primary-500 transition-colors"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Senha</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-gray-700 border border-gray-600 rounded-lg pl-10 pr-4 py-3 focus:outline-none focus:border-primary-500 transition-colors"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-600 text-white font-medium py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Entrando...
              </>
            ) : (
              'Entrar'
            )}
          </button>

          <p className="text-center text-gray-400 text-sm">
            Não tem conta?{' '}
            <Link to="/register" className="text-primary-500 hover:underline">
              Criar conta
            </Link>
          </p>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-700" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-gray-800 text-gray-500">ou</span>
            </div>
          </div>

          <Link
            to="/"
            className="block text-center text-gray-400 hover:text-white transition-colors"
          >
            Usar sem conta (verificação rápida)
          </Link>
        </form>
      </div>
    </div>
  );
}
