import React from 'react';
import { AlertTriangle, CheckCircle, ShieldAlert, Activity } from 'lucide-react';

const RiskProfile = ({ data }) => {
  if (!data) return null;

  const { decision_engine, malicious_score, risk_profile } = data;
  
  const getStatusStyles = (code) => {
    if (code === 'BLOCK') return { color: 'text-red-400 bg-red-900/20 border-red-800', icon: <AlertTriangle size={16} /> };
    if (code === 'WARN') return { color: 'text-yellow-400 bg-yellow-900/20 border-yellow-800', icon: <Activity size={16} /> };
    return { color: 'text-green-400 bg-green-900/20 border-green-800', icon: <CheckCircle size={16} /> };
  };

  const style = getStatusStyles(decision_engine.action_code);

  return (
    <div className="p-6 bg-[#1e293b] rounded-2xl border border-slate-800 shadow-2xl space-y-6">
      {/* Header with Dynamic Icon */}
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-black uppercase tracking-widest text-slate-400">Intelligence Report</h2>
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-[10px] font-bold border ${style.color}`}>
          {style.icon}
          {decision_engine.decision}
        </div>
      </div>

      {/* Malicious Meter */}
      <div>
        <div className="flex justify-between mb-2 items-end">
          <p className="text-xs text-slate-500 font-bold uppercase">Malicious Probability</p>
          <p className="text-xl font-mono font-bold text-red-500">{(malicious_score * 100).toFixed(1)}%</p>
        </div>
        <div className="w-full bg-slate-900 rounded-full h-3 border border-slate-800 p-0.5">
          <div 
            className="bg-gradient-to-r from-orange-600 to-red-600 h-full rounded-full transition-all duration-1000 shadow-[0_0_10px_rgba(220,38,38,0.3)]" 
            style={{ width: `${Math.min(malicious_score * 100, 100).toFixed(1)}%` }}
          ></div>
        </div>
      </div>

      {/* Intent Breakdown */}
      <div className="grid grid-cols-2 gap-3">
        {Object.entries(risk_profile).map(([key, value]) => (
          <div key={key} className="p-3 bg-slate-900/50 rounded-xl border border-slate-800/50">
            <p className="text-[10px] text-slate-500 uppercase font-black mb-1">{key.replace('_Intent', '')}</p>
            <p className="text-md font-mono text-slate-300">{(value * 100).toFixed(1)}%</p>
          </div>
        ))}
      </div>

      {/* Uncertainty Footer */}
      <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldAlert size={14} className="text-blue-500" />
          <p className="text-[11px] text-slate-400 uppercase tracking-tight">Uncertainty</p>
        </div>
        <span className="text-[11px] font-bold text-slate-200 bg-slate-800 px-2 py-0.5 rounded italic">
          {decision_engine.uncertainty_status}
        </span>
      </div>
    </div>
  );
};

export default RiskProfile;