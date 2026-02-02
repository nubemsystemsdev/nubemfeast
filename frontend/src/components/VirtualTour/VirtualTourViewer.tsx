import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, AlertTriangle, Info } from 'lucide-react';
import type { NavigationStep, Guide } from '../../types';
import { cn } from '../../utils/cn';
import { RATING_COLORS, RATING_LABELS, SEVERITY_COLORS } from '../../utils/accessibility';
import ImageViewer from './ImageViewer';
import NavigationControls from './NavigationControls';
import ProgressBar from './ProgressBar';
import AlertOverlay from './AlertOverlay';
import InstructionPanel from './InstructionPanel';

interface VirtualTourViewerProps {
  guide: Guide;
  scanId: string;
  onComplete?: () => void;
}

export default function VirtualTourViewer({
  guide,
  scanId,
  onComplete,
}: VirtualTourViewerProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [showAlerts, setShowAlerts] = useState(true);
  const [direction, setDirection] = useState(0);

  const currentStep = guide.navigation_steps[currentStepIndex];
  const totalSteps = guide.navigation_steps.length;
  const isFirstStep = currentStepIndex === 0;
  const isLastStep = currentStepIndex === totalSteps - 1;

  const goToStep = (index: number) => {
    if (index < 0 || index >= totalSteps) return;
    setDirection(index > currentStepIndex ? 1 : -1);
    setCurrentStepIndex(index);
  };

  const goNext = () => {
    if (isLastStep) {
      onComplete?.();
    } else {
      goToStep(currentStepIndex + 1);
    }
  };

  const goPrev = () => {
    goToStep(currentStepIndex - 1);
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        goNext();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        goPrev();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentStepIndex, isLastStep]);

  return (
    <div className="flex flex-col h-full bg-gray-900 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 px-4 py-3 flex items-center justify-between">
        <div>
          <h2 className="text-white font-medium">{guide.title}</h2>
          <p className="text-gray-400 text-sm">
            Paso {currentStepIndex + 1} de {totalSteps}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {currentStep.barriers.length > 0 && (
            <button
              onClick={() => setShowAlerts(!showAlerts)}
              className={cn(
                'p-2 rounded-lg transition-colors',
                showAlerts
                  ? 'bg-yellow-500 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              )}
              title={showAlerts ? 'Ocultar alertas' : 'Mostrar alertas'}
            >
              <AlertTriangle className="h-5 w-5" />
            </button>
          )}
        </div>
      </div>

      {/* Progress bar */}
      <ProgressBar
        currentStep={currentStepIndex}
        totalSteps={totalSteps}
        steps={guide.navigation_steps}
        onStepClick={goToStep}
      />

      {/* Main content */}
      <div className="flex-1 relative">
        <AnimatePresence mode="wait" custom={direction}>
          <motion.div
            key={currentStepIndex}
            custom={direction}
            initial={{ opacity: 0, x: direction * 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -direction * 100 }}
            transition={{ duration: 0.3 }}
            className="absolute inset-0"
          >
            <ImageViewer
              imageUrl={`/api/scans/${scanId}/images/${currentStep.image_id}/file`}
              barriers={currentStep.barriers}
              showBarrierOverlays={showAlerts}
            />
          </motion.div>
        </AnimatePresence>

        {/* Alert overlay */}
        {showAlerts && currentStep.alerts.length > 0 && (
          <AlertOverlay alerts={currentStep.alerts} />
        )}

        {/* Navigation arrows */}
        <button
          onClick={goPrev}
          disabled={isFirstStep}
          className={cn(
            'absolute left-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-black/50 text-white transition-all',
            isFirstStep
              ? 'opacity-30 cursor-not-allowed'
              : 'hover:bg-black/70 hover:scale-110'
          )}
        >
          <ChevronLeft className="h-6 w-6" />
        </button>

        <button
          onClick={goNext}
          className={cn(
            'absolute right-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-black/50 text-white transition-all',
            'hover:bg-black/70 hover:scale-110'
          )}
        >
          <ChevronRight className="h-6 w-6" />
        </button>
      </div>

      {/* Instruction panel */}
      <InstructionPanel step={currentStep} />

      {/* Navigation controls */}
      <NavigationControls
        currentStep={currentStepIndex}
        totalSteps={totalSteps}
        onPrev={goPrev}
        onNext={goNext}
        isFirstStep={isFirstStep}
        isLastStep={isLastStep}
      />
    </div>
  );
}
