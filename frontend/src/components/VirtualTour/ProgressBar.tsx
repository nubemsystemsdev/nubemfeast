import { cn } from '../../utils/cn';
import type { NavigationStep } from '../../types';

interface ProgressBarProps {
  currentStep: number;
  totalSteps: number;
  steps: NavigationStep[];
  onStepClick: (index: number) => void;
}

const RATING_DOT_COLORS = {
  accessible: 'bg-green-500',
  caution: 'bg-yellow-500',
  difficult: 'bg-orange-500',
  inaccessible: 'bg-red-500',
};

export default function ProgressBar({
  currentStep,
  totalSteps,
  steps,
  onStepClick,
}: ProgressBarProps) {
  const progressPercent = ((currentStep + 1) / totalSteps) * 100;

  return (
    <div className="bg-gray-800 px-4 py-2">
      {/* Progress line */}
      <div className="relative h-2 bg-gray-700 rounded-full overflow-hidden">
        <div
          className="absolute left-0 top-0 h-full bg-primary-500 transition-all duration-300"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* Step indicators */}
      <div className="flex justify-between mt-2">
        {steps.map((step, index) => (
          <button
            key={index}
            onClick={() => onStepClick(index)}
            className={cn(
              'relative w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium transition-all',
              index <= currentStep
                ? 'bg-primary-500 text-white'
                : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
            )}
            title={step.title}
          >
            {index + 1}
            {/* Accessibility rating dot */}
            <span
              className={cn(
                'absolute -bottom-1 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full',
                RATING_DOT_COLORS[step.accessibility_rating]
              )}
            />
          </button>
        ))}
      </div>
    </div>
  );
}
