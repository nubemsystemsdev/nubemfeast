import { motion } from 'framer-motion';
import { Lightbulb, AlertCircle } from 'lucide-react';
import type { NavigationStep } from '../../types';
import { cn } from '../../utils/cn';
import { RATING_COLORS, RATING_LABELS } from '../../utils/accessibility';

interface InstructionPanelProps {
  step: NavigationStep;
}

export default function InstructionPanel({ step }: InstructionPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-white border-t border-gray-200 p-4"
    >
      {/* Title and rating */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-medium text-gray-900">{step.title}</h3>
        <span
          className={cn(
            'px-3 py-1 rounded-full text-sm font-medium',
            RATING_COLORS[step.accessibility_rating]
          )}
        >
          {RATING_LABELS[step.accessibility_rating]}
        </span>
      </div>

      {/* Description */}
      {step.description && (
        <p className="text-gray-600 text-sm mb-3">{step.description}</p>
      )}

      {/* Recommendations */}
      {step.recommendations.length > 0 && (
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 mb-3">
          <div className="flex items-start gap-2">
            <Lightbulb className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-medium text-blue-800 mb-1">
                Recomendaciones
              </h4>
              <ul className="text-sm text-blue-700 space-y-1">
                {step.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Barrier count indicator */}
      {step.barriers.length > 0 && (
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <AlertCircle className="h-4 w-4" />
          <span>
            {step.barriers.length} barrera{step.barriers.length > 1 ? 's' : ''} detectada
            {step.barriers.length > 1 ? 's' : ''}
          </span>
        </div>
      )}
    </motion.div>
  );
}
