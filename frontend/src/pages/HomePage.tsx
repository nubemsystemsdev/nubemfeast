import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, MapPin, Calendar, Image as ImageIcon, Play, Trash2, Loader2 } from 'lucide-react';
import { useScans, useCreateScan, useDeleteScan } from '../hooks/useScans';
import type { ScanCreate } from '../types';
import { cn } from '../utils/cn';

export default function HomePage() {
  const navigate = useNavigate();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newScan, setNewScan] = useState<ScanCreate>({ name: '', description: '', location: '' });

  const { data: scansData, isLoading } = useScans();
  const createScan = useCreateScan();
  const deleteScan = useDeleteScan();

  const handleCreateScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newScan.name.trim()) return;

    try {
      const scan = await createScan.mutateAsync(newScan);
      setShowCreateForm(false);
      setNewScan({ name: '', description: '', location: '' });
      navigate(`/scan/${scan.id}/tour`);
    } catch (error) {
      console.error('Error creating scan:', error);
    }
  };

  const handleDeleteScan = async (scanId: string) => {
    if (!confirm('¿Estas seguro de que quieres eliminar este escaneo?')) return;
    await deleteScan.mutateAsync(scanId);
  };

  const getStatusBadge = (status: string) => {
    const badges: Record<string, { label: string; className: string }> = {
      pending: { label: 'Pendiente', className: 'bg-gray-100 text-gray-700' },
      uploading: { label: 'Subiendo', className: 'bg-blue-100 text-blue-700' },
      ready: { label: 'Listo', className: 'bg-yellow-100 text-yellow-700' },
      analyzing: { label: 'Analizando', className: 'bg-purple-100 text-purple-700' },
      completed: { label: 'Completado', className: 'bg-green-100 text-green-700' },
      failed: { label: 'Error', className: 'bg-red-100 text-red-700' },
    };
    return badges[status] || badges.pending;
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Mis Escaneos</h1>
          <p className="text-gray-600 mt-1">
            Analiza espacios y genera guias de accesibilidad
          </p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn-primary"
        >
          <Plus className="h-4 w-4 mr-2" />
          Nuevo Escaneo
        </button>
      </div>

      {/* Create form modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
            <h2 className="text-lg font-bold text-gray-900 mb-4">
              Nuevo Escaneo
            </h2>
            <form onSubmit={handleCreateScan} className="space-y-4">
              <div>
                <label htmlFor="name" className="label">
                  Nombre *
                </label>
                <input
                  type="text"
                  id="name"
                  value={newScan.name}
                  onChange={(e) => setNewScan({ ...newScan, name: e.target.value })}
                  className="input"
                  placeholder="Ej: Museo del Prado"
                  required
                />
              </div>
              <div>
                <label htmlFor="location" className="label">
                  Ubicacion
                </label>
                <input
                  type="text"
                  id="location"
                  value={newScan.location || ''}
                  onChange={(e) => setNewScan({ ...newScan, location: e.target.value })}
                  className="input"
                  placeholder="Ej: Madrid, Espana"
                />
              </div>
              <div>
                <label htmlFor="description" className="label">
                  Descripcion
                </label>
                <textarea
                  id="description"
                  value={newScan.description || ''}
                  onChange={(e) => setNewScan({ ...newScan, description: e.target.value })}
                  className="input"
                  rows={3}
                  placeholder="Descripcion opcional del espacio"
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="btn-secondary flex-1"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={createScan.isPending}
                  className="btn-primary flex-1"
                >
                  {createScan.isPending ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    'Crear'
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Scans list */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
        </div>
      ) : scansData?.items.length === 0 ? (
        <div className="text-center py-12">
          <ImageIcon className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-1">
            No hay escaneos
          </h3>
          <p className="text-gray-500 mb-4">
            Crea tu primer escaneo para comenzar a analizar espacios
          </p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="btn-primary"
          >
            <Plus className="h-4 w-4 mr-2" />
            Crear Escaneo
          </button>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {scansData?.items.map((scan) => {
            const badge = getStatusBadge(scan.status);
            return (
              <div
                key={scan.id}
                className="card p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="font-medium text-gray-900 truncate flex-1">
                    {scan.name}
                  </h3>
                  <span
                    className={cn(
                      'ml-2 px-2 py-0.5 rounded-full text-xs font-medium',
                      badge.className
                    )}
                  >
                    {badge.label}
                  </span>
                </div>

                {scan.location && (
                  <div className="flex items-center text-sm text-gray-500 mb-2">
                    <MapPin className="h-4 w-4 mr-1" />
                    {scan.location}
                  </div>
                )}

                <div className="flex items-center text-sm text-gray-500 mb-4">
                  <ImageIcon className="h-4 w-4 mr-1" />
                  {scan.image_count} imagenes
                  <span className="mx-2">·</span>
                  <Calendar className="h-4 w-4 mr-1" />
                  {new Date(scan.created_at).toLocaleDateString()}
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => navigate(`/scan/${scan.id}/tour`)}
                    className="btn-primary flex-1 text-sm"
                  >
                    <Play className="h-4 w-4 mr-1" />
                    {scan.status === 'completed' ? 'Ver Tour' : 'Continuar'}
                  </button>
                  <button
                    onClick={() => handleDeleteScan(scan.id)}
                    disabled={deleteScan.isPending}
                    className="btn-secondary p-2"
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
