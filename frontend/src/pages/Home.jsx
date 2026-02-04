import { Link } from 'react-router-dom';
import { Shield, ShieldCheck, Lock, BarChart3, ArrowRight } from 'lucide-react';
import PasswordChecker from '../components/PasswordChecker';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-500/20 rounded-2xl mb-6">
            <Shield className="w-10 h-10 text-primary-500" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            SecurePass
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Analyze your password strength and check if they've been exposed in data breaches.
            Protect your online accounts.
          </p>
        </div>

        {/* Password Checker */}
        <div className="max-w-xl mx-auto mb-16">
          <PasswordChecker />
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <FeatureCard
            icon={<ShieldCheck className="w-8 h-8" />}
            title="Breach Detection"
            description="We check your password against billions of leaked records using the Have I Been Pwned API."
          />
          <FeatureCard
            icon={<Lock className="w-8 h-8" />}
            title="Strength Analysis"
            description="Detailed assessment with criteria for length, complexity, and common patterns."
          />
          <FeatureCard
            icon={<BarChart3 className="w-8 h-8" />}
            title="Complete Dashboard"
            description="Create an account to save history and view statistics of your checks."
          />
        </div>

        {/* CTA */}
        <div className="bg-gradient-to-r from-primary-600/20 to-primary-800/20 rounded-2xl p-8 text-center">
          <h2 className="text-2xl font-bold mb-4">
            Want to save your history?
          </h2>
          <p className="text-gray-400 mb-6">
            Create a free account to access the complete dashboard with statistics and history.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              to="/register"
              className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
            >
              Create Free Account
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/login"
              className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              I have an account
            </Link>
          </div>
        </div>

        {/* Privacy Note */}
        <div className="mt-12 text-center text-sm text-gray-500">
          <p>
            🔒 <strong>Your privacy matters:</strong> Passwords are never stored in plain text.
            We use k-anonymity with the HIBP API — only the first 5 characters of the hash are sent.
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-6 mt-12">
        <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
          <p>
            Developed by{' '}
            <a
              href="https://github.com/kelsonbrito50"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-500 hover:underline"
            >
              Kelson Brito
            </a>
          </p>
          <p className="mt-2">
            Portfolio demonstration project • {new Date().getFullYear()}
          </p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="bg-gray-800 rounded-xl p-6 hover:bg-gray-750 transition-colors">
      <div className="w-14 h-14 bg-primary-500/20 rounded-xl flex items-center justify-center text-primary-500 mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  );
}
