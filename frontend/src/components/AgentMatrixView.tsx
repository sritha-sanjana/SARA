import React, { useState } from 'react';
import type { AgentAnalysis } from '../types/sara';
import { Brain, Stethoscope, Heart, Lightbulb, AlertCircle, HelpCircle, ChevronDown, ChevronUp, PlusCircle, MinusCircle } from 'lucide-react';

interface AgentMatrixViewProps {
  analyses: Record<string, AgentAnalysis>;
}

const AGENT_CONFIG: Record<
  string,
  { name: string; role: string; color: string; icon: React.ReactNode }
> = {
  AURA: {
    name: 'AURA',
    role: 'Analytical Understanding & Reasoning Agent',
    color: 'var(--agent-aura)',
    icon: <Brain size={20} style={{ color: 'var(--agent-aura)' }} aria-hidden="true" />,
  },
  NEXA: {
    name: 'NEXA',
    role: 'Neural & EXpert Analysis Agent (Clinical/Technical)',
    color: 'var(--agent-nexa)',
    icon: <Stethoscope size={20} style={{ color: 'var(--agent-nexa)' }} aria-hidden="true" />,
  },
  LYRA: {
    name: 'LYRA',
    role: 'Language & Patient-Centered Reasoning Agent',
    color: 'var(--agent-lyra)',
    icon: <Heart size={20} style={{ color: 'var(--agent-lyra)' }} aria-hidden="true" />,
  },
  ITHRA: {
    name: 'ITHRA',
    role: 'Intuitive & Thematic Hypothesis Reasoning Agent (Creative)',
    color: 'var(--agent-ithra)',
    icon: <Lightbulb size={20} style={{ color: 'var(--agent-ithra)' }} aria-hidden="true" />,
  },
};

