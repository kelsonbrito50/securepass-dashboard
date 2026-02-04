import { useState, useEffect } from 'react';
import { Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
} from 'chart.js';
import { Shield, ShieldAlert, ShieldCheck, Activity, TrendingUp, History } from 'lucide-react';
import api from '../api/axios';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/stats/');
      setStats(response.data);
    } catch (err) {
      setError('Erro ao carregar estatísticas');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 text-red-400">
        {error}
      </div>
    );
  }

  if (!stats || stats.total_checks === 0) {
    return (
      <div className="bg-gray-800 rounded-xl p-8 text-center">
        <Shield className="w-16 h-16 mx-auto text-gray-600 mb-4" />
        <h3 className="text-xl font-bold mb-2">Nenhuma verificação ainda</h3>
        <p className="text-gray-400">
          Verifique suas senhas para ver estatísticas aqui!
        </p>
      </div>
    );
  }

  const doughnutData = {
    labels: ['Fraca', 'Razoável', 'Boa', 'Forte', 'Muito Forte'],
    datasets: [
      {
        data: [
          stats.strength_distribution.weak,
          stats.strength_distribution.fair,
          stats.strength_distribution.good,
          stats.strength_distribution.strong,
          stats.strength_distribution.very_strong,
        ],
        backgroundColor: [
          '#ef4444',
          '#f97316',
          '#eab308',
          '#22c55e',
          '#10b981',
        ],
        borderWidth: 0,
      },
    ],
  };

  const barData = {
    labels: stats.recent_checks.map(c => c.label || 'Sem rótulo').slice(0, 5),
    datasets: [
      {
        label: 'Força',
        data: stats.recent_checks.map(c => c.strength_score).slice(0, 5),
        backgroundColor: stats.recent_checks.map(c => 
          c.strength_score >= 70 ? '#22c55e' :
          c.strength_score >= 50 ? '#eab308' : '#ef4444'
        ).slice(0, 5),
        borderRadius: 4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#9ca3af',
        },
      },
    },
  };

  const barOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: { color: '#9ca3af' },
        grid: { color: '#374151' },
      },
      x: {
        ticks: { color: '#9ca3af' },
        grid: { display: false },
      },
    },
    plugins: {
      legend: { display: false },
    },
  };

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon={<Activity className="w-6 h-6" />}
          label="Total Verificadas"
          value={stats.total_checks}
          color="primary"
        />
        <StatCard
          icon={<ShieldAlert className="w-6 h-6" />}
          label="Vazadas"
          value={stats.breached_count}
          color="danger"
        />
        <StatCard
          icon={<TrendingUp className="w-6 h-6" />}
          label="Força Média"
          value={`${stats.avg_strength}%`}
          color="success"
        />
        <StatCard
          icon={<ShieldCheck className="w-6 h-6" />}
          label="Score Segurança"
          value={`${stats.security_score}%`}
          color={stats.security_score >= 70 ? 'success' : stats.security_score >= 50 ? 'warning' : 'danger'}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Strength Distribution */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-primary-500" />
            Distribuição de Força
          </h3>
          <div className="h-64">
            <Doughnut data={doughnutData} options={chartOptions} />
          </div>
        </div>

        {/* Recent Checks */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <History className="w-5 h-5 text-primary-500" />
            Verificações Recentes
          </h3>
          <div className="h-64">
            <Bar data={barData} options={barOptions} />
          </div>
        </div>
      </div>

      {/* Recent Checks List */}
      <div className="bg-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">Histórico de Verificações</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left text-gray-400 border-b border-gray-700">
                <th className="pb-3">Rótulo</th>
                <th className="pb-3">Força</th>
                <th className="pb-3">Status</th>
                <th className="pb-3">Data</th>
              </tr>
            </thead>
            <tbody>
              {stats.recent_checks.map((check, index) => (
                <tr key={index} className="border-b border-gray-700/50">
                  <td className="py-3">{check.label || 'Sem rótulo'}</td>
                  <td className="py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${
                            check.strength_score >= 70 ? 'bg-green-500' :
                            check.strength_score >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${check.strength_score}%` }}
                        />
                      </div>
                      <span className="text-sm">{check.strength_score}%</span>
                    </div>
                  </td>
                  <td className="py-3">
                    {check.is_breached ? (
                      <span className="text-red-400 flex items-center gap-1">
                        <ShieldAlert className="w-4 h-4" />
                        Vazada
                      </span>
                    ) : (
                      <span className="text-green-400 flex items-center gap-1">
                        <ShieldCheck className="w-4 h-4" />
                        Segura
                      </span>
                    )}
                  </td>
                  <td className="py-3 text-gray-400 text-sm">
                    {new Date(check.checked_at).toLocaleDateString('pt-BR')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color }) {
  const colors = {
    primary: 'bg-primary-500/20 text-primary-500',
    danger: 'bg-red-500/20 text-red-500',
    success: 'bg-green-500/20 text-green-500',
    warning: 'bg-yellow-500/20 text-yellow-500',
  };

  return (
    <div className="bg-gray-800 rounded-xl p-4">
      <div className={`w-12 h-12 rounded-lg ${colors[color]} flex items-center justify-center mb-3`}>
        {icon}
      </div>
      <p className="text-gray-400 text-sm">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}
