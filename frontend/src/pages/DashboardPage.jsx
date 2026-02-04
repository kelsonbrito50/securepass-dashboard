import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, Home, LogOut, Menu, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Dashboard from '../components/Dashboard';
import PasswordChecker from '../components/PasswordChecker';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2">
              <Shield className="w-8 h-8 text-primary-500" />
              <span className="text-xl font-bold">SecurePass</span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-4">
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  activeTab === 'dashboard'
                    ? 'bg-primary-500/20 text-primary-500'
                    : 'hover:bg-gray-700'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveTab('check')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  activeTab === 'check'
                    ? 'bg-primary-500/20 text-primary-500'
                    : 'hover:bg-gray-700'
                }`}
              >
                Check Password
              </button>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-gray-400 hover:text-white transition-colors"
              >
                <LogOut className="w-5 h-5" />
                Logout
              </button>
            </nav>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 hover:bg-gray-700 rounded-lg"
            >
              {mobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <nav className="md:hidden py-4 border-t border-gray-700">
              <button
                onClick={() => {
                  setActiveTab('dashboard');
                  setMobileMenuOpen(false);
                }}
                className="w-full text-left px-4 py-3 hover:bg-gray-700 rounded-lg"
              >
                Dashboard
              </button>
              <button
                onClick={() => {
                  setActiveTab('check');
                  setMobileMenuOpen(false);
                }}
                className="w-full text-left px-4 py-3 hover:bg-gray-700 rounded-lg"
              >
                Check Password
              </button>
              <button
                onClick={handleLogout}
                className="w-full text-left px-4 py-3 text-red-400 hover:bg-gray-700 rounded-lg flex items-center gap-2"
              >
                <LogOut className="w-5 h-5" />
                Logout
              </button>
            </nav>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8">
        {activeTab === 'dashboard' ? (
          <Dashboard />
        ) : (
          <div className="max-w-xl mx-auto">
            <PasswordChecker />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-4">
        <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
          SecurePass Dashboard • {new Date().getFullYear()}
        </div>
      </footer>
    </div>
  );
}
