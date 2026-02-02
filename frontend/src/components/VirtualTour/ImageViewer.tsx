import { useState } from 'react';
import { motion } from 'framer-motion';
import type { BarrierSummary } from '../../types';
import { cn } from '../../utils/cn';
import { SEVERITY_COLORS, BARRIER_TYPE_LABELS } from '../../utils/accessibility';

interface ImageViewerProps {
  imageUrl: string;
  barriers: BarrierSummary[];
  showBarrierOverlays?: boolean;
}

export default function ImageViewer({
  imageUrl,
  barriers,
  showBarrierOverlays = true,
}: ImageViewerProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [selectedBarrier, setSelectedBarrier] = useState<BarrierSummary | null>(null);

  return (
    <div className="relative w-full h-full bg-gray-900">
      {/* Loading state */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="animate-pulse text-gray-400">Cargando imagen...</div>
        </div>
      )}

      {/* Image */}
      <img
        src={imageUrl}
        alt="Vista del recorrido"
        onLoad={() => setIsLoading(false)}
        className={cn(
          'w-full h-full object-contain transition-opacity',
          isLoading ? 'opacity-0' : 'opacity-100'
        )}
      />

      {/* Barrier indicators (simplified - no bbox positioning) */}
      {showBarrierOverlays && barriers.length > 0 && (
        <div className="absolute bottom-20 left-4 right-4 flex flex-wrap gap-2 justify-center">
          {barriers.map((barrier, index) => (
            <motion.button
              key={barrier.id || index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() =>
                setSelectedBarrier(selectedBarrier?.id === barrier.id ? null : barrier)
              }
              className={cn(
                'px-3 py-1.5 rounded-full text-sm font-medium shadow-lg',
                SEVERITY_COLORS[barrier.severity],
                selectedBarrier?.id === barrier.id && 'ring-2 ring-white'
              )}
            >
              {BARRIER_TYPE_LABELS[barrier.barrier_type]}
            </motion.button>
          ))}
        </div>
      )}

      {/* Selected barrier detail */}
      {selectedBarrier && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          className="absolute bottom-32 left-4 right-4 mx-auto max-w-md bg-white rounded-xl shadow-xl p-4"
        >
          <div className="flex items-start justify-between mb-2">
            <h4 className="font-medium text-gray-900">
              {BARRIER_TYPE_LABELS[selectedBarrier.barrier_type]}
            </h4>
            <span
              className={cn(
                'px-2 py-0.5 rounded text-xs font-medium',
                SEVERITY_COLORS[selectedBarrier.severity]
              )}
            >
              {selectedBarrier.severity}
            </span>
          </div>
          <p className="text-sm text-gray-600 mb-2">{selectedBarrier.description}</p>
          {selectedBarrier.recommendation && (
            <p className="text-sm text-primary-600 bg-primary-50 p-2 rounded">
              {selectedBarrier.recommendation}
            </p>
          )}
          <button
            onClick={() => setSelectedBarrier(null)}
            className="mt-3 text-sm text-gray-500 hover:text-gray-700"
          >
            Cerrar
          </button>
        </motion.div>
      )}
    </div>
  );
}
