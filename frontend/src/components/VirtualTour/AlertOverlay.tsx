import { motion } from 'framer-motion';
import { AlertTriangle, X } from 'lucide-react';
import { useState } from 'react';

interface AlertOverlayProps {
  alerts: string[];
}

export default function AlertOverlay({ alerts }: AlertOverlayProps) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed || alerts.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="absolute top-4 left-4 right-4 mx-auto max-w-md"
    >
      <div className="bg-yellow-500 text-yellow-900 rounded-xl shadow-lg p-4">
        <div className="flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h4 className="font-medium mb-1">Atencion</h4>
            <ul className="text-sm space-y-1">
              {alerts.map((alert, index) => (
                <li key={index}>{alert}</li>
              ))}
            </ul>
          </div>
          <button
            onClick={() => setDismissed(true)}
            className="p-1 hover:bg-yellow-600/20 rounded"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
