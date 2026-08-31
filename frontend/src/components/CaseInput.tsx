import React from 'react';
import { Play, RotateCcw, FileText, ChevronRight, Loader2 } from 'lucide-react';

interface CaseInputProps {
  caseText: string;
  setCaseText: (text: string) => void;
  onAnalyze: () => void;
  onReset: () => void;
  isLoading: boolean;
}

const SAMPLE_CASES = [
  {
    title: 'Case 1: Muscle Weakness & Fatigue',
    text: `A 32-year-old woman presents with progressive fatigue, shortness of breath, and muscle weakness over several months. Symptoms worsen after physical activity. Laboratory investigations show elevated creatine kinase (CK) and mild anemia. There is no known history of trauma or recent infection.`
  },
  {
    title: 'Case 2: Episodic Fever & Joint Pain',
    text: `A 45-year-old man presents with recurrent episodes of high fever, migratory joint pain, and an evanescent salmon-pink rash over the trunk and extremities during fever spikes. Lab results reveal severe neutrophilic leukocytosis, elevated ferritin levels (>5000 ng/mL), and negative ANA and Rheumatoid Factor.`
  }
];

export const CaseInput: React.FC<CaseInputProps> = ({
  caseText,
  setCaseText,
  onAnalyze,
  onReset,
  isLoading
}) => {
  const wordCount = caseText.trim() ? caseText.trim().split(/\s+/).length : 0;
  const charCount = caseText.length;

  return (
    <div className="card input-panel">
      <div className="card-header-bar" style={{ marginBottom: '0.85rem' }}>
        <div className="card-title">
          <FileText size={18} style={{ color: '#3b82f6' }} aria-hidden="true" />
          <span>Clinical Case Presentation</span>
        </div>
      </div>

      <div className="preset-section">
        <span className="preset-label">Load Sample Clinical Mysteries:</span>
        <div className="preset-buttons">
          {SAMPLE_CASES.map((sample, idx) => {
            const isSelected = caseText === sample.text;
            return (
              <button
                key={idx}
                type="button"
                className={`btn-preset ${isSelected ? 'active' : ''}`}
                onClick={() => setCaseText(sample.text)}
                disabled={isLoading}
              >
                <span>{sample.title}</span>
                <ChevronRight size={14} style={{ color: 'var(--text-dim)' }} aria-hidden="true" />
              </button>
            );
          })}
        </div>
      </div>

      <div className="textarea-container">
        <textarea
          className="case-textarea"
          placeholder="Paste or type clinical case details, patient symptoms, lab values, diagnostic imaging summaries, and medical history..."
          value={caseText}
          onChange={(e) => setCaseText(e.target.value)}
          disabled={isLoading}
          aria-label="Clinical case description input"
        />
        <div className="input-footer">
          <div className="live-stats">
            <span><strong>{wordCount}</strong> words</span>
            <span>|</span>
            <span><strong>{charCount}</strong> characters</span>
          </div>
          <span>SARA Multi-Agent Architecture</span>
        </div>
      </div>

      <div className="action-buttons">
        <button
          type="button"
          className="btn-primary"
          onClick={onAnalyze}
          disabled={isLoading || !caseText.trim()}
          aria-label="Run SARA Analysis"
        >
          {isLoading ? (
            <>
              <Loader2 size={18} className="spin-icon" style={{ animation: 'spin 1s linear infinite' }} aria-hidden="true" />
              <span>Analyzing Pipeline...</span>
            </>
          ) : (
            <>
              <Play size={18} aria-hidden="true" />
              <span>Run SARA Analysis</span>
            </>
          )}
        </button>

        <button
          type="button"
          className="btn-secondary"
          onClick={onReset}
          disabled={isLoading || (!caseText && !isLoading)}
          aria-label="Reset input and workspace"
        >
          <RotateCcw size={16} aria-hidden="true" />
          <span>Reset</span>
        </button>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};
