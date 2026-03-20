import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import DashboardLayout from "./components/layout/DashboardLayout";
import Overview from "./pages/dashboard/Overview";
import LiveStream from "./pages/dashboard/LiveStream";
import VideoUpload from "./pages/upload/VideoUpload";
import IncidentLog from "./pages/incidents/IncidentLog";
import BehaviorAnalytics from "./pages/analytics/BehaviorAnalytics";
import Settings from "./pages/settings/Settings";
import Auth from "./pages/auth/Auth";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Route */}
        <Route path="/auth" element={<Auth />} />

        {/* Protected Dashboard Routes */}
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<Overview />} />
          <Route path="stream" element={<LiveStream />} />
          <Route path="upload" element={<VideoUpload />} />
          <Route path="incidents" element={<IncidentLog />} />
          <Route path="analytics" element={<BehaviorAnalytics />} />
          <Route path="settings" element={<Settings />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/auth" replace />} />
      </Routes>
    </BrowserRouter>
  );
}