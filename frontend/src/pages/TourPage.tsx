import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, AlertCircle, Upload, Play, ArrowLeft } from 'lucide-react';
import { useScan, useUploadImages } from '../hooks/useScans';
import { useStartAnalysis, useAnalysis } from '../hooks/useAnalysis';
import { useGuide, useGenerateGuide } from '../hooks/useGuide';
import ImageUploader from '../components/Upload/ImageUploader';
import VirtualTourViewer from '../components/VirtualTour/VirtualTourViewer';
import { cn } from '../utils/cn';

type PageState = 'upload' | 'analyzing' | 'tour';

export default function TourPage() {
  const { scanId } = useParams<{ scanId: string }>();
  const navigate = useNavigate();
  const [pageState, setPageState] = useState<PageState>('upload');

  const { data: scan, isLoading: scanLoading, error: scanError } = useScan(scanId!);
  const uploadImages = useUploadImages();
  const startAnalysis = useStartAnalysis();
  const generateGuide = useGenerateGuide();

  // Only fetch analysis/guide when needed
  const { data: analysis, refetch: refetchAnalysis } = useAnalysis(scanId!);
  const { data: guide, refetch: refetchGuide } = useGuide(scanId!);

  const handleUpload = async (files: File[]) => {
    await uploadImages.mutateAsync({ scanId: scanId!, files });
  };

  const handleStartAnalysis = async () => {
    setPageState('analyzing');

    try {
      // Start analysis
      await startAnalysis.mutateAsync({ scanId: scanId! });

      // Poll for completion
      const pollInterval = setInterval(async () => {
        const result = await refetchAnalysis();
        if (result.data?.status === 'completed') {
          clearInterval(pollInterval);

          // Generate guide
          await generateGuide.mutateAsync({ scanId: scanId! });
          await refetchGuide();

          setPageState('tour');
        } else if (result.data?.status === 'failed') {
          clearInterval(pollInterval);
          setPageState('upload');
        }
      }, 2000);
    } catch (error) {
      console.error('Analysis error:', error);
      setPageState('upload');
    }
  };

  const handleTourComplete = () => {
    navigate(`/scan/${scanId}/summary`);
  };

  if (scanLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
      </div>
    );
  }

  if (scanError || !scan) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
        <h2 className="text-lg font-medium text-gray-900 mb-2">
          Error al cargar el escaneo
        </h2>
        <button onClick={() => navigate('/')} className="btn-secondary">
          Volver al inicio
        </button>
      </div>
    );
  }

  // Determine actual page state based on scan status
  const effectiveState =
    scan.status === 'completed' && guide ? 'tour' : scan.status === 'analyzing' ? 'analyzing' : pageState;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/')} className="btn-secondary p-2">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-gray-900">{scan.name}</h1>
          {scan.location && (
            <p className="text-sm text-gray-500">{scan.location}</p>
          )}
        </div>
      </div>

      {/* Upload state */}
      {effectiveState === 'upload' && (
        <div className="card p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            Sube las imagenes del recorrido
          </h2>
          <p className="text-gray-600 mb-6">
            Sube fotos en orden del recorrido que deseas analizar. El sistema
            detectara barreras de accesibilidad y generara una guia de
            navegacion.
          </p>

          <ImageUploader
            onUpload={handleUpload}
            disabled={uploadImages.isPending}
          />

          {/* Current images */}
          {scan.images.length > 0 && (
            <div className="mt-8">
              <h3 className="text-sm font-medium text-gray-700 mb-3">
                Imagenes subidas ({scan.images.length})
              </h3>
              <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-2">
                {scan.images.map((image, index) => (
                  <div
                    key={image.id}
                    className="aspect-square rounded-lg overflow-hidden border border-gray-200"
                  >
                    <img
                      src={`/api/scans/${scanId}/images/${image.id}/file`}
                      alt={`Imagen ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                ))}
              </div>

              <button
                onClick={handleStartAnalysis}
                disabled={scan.images.length === 0}
                className="btn-primary mt-6 w-full sm:w-auto"
              >
                <Play className="h-4 w-4 mr-2" />
                Analizar Accesibilidad
              </button>
            </div>
          )}
        </div>
      )}

      {/* Analyzing state */}
      {effectiveState === 'analyzing' && (
        <div className="card p-8 text-center">
          <Loader2 className="h-12 w-12 animate-spin text-primary-600 mx-auto mb-4" />
          <h2 className="text-lg font-medium text-gray-900 mb-2">
            Analizando imagenes...
          </h2>
          <p className="text-gray-600">
            Estamos detectando barreras de accesibilidad en las {scan.images.length} imagenes.
            Esto puede tardar unos minutos.
          </p>
          {analysis && (
            <p className="text-sm text-gray-500 mt-4">
              Progreso: {analysis.total_images_analyzed} / {scan.images.length} imagenes analizadas
            </p>
          )}
        </div>
      )}

      {/* Tour state */}
      {effectiveState === 'tour' && guide && (
        <div className="h-[calc(100vh-200px)] min-h-[500px]">
          <VirtualTourViewer
            guide={guide}
            scanId={scanId!}
            onComplete={handleTourComplete}
          />
        </div>
      )}
    </div>
  );
}
