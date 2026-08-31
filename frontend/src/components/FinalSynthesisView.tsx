import React from 'react';
import type { FinalSynthesis } from '../types/sara';
import { AlertTriangle, Compass, CheckSquare, Stethoscope, HelpCircle, GitFork, ShieldAlert } from 'lucide-react';

interface FinalSynthesisViewProps {
  synthesis: FinalSynthesis;
}

export const FinalSynthesisView: React.FC<FinalSynthesisViewProps> = ({ synthesis }) => {
  return (
    <div className="synthesis-container">
      {/* Primary Clinical Direction Hero Card */}
      <div className="hero-synthesis-card">
        <div className="hero-content">
          <div className="hero-label">
            <Compass size={16} aria-hidden="true" />
            <span>Primary Clinical Direction / Working Hypothesis</span>
          </div>
          <h2 className="hero-title">{synthesis.primary_clinical_direction}</h2>
        </div>
        <div className="metric-ring-container">
          <span className="ring-score-val">{synthesis.confidence.toFixed(0)}%</span>
          <span className="ring-score-label">Synthesis Confidence</span>
        </div>
      </div>

      {/* Mandatory Clinical Caution Alert */}
      <div className="caution-alert-banner">
        <AlertTriangle className="caution-alert-icon" size={22} aria-hidden="true" />
        <div className="caution-alert-body">
          <h4>Clinical Decision Support Advisory</h4>
          <p>{synthesis.clinical_caution}</p>
        </div>
      </div>

      {/* Core Reasoning & Supporting Findings Grid */}
      <div className="section-grid-2">
        {/* Core Reasoning */}
        <div className="sub-card">
          <div className="sub-card-title">
            <Compass size={18} style={{ color: '#3b82f6' }} aria-hidden="true" />
            <span>Core Reasoning Pipeline</span>
          </div>
          <div className="reasoning-list">
            {synthesis.reasoning.map((item, idx) => (
              <div key={idx} className="reasoning-item">
                <div className="reasoning-num-badge">{String(idx + 1).padStart(2, '0')}</div>
                <div className="reasoning-text">{item}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Supporting Findings */}
        <div className="sub-card">
          <div className="sub-card-title">
            <CheckSquare size={18} style={{ color: '#10b981' }} aria-hidden="true" />
            <span>Supporting Key Findings</span>
          </div>
          <ul className="clinical-bullet-list">
            {synthesis.supporting_findings.map((item, idx) => (
              <li key={idx} className="clinical-bullet-item">
                <div className="bullet-icon-wrapper">
                  <CheckSquare size={15} style={{ color: '#10b981' }} aria-hidden="true" />
                </div>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Recommended Investigations & Unresolved Questions */}
      <div className="section-grid-2">
        {/* Recommended Investigations */}
        <div className="sub-card">
          <div className="sub-card-title">
            <Stethoscope size={18} style={{ color: '#f59e0b' }} aria-hidden="true" />
            <span>Recommended Next Investigations</span>
          </div>
          <ul className="clinical-bullet-list">
            {synthesis.recommended_investigations.map((item, idx) => (
              <li key={idx} className="clinical-bullet-item">
                <div className="bullet-icon-wrapper">
                  <Stethoscope size={15} style={{ color: '#f59e0b' }} aria-hidden="true" />
                </div>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Unresolved Questions */}
        <div className="sub-card">
          <div className="sub-card-title">
            <HelpCircle size={18} style={{ color: '#f43f5e' }} aria-hidden="true" />
            <span>Unresolved Clinical Questions</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {synthesis.unresolved_questions.map((item, idx) => (
              <div key={idx} className="uncertainty-item">
                <ShieldAlert size={16} style={{ color: '#f43f5e', flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Alternative Hypotheses */}
      {synthesis.alternative_hypotheses.length > 0 && (
        <div className="sub-card">
          <div className="sub-card-title">
            <GitFork size={18} style={{ color: '#c084fc' }} aria-hidden="true" />
            <span>Alternative Hypotheses Evaluated</span>
          </div>
          <div className="hypothesis-card-list">
            {synthesis.alternative_hypotheses.map((alt, idx) => (
              <div key={idx} className="alt-hypothesis-card">
                <div className="alt-hypothesis-header">
                  <span className="alt-hypothesis-title">{alt.name}</span>
                  <span className="likelihood-pill moderate">Differential Option</span>
                </div>
                <p className="alt-hypothesis-reason">{alt.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
