import React from 'react';
import { ShieldCheck, AlertCircle } from 'lucide-react';
import saraLogo from '../assets/SARA_Logo.png';

interface HeaderProps {
  apiConnected: boolean | null;
}

export const Header: React.FC<HeaderProps> = ({ apiConnected }) => {
  const isConnected = apiConnected === true;
  const isError = apiConnected === false;

  return (
    <header className="app-header">
      <div className="header-brand">
        <div className="brand-icon">
          <img src={saraLogo} alt="SARA Logo" style={{ width: '50px', height: '50px' }} />
        </div>
        <div className="brand-title">
          <h1>
            SARA
            <span className="brand-tag">Clinical Decision Support</span>
          </h1>
          <p>Synchronized Agentic Reasoning & Assistance — Biomedical Intelligence Workspace</p>
        </div>
      </div>

      <div className="header-status">
        {isError ? (
          <AlertCircle size={16} style={{ color: '#f43f5e' }} aria-hidden="true" />
        ) : (
          <ShieldCheck size={16} style={{ color: isConnected ? '#10b981' : '#94a3b8' }} aria-hidden="true" />
        )}
        <div className="status-indicator">
          <span>
            Backend API:{' '}
            <strong style={{ color: isConnected ? '#10b981' : isError ? '#f43f5e' : '#94a3b8' }}>
              {apiConnected === null
                ? 'Connecting...'
                : isConnected
                ? 'Connected'
                : 'Unavailable'}
            </strong>
          </span>
          <div className={`status-dot ${isConnected ? 'online' : isError ? 'offline' : ''}`} />
        </div>
      </div>
    </header>
  );
};
