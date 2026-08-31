import React from 'react';
import { Users, MessageSquare, Scale, Award, CheckCircle2, AlertCircle, Clock, Loader2 } from 'lucide-react';

interface PipelineStepperProps {
  isLoading: boolean;
  isComplete: boolean;
  hasError?: boolean;
}

interface Step {
  id: number;
  title: string;
  desc: string;
  icon: React.ReactNode;
}

const STEPS: Step[] = [
  {
    id: 1,
    title: 'Agent Analysis',
    desc: 'AURA, NEXA, LYRA & ITHRA reasoning',
    icon: <Users size={16} aria-hidden="true" />,
  },
  {
    id: 2,
    title: 'Multi-Agent Debate',
    desc: 'Cross-agent critique & evaluation',
    icon: <MessageSquare size={16} aria-hidden="true" />,
  },
  {
    id: 3,
    title: 'Consensus Engine',
    desc: 'Convergence & agreement evaluation',
    icon: <Scale size={16} aria-hidden="true" />,
  },
  {
    id: 4,
    title: 'Final Synthesis',
    desc: 'Clinical reasoning & direction summary',
    icon: <Award size={16} aria-hidden="true" />,
  },
];

export const PipelineStepper: React.FC<PipelineStepperProps> = ({
  isLoading,
  isComplete,
  hasError = false,
}) => {
  return (
    <div className="card pipeline-card">
      <div className="card-header-bar" style={{ marginBottom: '0.85rem' }}>
        <div className="card-title" style={{ fontSize: '0.95rem' }}>
          <Clock size={18} style={{ color: '#6366f1' }} aria-hidden="true" />
          <span>Reasoning Pipeline Lifecycle</span>
        </div>
        {isLoading && (
          <span className="step-status-tag running" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Loader2 size={12} className="spin-icon" style={{ animation: 'spin 1s linear infinite' }} aria-hidden="true" />
            Processing
          </span>
        )}
        {isComplete && (
          <span className="step-status-tag completed">
            Completed
          </span>
        )}
      </div>

      <div className="stepper-list">
        {STEPS.map((step) => {
          const isFinished = isComplete;
          const isRunning = isLoading;
          const isFailed = hasError && !isLoading && !isComplete;

          let itemClass = '';
          if (isFinished) itemClass = 'completed';
          else if (isRunning) itemClass = 'running';
          else if (isFailed) itemClass = 'failed';

          return (
            <div key={step.id} className={`step-item ${itemClass}`}>
              <div className="step-badge">
                {isFinished ? (
                  <CheckCircle2 size={16} aria-hidden="true" />
                ) : isFailed ? (
                  <AlertCircle size={16} aria-hidden="true" />
                ) : isRunning ? (
                  <Loader2 size={16} style={{ animation: 'spin 1s linear infinite' }} aria-hidden="true" />
                ) : (
                  step.id
                )}
              </div>
              <div className="step-info">
                <div className="step-title-row">
                  <span className="step-title">{step.title}</span>
                  {isRunning && (
                    <span className="step-status-tag running">Active</span>
                  )}
                </div>
                <span className="step-desc">{step.desc}</span>
              </div>
            </div>
          );
        })}
      </div>

      {isLoading && (
        <div style={{ marginTop: '0.85rem', fontSize: '0.775rem', color: '#818cf8', fontStyle: 'italic', textAlign: 'center' }}>
          SARA is processing the case through its multi-agent reasoning pipeline...
        </div>
      )}
    </div>
  );
};
