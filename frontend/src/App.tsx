import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import HomePage from './pages/HomePage';
import TourPage from './pages/TourPage';
import SummaryPage from './pages/SummaryPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="scan/:scanId/tour" element={<TourPage />} />
        <Route path="scan/:scanId/summary" element={<SummaryPage />} />
      </Route>
    </Routes>
  );
}

export default App;
