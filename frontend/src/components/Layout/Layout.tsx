import { Outlet, Link } from 'react-router-dom';
import { Accessibility } from 'lucide-react';

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2">
              <Accessibility className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">NubemFeast</span>
            </Link>
            <nav className="flex items-center gap-4">
              <Link
                to="/"
                className="text-gray-600 hover:text-gray-900 text-sm font-medium"
              >
                Inicio
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            NubemFeast - Sistema de Accesibilidad para Sillas de Ruedas
          </p>
        </div>
      </footer>
    </div>
  );
}
