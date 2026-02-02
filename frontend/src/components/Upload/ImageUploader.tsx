import { useCallback, useState } from 'react';
import { Upload, X, Image as ImageIcon, Loader2 } from 'lucide-react';
import { cn } from '../../utils/cn';

interface ImageUploaderProps {
  onUpload: (files: File[]) => Promise<void>;
  maxFiles?: number;
  maxSizeMB?: number;
  disabled?: boolean;
  className?: string;
}

export default function ImageUploader({
  onUpload,
  maxFiles = 20,
  maxSizeMB = 10,
  disabled = false,
  className,
}: ImageUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [error, setError] = useState<string | null>(null);

  const validateFiles = useCallback(
    (files: File[]): { valid: File[]; errors: string[] } => {
      const valid: File[] = [];
      const errors: string[] = [];
      const maxSizeBytes = maxSizeMB * 1024 * 1024;

      for (const file of files) {
        if (!file.type.startsWith('image/')) {
          errors.push(`${file.name}: No es una imagen valida`);
          continue;
        }
        if (file.size > maxSizeBytes) {
          errors.push(`${file.name}: Excede el tamano maximo de ${maxSizeMB}MB`);
          continue;
        }
        valid.push(file);
      }

      if (valid.length > maxFiles) {
        errors.push(`Solo se permiten ${maxFiles} imagenes como maximo`);
        return { valid: valid.slice(0, maxFiles), errors };
      }

      return { valid, errors };
    },
    [maxFiles, maxSizeMB]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      setError(null);

      const files = Array.from(e.dataTransfer.files);
      const { valid, errors } = validateFiles(files);

      if (errors.length > 0) {
        setError(errors.join('. '));
      }

      if (valid.length > 0) {
        setSelectedFiles((prev) => [...prev, ...valid].slice(0, maxFiles));
      }
    },
    [validateFiles, maxFiles]
  );

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setError(null);
      const files = Array.from(e.target.files || []);
      const { valid, errors } = validateFiles(files);

      if (errors.length > 0) {
        setError(errors.join('. '));
      }

      if (valid.length > 0) {
        setSelectedFiles((prev) => [...prev, ...valid].slice(0, maxFiles));
      }

      // Reset input
      e.target.value = '';
    },
    [validateFiles, maxFiles]
  );

  const removeFile = useCallback((index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    setIsUploading(true);
    setError(null);

    try {
      await onUpload(selectedFiles);
      setSelectedFiles([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al subir imagenes');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className={cn('space-y-4', className)}>
      {/* Drop zone */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={cn(
          'border-2 border-dashed rounded-xl p-8 text-center transition-colors',
          isDragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
      >
        <input
          type="file"
          id="file-upload"
          multiple
          accept="image/*"
          onChange={handleFileSelect}
          disabled={disabled || isUploading}
          className="sr-only"
        />
        <label
          htmlFor="file-upload"
          className={cn(
            'cursor-pointer',
            disabled && 'cursor-not-allowed'
          )}
        >
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-4 text-sm text-gray-600">
            <span className="font-medium text-primary-600">
              Haz clic para seleccionar
            </span>{' '}
            o arrastra imagenes aqui
          </p>
          <p className="mt-1 text-xs text-gray-500">
            PNG, JPG, WebP hasta {maxSizeMB}MB (maximo {maxFiles} imagenes)
          </p>
        </label>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Selected files preview */}
      {selectedFiles.length > 0 && (
        <div className="space-y-3">
          <h4 className="text-sm font-medium text-gray-700">
            Imagenes seleccionadas ({selectedFiles.length})
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {selectedFiles.map((file, index) => (
              <div
                key={`${file.name}-${index}`}
                className="relative group rounded-lg overflow-hidden border border-gray-200"
              >
                <img
                  src={URL.createObjectURL(file)}
                  alt={file.name}
                  className="w-full h-24 object-cover"
                />
                <button
                  onClick={() => removeFile(index)}
                  className="absolute top-1 right-1 p-1 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <X className="h-4 w-4" />
                </button>
                <div className="absolute bottom-0 left-0 right-0 bg-black/50 px-2 py-1">
                  <p className="text-xs text-white truncate">{file.name}</p>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={handleUpload}
            disabled={isUploading || disabled}
            className="btn-primary w-full"
          >
            {isUploading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Subiendo...
              </>
            ) : (
              <>
                <ImageIcon className="h-4 w-4 mr-2" />
                Subir {selectedFiles.length} imagen
                {selectedFiles.length > 1 ? 'es' : ''}
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}
