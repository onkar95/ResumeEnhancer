import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import AppLayout from "./components/layout/AppLayout";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import GeneratePage from "./pages/GeneratePage";
import ReviewPage from "./pages/ReviewPage";
import HistoryPage from "./pages/HistoryPage";
import AssistantPage from "./pages/AssistantPage";

export default function App() {
  return <BrowserRouter><AuthProvider><Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route element={<ProtectedRoute />}><Route element={<AppLayout />}>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/generate" element={<GeneratePage />} />
      <Route path="/history" element={<HistoryPage />} />
      <Route path="/versions" element={<HistoryPage mode="versions" />} />
      <Route path="/review/:runId" element={<ReviewPage />} />
      <Route path="/review/:runId/assistant" element={<AssistantPage />} />
      <Route path="/review/:runId/assistant/suggestions" element={<AssistantPage />} />
      <Route path="/review/:runId/assistant/chat" element={<AssistantPage />} />
    </Route></Route>
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes></AuthProvider></BrowserRouter>;
}
