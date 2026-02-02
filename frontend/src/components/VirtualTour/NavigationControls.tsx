import { ChevronLeft, ChevronRight, Flag } from 'lucide-react';
import { cn } from '../../utils/cn';

interface NavigationControlsProps {
  currentStep: number;
  totalSteps: number;
  onPrev: () => void;
  onNext: () => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

export default function NavigationControls({
  currentStep,
  totalSteps,
  onPrev,
  onNext,
  isFirstStep,
  isLastStep,
}: NavigationControlsProps) {
  return (
    <div className="bg-gray-800 px-4 py-3 flex items-center justify-between">
      <button
        onClick={onPrev}
        disabled={isFirstStep}
        className={cn(
          'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
          isFirstStep
            ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
            : 'bg-gray-700 text-white hover:bg-gray-600'
        )}
      >
        <ChevronLeft className="h-4 w-4" />
        Anterior
      </button>

      <div className="text-white text-sm">
        <span className="font-medium">{currentStep + 1}</span>
        <span className="text-gray-400"> / {totalSteps}</span>
      </div>

      <button
        onClick={onNext}
        className={cn(
          'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
          isLastStep
            ? 'bg-green-600 text-white hover:bg-green-700'
            : 'bg-primary-600 text-white hover:bg-primary-700'
        )}
      >
        {isLastStep ? (
          <>
            Finalizar
            <Flag className="h-4 w-4" />
          </>
        ) : (
          <>
            Siguiente
            <ChevronRight className="h-4 w-4" />
          </>
        )}
      </button>
    </div>
  );
}
