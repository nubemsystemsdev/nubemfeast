import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Download,
  Share2,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Info,
  Loader2,
  AlertCircle,
} from 'lucide-react';
import { useScan } from '../hooks/useScans';
import { useGuide, useAnalysis } from '../hooks/useGuide';
import { useBarriers } from '../hooks/useAnalysis';
import { cn } from '../utils/cn';
import {
  getAccessibilityScoreColor,
  getAccessibilityScoreLabel,
  BARRIER_TYPE_LABELS,
  SEVERITY_COLORS,
  SEVERITY_LABELS,
} from '../utils/accessibility';
import type { BarrierSeverity } from '../types';

export default function SummaryPage() {
  const { scanId } = useParams<{ scanId: string }>();
  const navigate = useNavigate();

  const { data: scan, isLoading: scanLoading } = useScan(scanId!);
  const { data: guide, isLoading: guideLoading } = useGuide(scanId!);
  const { data: barriers, isLoading: barriersLoading } = useBarriers(scanId!);

  const isLoading = scanLoading || guideLoading || barriersLoading;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
      </div>
    );
  }

  if (!scan || !guide) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
        <h2 className="text-lg font-medium text-gray-900 mb-2">
          No se encontro el resumen
        </h2>
        <button onClick={() => navigate('/')} className="btn-secondary">
          Volver al inicio
        </button>
      </div>
    );
  }

  // Group barriers by severity
  const barriersBySeverity = barriers?.reduce(
    (acc, b) => {
      acc[b.severity] = (acc[b.severity] || 0) + 1;
      return acc;
    },
    {} as Record<BarrierSeverity, number>
  ) || {};

  // Group barriers by type
  const barriersByType = barriers?.reduce(
    (acc, b) => {
      acc[b.barrier_type] = (acc[b.barrier_type] || 0) + 1;
      return acc;
    },
    {} as Record<string, number>
  ) || {};

  const score = guide.accessibility_score;

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate(-1)} className="btn-secondary p-2">
            <ArrowLeft className="h-5 w-5" />
          </button>
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              Resumen de Accesibilidad
            </h1>
            <p className="text-sm text-gray-500">{scan.name}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button className="btn-secondary">
            <Share2 className="h-4 w-4 mr-2" />
            Compartir
          </button>
          <button className="btn-primary">
            <Download className="h-4 w-4 mr-2" />
            Descargar PDF
          </button>
        </div>
      </div>

      {/* Score card */}
      <div className="card p-6">
        <div className="flex items-center gap-6">
          <div
            className={cn(
              'w-24 h-24 rounded-full flex items-center justify-center text-3xl font-bold',
              score !== null && score >= 80
                ? 'bg-green-100 text-green-600'
                : score !== null && score >= 60
                  ? 'bg-yellow-100 text-yellow-600'
                  : score !== null && score >= 40
                    ? 'bg-orange-100 text-orange-600'
                    : 'bg-red-100 text-red-600'
            )}
          >
            {score !== null ? Math.round(score) : '?'}
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900">
              {getAccessibilityScoreLabel(score)}
            </h2>
            <p className="text-gray-600 mt-1">{guide.summary}</p>
          </div>
        </div>
      </div>

      {/* Critical alerts */}
      {guide.critical_alerts.length > 0 && (
        <div className="card p-6 border-red-200 bg-red-50">
          <div className="flex items-start gap-3">
            <XCircle className="h-6 w-6 text-red-600 flex-shrink-0" />
            <div>
              <h3 className="font-medium text-red-800 mb-2">
                Alertas Criticas ({guide.critical_alerts.length})
              </h3>
              <ul className="space-y-1">
                {guide.critical_alerts.map((alert, index) => (
                  <li key={index} className="text-red-700 text-sm">
                    {alert}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Barriers summary */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* By severity */}
        <div className="card p-6">
          <h3 className="font-medium text-gray-900 mb-4">Barreras por Severidad</h3>
          <div className="space-y-3">
            {(['critical', 'high', 'medium', 'low'] as BarrierSeverity[]).map((severity) => (
              <div key={severity} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span
                    className={cn(
                      'w-3 h-3 rounded-full',
                      severity === 'critical'
                        ? 'bg-red-500'
                        : severity === 'high'
                          ? 'bg-orange-500'
                          : severity === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                    )}
                  />
                  <span className="text-sm text-gray-600">
                    {SEVERITY_LABELS[severity]}
                  </span>
                </div>
                <span className="font-medium text-gray-900">
                  {barriersBySeverity[severity] || 0}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* By type */}
        <div className="card p-6">
          <h3 className="font-medium text-gray-900 mb-4">Barreras por Tipo</h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {Object.entries(barriersByType)
              .sort(([, a], [, b]) => b - a)
              .map(([type, count]) => (
                <div key={type} className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">
                    {BARRIER_TYPE_LABELS[type as keyof typeof BARRIER_TYPE_LABELS] || type}
                  </span>
                  <span className="font-medium text-gray-900">{count}</span>
                </div>
              ))}
          </div>
        </div>
      </div>

      {/* Navigation steps summary */}
      <div className="card p-6">
        <h3 className="font-medium text-gray-900 mb-4">Resumen del Recorrido</h3>
        <div className="space-y-4">
          {guide.navigation_steps.map((step) => (
            <div
              key={step.step_number}
              className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg"
            >
              <div
                className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium',
                  step.accessibility_rating === 'accessible'
                    ? 'bg-green-100 text-green-700'
                    : step.accessibility_rating === 'caution'
                      ? 'bg-yellow-100 text-yellow-700'
                      : step.accessibility_rating === 'difficult'
                        ? 'bg-orange-100 text-orange-700'
                        : 'bg-red-100 text-red-700'
                )}
              >
                {step.step_number}
              </div>
              <div className="flex-1">
                <h4 className="font-medium text-gray-900">{step.title}</h4>
                {step.barriers.length > 0 && (
                  <p className="text-sm text-gray-500 mt-1">
                    {step.barriers.length} barrera{step.barriers.length > 1 ? 's' : ''}
                  </p>
                )}
              </div>
              {step.accessibility_rating === 'accessible' ? (
                <CheckCircle className="h-5 w-5 text-green-500" />
              ) : step.accessibility_rating === 'inaccessible' ? (
                <XCircle className="h-5 w-5 text-red-500" />
              ) : (
                <AlertTriangle className="h-5 w-5 text-yellow-500" />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex justify-center gap-4 pb-8">
        <Link to={`/scan/${scanId}/tour`} className="btn-secondary">
          Ver Recorrido Virtual
        </Link>
        <Link to="/" className="btn-primary">
          Volver al Inicio
        </Link>
      </div>
    </div>
  );
}
