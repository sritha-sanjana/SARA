import React, { useState } from 'react';
import type { ConsensusResult, AgentCritique } from '../types/sara';
import { Scale, CheckCircle2, XCircle, AlertCircle, MessageSquare, ChevronDown, ChevronUp, Layers } from 'lucide-react';

interface ConsensusDebateViewProps {
  consensus: ConsensusResult;
  debate: AgentCritique[];
}

export const ConsensusDebateView: React.FC<ConsensusDebateViewProps> = ({
  consensus,
  debate,
}) => {
  // Track open state for each critique index. Default all collapsed.
  const [openAccordions, setOpenAccordions] = useState<Record<number, boolean>>({});

  const toggleAccordion = (idx: number) => {
    setOpenAccordions((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const allExpanded = debate.length > 0 && debate.every((_, idx) => openAccordions[idx]);

  const toggleAll = () => {
    if (allExpanded) {
      setOpenAccordions({});
    } else {
      const expandedState: Record<number, boolean> = {};
      debate.forEach((_, idx) => {
        expandedState[idx] = true;
      });
      setOpenAccordions(expandedState);
    }
  };

  const getBadgeStyle = (agent: string) => {
    switch (agent.toUpperCase()) {
      case 'AURA':
        return 'badge-aura';
      case 'NEXA':
        return 'badge-nexa';
      case 'LYRA':
        return 'badge-lyra';
      case 'ITHRA':
        return 'badge-ithra';
      default:
        return '';
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Lightweight Metrics Row */}
      <div className="metrics-grid-4">
        <div className="metric-widget-card">
          <div className="metric-widget-header">
            <span>Consensus Score</span>
            <Scale size={16} style={{ color: '#3b82f6' }} aria-hidden="true" />
          </div>
          <div className="metric-widget-value" style={{ color: '#3b82f6' }}>
            {consensus.consensus_score.toFixed(0)}%
          </div>
          <div className="progress-bar-track">
            <div
              className="progress-bar-fill"
              style={{ width: `${Math.min(100, Math.max(0, consensus.consensus_score))}%`, background: '#3b82f6' }}
            />
          </div>
        </div>

        <div className="metric-widget-card">
          <div className="metric-widget-header">
            <span>Agreement Score</span>
            <CheckCircle2 size={16} style={{ color: '#34d399' }} aria-hidden="true" />
          </div>
          <div className="metric-widget-value" style={{ color: '#34d399' }}>
            {consensus.agreement_score.toFixed(0)}%
          </div>
          <div className="progress-bar-track">
            <div
              className="progress-bar-fill"
              style={{ width: `${Math.min(100, Math.max(0, consensus.agreement_score))}%`, background: '#34d399' }}
            />
          </div>
        </div>

        <div className="metric-widget-card">
          <div className="metric-widget-header">
            <span>System Confidence</span>
            <Layers size={16} style={{ color: '#6366f1' }} aria-hidden="true" />
          </div>
          <div className="metric-widget-value" style={{ color: '#6366f1' }}>
            {consensus.confidence_score.toFixed(0)}%
          </div>
          <div className="progress-bar-track">
            <div
              className="progress-bar-fill"
              style={{ width: `${Math.min(100, Math.max(0, consensus.confidence_score))}%`, background: '#6366f1' }}
            />
          </div>
        </div>

        <div className="metric-widget-card">
          <div className="metric-widget-header">
            <span>Consensus Status</span>
            {consensus.consensus_reached ? (
              <CheckCircle2 size={16} style={{ color: '#10b981' }} aria-hidden="true" />
            ) : (
              <XCircle size={16} style={{ color: '#f59e0b' }} aria-hidden="true" />
            )}
          </div>
          <div className="metric-widget-value" style={{ fontSize: '1.2rem', color: consensus.consensus_reached ? '#10b981' : '#f59e0b' }}>
            {consensus.consensus_reached ? 'Reached' : 'Divergent'}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
            Evaluation Round {consensus.round_number}
          </span>
        </div>
      </div>

      {/* Dominant Hypothesis & Unresolved Disagreements */}
      <div className="section-grid-2">
        <div className="sub-card">
          <div className="sub-card-title">
            <Scale size={18} style={{ color: '#6366f1' }} aria-hidden="true" />
            <span>Dominant Hypothesis Convergence</span>
          </div>
          <div
            style={{
              fontSize: '1.05rem',
              fontWeight: 700,
              color: '#ffffff',
              background: 'var(--bg-card)',
              padding: '1rem',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-color)',
            }}
          >
            {consensus.dominant_hypothesis || 'No single hypothesis dominated.'}
          </div>
        </div>

        <div className="sub-card">
          <div className="sub-card-title">
            <AlertCircle size={18} style={{ color: '#f59e0b' }} aria-hidden="true" />
            <span>Unresolved Debate Disagreements</span>
          </div>
          {consensus.unresolved_disagreements.length > 0 ? (
            <ul className="clinical-bullet-list">
              {consensus.unresolved_disagreements.map((item, idx) => (
                <li key={idx} className="clinical-bullet-item">
                  <AlertCircle size={14} style={{ color: '#f59e0b', flexShrink: 0, marginTop: '3px' }} aria-hidden="true" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          ) : (
            <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
              No critical unresolved disagreements noted across agents.
            </div>
          )}
        </div>
      </div>

      {/* Debate Critiques Header & Toggle */}
      <div className="sub-card">
        <div className="debate-controls-bar">
          <div className="sub-card-title" style={{ marginBottom: 0, paddingBottom: 0, borderBottom: 'none' }}>
            <MessageSquare size={18} style={{ color: '#c084fc' }} aria-hidden="true" />
            <span>Multi-Agent Debate Critiques ({debate.length})</span>
          </div>
          <button
            type="button"
            className="btn-secondary"
            onClick={toggleAll}
            style={{ padding: '0.4rem 0.85rem', fontSize: '0.8rem' }}
          >
            {allExpanded ? 'Collapse All' : 'Expand All'}
          </button>
        </div>

        {/* Collapsible Debate Cards */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          {debate.map((critiqueItem, idx) => {
            const isOpen = !!openAccordions[idx];
            const badgeClass = getBadgeStyle(critiqueItem.target_agent);

            return (
              <div key={idx} className="debate-accordion-card">
                {/* Header Row */}
                <div className="debate-accordion-header" onClick={() => toggleAccordion(idx)}>
                  <div className="debate-header-left">
                    <span className={`agent-badge-pill ${badgeClass}`}>
                      {critiqueItem.target_agent} Critique
                    </span>
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                      Critique Confidence: <strong>{critiqueItem.confidence}%</strong>
                    </span>
                  </div>
                  <div className="debate-header-right">
                    {!isOpen && (
                      <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        "{critiqueItem.critique}"
                      </span>
                    )}
                    {isOpen ? (
                      <ChevronUp size={18} style={{ color: 'var(--text-muted)' }} aria-hidden="true" />
                    ) : (
                      <ChevronDown size={18} style={{ color: 'var(--text-muted)' }} aria-hidden="true" />
                    )}
                  </div>
                </div>

                {/* Expanded Accordion Body */}
                {isOpen && (
                  <div className="debate-accordion-body">
                    <div className="critique-quote-box">
                      "{critiqueItem.critique}"
                    </div>

                    <div className="section-grid-2" style={{ gap: '0.85rem' }}>
                      {critiqueItem.agrees.length > 0 && (
                        <div>
                          <span style={{ fontSize: '0.775rem', color: '#34d399', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                            Points of Agreement
                          </span>
                          <ul className="clinical-bullet-list" style={{ marginTop: '0.4rem' }}>
                            {critiqueItem.agrees.map((item, i) => (
                              <li key={i} className="clinical-bullet-item" style={{ fontSize: '0.85rem' }}>
                                <CheckCircle2 size={13} style={{ color: '#34d399', flexShrink: 0, marginTop: '3px' }} aria-hidden="true" />
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {critiqueItem.disagreements.length > 0 && (
                        <div>
                          <span style={{ fontSize: '0.775rem', color: '#f87171', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                            Points of Disagreement
                          </span>
                          <ul className="clinical-bullet-list" style={{ marginTop: '0.4rem' }}>
                            {critiqueItem.disagreements.map((item, i) => (
                              <li key={i} className="clinical-bullet-item" style={{ fontSize: '0.85rem' }}>
                                <XCircle size={13} style={{ color: '#f87171', flexShrink: 0, marginTop: '3px' }} aria-hidden="true" />
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>

                    {critiqueItem.new_insights && critiqueItem.new_insights.length > 0 && (
                      <div style={{ marginTop: '0.5rem' }}>
                        <span style={{ fontSize: '0.775rem', color: '#60a5fa', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                          New Insights Introduced
                        </span>
                        <ul className="clinical-bullet-list" style={{ marginTop: '0.4rem' }}>
                          {critiqueItem.new_insights.map((insight, i) => (
                            <li key={i} className="clinical-bullet-item" style={{ fontSize: '0.85rem' }}>
                              <Layers size={13} style={{ color: '#60a5fa', flexShrink: 0, marginTop: '3px' }} aria-hidden="true" />
                              <span>{insight}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {critiqueItem.revised_conclusion && (
                      <div style={{ marginTop: '0.5rem', paddingTop: '0.65rem', borderTop: '1px solid var(--border-color)', fontSize: '0.875rem', color: '#cbd5e1' }}>
                        <strong style={{ color: '#ffffff' }}>Revised Conclusion:</strong> {critiqueItem.revised_conclusion}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
