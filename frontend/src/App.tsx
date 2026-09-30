import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Topbar } from './components/Topbar';
import { DashboardPage } from './pages/DashboardPage';
import { TransformWorkspace } from './pages/TransformWorkspace';
import { ProjectsPage } from './pages/ProjectsPage';
import { HistoryPage } from './pages/HistoryPage';
import { TemplatesPage } from './pages/TemplatesPage';
import { ValidationPage } from './pages/ValidationPage';
import { ExportsPage } from './pages/ExportsPage';
import { AuditLogsPage } from './pages/AuditLogsPage';
import { SettingsPage } from './pages/SettingsPage';
import { Template, SystemSettings } from './types';
import { api } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [userRole, setUserRole] = useState('Analyst');
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const [demoMode, setDemoMode] = useState(true);

  useEffect(() => {
    api.getSettings().then(s => setDemoMode(s.demo_mode)).catch(() => {});
  }, []);

  const handleStartNewTransformation = () => {
    setSelectedProjectId(null);
    setActiveTab('transform');
  };

  const handleViewProject = (projectId: number) => {
    setSelectedProjectId(projectId);
    setActiveTab('transform');
  };

  const handleApplyTemplate = (template: Template) => {
    setSelectedProjectId(null);
    setActiveTab('transform');
  };

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        demoMode={demoMode}
        userRole={userRole}
      />

      {/* Main Content Viewport */}
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar
          userRole={userRole}
          setUserRole={setUserRole}
          onNewTransformation={handleStartNewTransformation}
        />

        <main className="flex-1 overflow-y-auto">
          {activeTab === 'dashboard' && (
            <DashboardPage
              onStartNewTransformation={handleStartNewTransformation}
              onViewProject={handleViewProject}
            />
          )}

          {activeTab === 'transform' && (
            <TransformWorkspace
              key={selectedProjectId || 'new'}
              initialProjectId={selectedProjectId}
            />
          )}

          {activeTab === 'projects' && (
            <ProjectsPage
              onOpenProject={handleViewProject}
              onNewTransformation={handleStartNewTransformation}
            />
          )}

          {activeTab === 'history' && (
            <HistoryPage
              onInspectProject={handleViewProject}
            />
          )}

          {activeTab === 'templates' && (
            <TemplatesPage
              onApplyTemplate={handleApplyTemplate}
            />
          )}

          {activeTab === 'validation' && (
            <ValidationPage />
          )}

          {activeTab === 'exports' && (
            <ExportsPage />
          )}

          {activeTab === 'audit-logs' && (
            <AuditLogsPage />
          )}

          {activeTab === 'settings' && (
            <SettingsPage
              onSettingsUpdated={(s) => setDemoMode(s.demo_mode)}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