export const AgentMatrixView: React.FC<AgentMatrixViewProps> = ({ analyses }) => {
  const agentKeys = ['AURA', 'NEXA', 'LYRA', 'ITHRA'];
  const [selectedAgent, setSelectedAgent] = useState<string>('ALL');

  // Track collapsible section open states per agent
  const [openSections, setOpenSections] = useState<Record<string, { missing?: boolean; anomalies?: boolean }>>({});

  const toggleSection = (agentKey: string, section: 'missing' | 'anomalies') => {
    setOpenSections((prev) => ({
      ...prev,
      [agentKey]: {
        ...prev[agentKey],
        [section]: !prev[agentKey]?.[section],
      },
    }));
  };

  const getLikelihoodClass = (likelihood: string) => {
    const l = likelihood.toLowerCase();
    if (l.includes('high')) return 'high';
    if (l.includes('mod')) return 'moderate';
    if (l.includes('low')) return 'low';
    return 'moderate';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Matrix Filter Buttons */}
      <div className="matrix-filter-bar">
        <button
          type="button"
          className={`btn-secondary ${selectedAgent === 'ALL' ? 'active' : ''}`}
          onClick={() => setSelectedAgent('ALL')}
          style={{
            borderColor: selectedAgent === 'ALL' ? 'var(--primary-blue)' : undefined,
            color: selectedAgent === 'ALL' ? '#ffffff' : undefined,
            background: selectedAgent === 'ALL' ? 'rgba(59, 130, 246, 0.15)' : undefined,
          }}
        >
          All 4 Agents Matrix
        </button>
        {agentKeys.map((key) => {
          const isSel = selectedAgent === key;
          return (
            <button
              key={key}
              type="button"
              className="btn-secondary"
              onClick={() => setSelectedAgent(key)}
              style={{
                borderColor: isSel ? AGENT_CONFIG[key].color : undefined,
                color: isSel ? '#ffffff' : undefined,
                background: isSel ? 'var(--bg-card-hover)' : undefined,
              }}
            >
              {key} Agent
            </button>
          );
        })}
      </div>

      {/* Persona Cards Grid */}
      <div className={selectedAgent === 'ALL' ? 'agent-matrix-grid' : 'single-agent-view'}>
        {agentKeys
          .filter((key) => selectedAgent === 'ALL' || selectedAgent === key)
          .map((key) => {
            const analysis = analyses[key];
            const config = AGENT_CONFIG[key] || {
              name: key,
              role: 'Reasoning Agent',
              color: 'var(--primary-blue)',
              icon: <Brain size={20} aria-hidden="true" />,
            };

            if (!analysis) {
              return (
                <div key={key} className="agent-persona-card">
                  <div className="agent-name-title">{key}</div>
                  <div style={{ color: 'var(--text-dim)' }}>No analysis data returned for agent.</div>
                </div>
              );
            }

            const isMissingOpen = !!openSections[key]?.missing;
            const isAnomaliesOpen = !!openSections[key]?.anomalies;

            return (
              <div key={key} className="agent-persona-card">
                {/* Agent Header Bar */}
                <div className="agent-card-top">
                  <div className="agent-identity">
                    <div className="agent-avatar-icon">{config.icon}</div>
                    <div>
                      <div className="agent-name-title" style={{ color: config.color }}>{config.name}</div>
                      <div className="agent-role-desc">{config.role}</div>
                    </div>
                  </div>
                  <div className="metric-ring-container" style={{ padding: '0.4rem 0.85rem', minWidth: 'auto' }}>
                    <span className="ring-score-val" style={{ fontSize: '1.2rem' }}>
                      {analysis.confidence}%
                    </span>
                    <span className="ring-score-label" style={{ fontSize: '0.65rem' }}>Confidence</span>
                  </div>
                </div>

                {/* Analytical Summary */}
                <div style={{ fontSize: '0.875rem', color: 'var(--text-main)', background: 'var(--bg-input)', padding: '0.85rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', lineHeight: 1.55 }}>
                  <strong style={{ color: '#ffffff' }}>Analytical Summary:</strong> {analysis.analytical_summary}
                </div>

                {/* Key Findings */}
                {analysis.key_findings.length > 0 && (
                  <div>
                    <span style={{ fontSize: '0.775rem', fontWeight: 800, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                      Key Findings
                    </span>
                    <ul className="clinical-bullet-list" style={{ marginTop: '0.4rem' }}>
                      {analysis.key_findings.map((finding, idx) => (
                        <li key={idx} className="clinical-bullet-item" style={{ fontSize: '0.85rem' }}>
                          <span style={{ color: config.color }}>•</span>
                          <span>{finding}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Hypotheses Structured Cards */}
                {analysis.hypotheses.length > 0 && (
                  <div>
                    <span style={{ fontSize: '0.775rem', fontWeight: 800, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                      Formulated Hypotheses ({analysis.hypotheses.length})
                    </span>
                    <div className="hypotheses-list-container" style={{ marginTop: '0.4rem' }}>
                      {analysis.hypotheses.map((hyp, idx) => (
                        <div key={idx} className="agent-hypothesis-box">
                          <div className="hypothesis-title-row">
                            <span className="hypothesis-name-text">{hyp.name}</span>
                            <span className={`likelihood-pill ${getLikelihoodClass(hyp.likelihood)}`}>
                              {hyp.likelihood}
                            </span>
                          </div>

                          <div className="evidence-tag-list">
                            {hyp.supporting_evidence.map((ev, i) => (
                              <div key={i} className="evidence-tag supporting">
                                <PlusCircle size={13} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
                                <span>Supporting: {ev}</span>
                              </div>
                            ))}
                            {hyp.contradicting_evidence.map((ev, i) => (
                              <div key={i} className="evidence-tag contradicting">
                                <MinusCircle size={13} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
                                <span>Contradicting: {ev}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Collapsible Missing Information */}
                {analysis.missing_information.length > 0 && (
                  <div>
                    <div className="collapsible-trigger" onClick={() => toggleSection(key, 'missing')}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-amber)' }}>
                        <HelpCircle size={14} aria-hidden="true" /> Missing Info ({analysis.missing_information.length})
                      </span>
                      {isMissingOpen ? <ChevronUp size={16} aria-hidden="true" /> : <ChevronDown size={16} aria-hidden="true" />}
                    </div>
                    {isMissingOpen && (
                      <ul className="clinical-bullet-list" style={{ marginTop: '0.5rem', padding: '0.5rem', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)' }}>
                        {analysis.missing_information.map((item, idx) => (
                          <li key={idx} className="clinical-bullet-item" style={{ fontSize: '0.825rem', color: '#fef08a' }}>
                            <span>• {item}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}

                {/* Collapsible Anomalies */}
                {analysis.anomalies.length > 0 && (
                  <div>
                    <div className="collapsible-trigger" onClick={() => toggleSection(key, 'anomalies')}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-rose)' }}>
                        <AlertCircle size={14} aria-hidden="true" /> Anomalies Identified ({analysis.anomalies.length})
                      </span>
                      {isAnomaliesOpen ? <ChevronUp size={16} aria-hidden="true" /> : <ChevronDown size={16} aria-hidden="true" />}
                    </div>
                    {isAnomaliesOpen && (
                      <ul className="clinical-bullet-list" style={{ marginTop: '0.5rem', padding: '0.5rem', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)' }}>
                        {analysis.anomalies.map((item, idx) => (
                          <li key={idx} className="clinical-bullet-item" style={{ fontSize: '0.825rem', color: '#fecdd3' }}>
                            <span>• {item}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            );
          })}
      </div>
    </div>
  );
};
