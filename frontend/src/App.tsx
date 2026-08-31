import { useState, useEffect } from 'react';
import type { SARAResponse } from './types/sara';
import { analyzeCase } from './services/api';
import { Header } from './components/Header';
import { CaseInput } from './components/CaseInput';
import { PipelineStepper } from './components/PipelineStepper';
import { FinalSynthesisView } from './components/FinalSynthesisView';
import { ConsensusDebateView } from './components/ConsensusDebateView';
import { AgentMatrixView } from './components/AgentMatrixView';
import { Award, Scale, Users, Activity, AlertOctagon, ChevronDown, ChevronUp } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export function App() {
  const [caseText, setCaseText] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isComplete, setIsComplete] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [showTechDetails, setShowTechDetails] = useState<boolean>(false);
  const [result, setResult] = useState<SARAResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'synthesis' | 'consensus' | 'agents'>('synthesis');
  const [apiConnected, setApiConnected] = useState<boolean | null>(null);

  // Check backend API connectivity on initial load
  useEffect(() => {
    async function checkApi() {
      try {
        const res = await fetch(`${API_BASE_URL}/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ case_text: '' }), // dummy reachability check
        });
        if (res.status === 400 || res.status === 422 || res.ok) {
          setApiConnected(true);
        } else {
          setApiConnected(false);
        }
      } catch {
        setApiConnected(false);
      }
    }
    checkApi();
  }, []);

  const handleAnalyze = async () => {
    if (!caseText.trim()) {
      setError('Please provide a biomedical case description to analyze.');
      setShowTechDetails(false);
      return;
    }

    setIsLoading(true);
    setIsComplete(false);
    setError(null);
    setShowTechDetails(false);

    try {
      const data = await analyzeCase(caseText);
      setResult(data);
      setIsComplete(true);
      setApiConnected(true);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred during case analysis.');
      }
      setApiConnected(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setCaseText('');
    setResult(null);
    setError(null);
    setShowTechDetails(false);
    setIsLoading(false);
    setIsComplete(false);
    setActiveTab('synthesis');
  };

  return (
    <div className="app-container">
      {/* Header Bar */}
      <Header apiConnected={apiConnected} />

      {/* Main Workspace Grid */}
      <main className="main-grid">
        {/* Left Column: Input Terminal & Lifecycle Pipeline Stepper */}
        <div>
          <CaseInput
            caseText={caseText}
            setCaseText={setCaseText}
            onAnalyze={handleAnalyze}
            onReset={handleReset}
            isLoading={isLoading}
          />
          <PipelineStepper isLoading={isLoading} isComplete={isComplete} hasError={!!error} />
        </div>

        {/* Right Column: Analytics & Clinical Decision Workspace */}
        <div className="card">
          {/* Friendly Error Banner with Technical Details Toggle */}
          {error && (
            <div className="error-banner-container">
              <div className="error-banner-main">
                <AlertOctagon size={22} style={{ color: '#f43f5e', flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
                <div>
                  <strong style={{ color: '#ffffff' }}>Unable to complete SARA analysis.</strong>
                  <div style={{ fontSize: '0.875rem', marginTop: '4px' }}>
                    Please verify that the backend FastAPI server is running and try again.
                  </div>
                </div>
              </div>

              <button
                type="button"
                className="tech-details-toggle"
                onClick={() => setShowTechDetails(!showTechDetails)}
              >
                {showTechDetails ? (
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    Hide Technical Details <ChevronUp size={14} aria-hidden="true" />
                  </span>
                ) : (
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    Show Technical Details <ChevronDown size={14} aria-hidden="true" />
                  </span>
                )}
              </button>

              {showTechDetails && (
                <div className="tech-details-box">
                  {error}
                </div>
              )}
            </div>
          )}

          {/* Results Workspace */}
          {result ? (
            <div>
              {/* Tab Navigation */}
              <div className="dashboard-tabs">
                <button
                  type="button"
                  className={`tab-btn ${activeTab === 'synthesis' ? 'active' : ''}`}
                  onClick={() => setActiveTab('synthesis')}
                >
                  <Award size={18} aria-hidden="true" />
                  Clinical Synthesis
                </button>

                <button
                  type="button"
                  className={`tab-btn ${activeTab === 'consensus' ? 'active' : ''}`}
                  onClick={() => setActiveTab('consensus')}
                >
                  <Scale size={18} aria-hidden="true" />
                  Consensus & Debate
                  <span className="tab-count-badge">{result.debate.length}</span>
                </button>

                <button
                  type="button"
                  className={`tab-btn ${activeTab === 'agents' ? 'active' : ''}`}
                  onClick={() => setActiveTab('agents')}
                >
                  <Users size={18} aria-hidden="true" />
                  4-Agent Matrix
                </button>
              </div>

              {/* Active Tab View Rendering */}
              {activeTab === 'synthesis' && (
                <FinalSynthesisView synthesis={result.final_synthesis} />
              )}

              {activeTab === 'consensus' && (
                <ConsensusDebateView
                  consensus={result.consensus}
                  debate={result.debate}
                />
              )}

              {activeTab === 'agents' && (
                <AgentMatrixView analyses={result.analyses} />
              )}
            </div>
          ) : (
            /* Initial Empty State */
            <div className="empty-state">
              <Activity className="empty-icon" aria-hidden="true" />
              <h3 style={{ fontSize: '1.25rem', color: '#ffffff', marginBottom: '0.5rem' }}>
                SARA Biomedical Intelligence Workspace
              </h3>
              <p style={{ maxWidth: '500px', fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>
                Enter or select a biomedical mystery case on the left panel and click <strong>"Run SARA Analysis"</strong> to initiate the 4-agent reasoning, multi-agent debate, and consensus engine pipeline.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
