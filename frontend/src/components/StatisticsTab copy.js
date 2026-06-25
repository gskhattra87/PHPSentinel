import React from 'react';
import { BarChart3, Target, Zap, ShieldCheck, Info } from 'lucide-react';

const StatisticsTab = () => {
  // Quantitative Metrics (Extracted from your evaluate.py results)
// Quantitative Metrics (Extracted from your evaluate.py results)
  const metrics = [
    { label: "Model Accuracy", value: "89.70%", icon: <Target className="text-emerald-400" />, desc: "Overall classification precision" },
    { label: "Avg. Latency", value: "124ms", icon: <Zap className="text-amber-400" />, desc: "Time per 512-token sequence" },
    { label: "Calibration (ECE)", value: "0.012", icon: <ShieldCheck className="text-blue-400" />, desc: "Expected Calibration Error" },
    { label: "Dataset Size", value: "5,389", icon: <BarChart3 className="text-purple-400" />, desc: "Scrubbed PHP samples used" }
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom duration-700">
      
      {/* 1. KPI Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((m, i) => (
          <div key={i} className="bg-[#1e293b] p-6 rounded-[1.5rem] border border-slate-800 shadow-lg hover:border-slate-700 transition-all group">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-slate-900 rounded-xl group-hover:scale-110 transition-transform">{m.icon}</div>
              <span className="text-[10px] uppercase font-black text-slate-500 tracking-widest">{m.label}</span>
            </div>
            <p className="text-3xl font-mono font-bold text-white mb-1">{m.value}</p>
            <p className="text-[10px] text-slate-600 font-medium italic">{m.desc}</p>
          </div>
        ))}
      </div>

      {/* 2. Evaluation Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Confusion Matrix Card */}
        <div className="bg-[#1e293b] p-8 rounded-[2rem] border border-slate-800 shadow-2xl">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-white font-bold flex items-center gap-2 text-lg">
              <BarChart3 size={20} className="text-blue-500" /> Behavioral Mapping
            </h3>
            <span className="text-[10px] font-mono text-slate-500 bg-slate-900 px-2 py-1 rounded">FIG 4.1</span>
          </div>
          <div className="aspect-square bg-slate-950/50 rounded-2xl border border-slate-800/50 flex items-center justify-center p-4">
            <img 
              src="/thesis_confusion_matrix.png" 
              alt="Confusion Matrix" 
              className="max-h-full rounded-lg opacity-90 hover:opacity-100 transition-opacity cursor-zoom-in" 
              onError={(e) => e.target.src='https://placehold.co/600x600/1e293b/475569?text=Confusion+Matrix+Not+Found'}
            />
          </div>
          <p className="mt-4 text-xs text-slate-500 italic text-center">Correlation between ground-truth labels and CodeBERT-predicted intent.</p>
        </div>

        {/* Calibration Card */}
        <div className="bg-[#1e293b] p-8 rounded-[2rem] border border-slate-800 shadow-2xl">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-white font-bold flex items-center gap-2 text-lg">
              <ShieldCheck size={20} className="text-emerald-500" /> Reliability Diagram
            </h3>
            <span className="text-[10px] font-mono text-slate-500 bg-slate-900 px-2 py-1 rounded">FIG 4.2</span>
          </div>
          <div className="aspect-square bg-slate-950/50 rounded-2xl border border-slate-800/50 flex items-center justify-center p-4">
            <img 
              src="/thesis_reliability_diagram.png" 
              alt="Reliability Diagram" 
              className="max-h-full rounded-lg opacity-90 hover:opacity-100 transition-opacity cursor-zoom-in"
              onError={(e) => e.target.src='https://placehold.co/600x600/1e293b/475569?text=Calibration+Plot+Not+Found'}
            />
          </div>
          <p className="mt-4 text-xs text-slate-500 italic text-center">Probability calibration via Temperature Scaling for RQ2.</p>
        </div>
      </div>

      {/* 3. Research Appendix / Conclusion Summary */}
      <div className="p-8 bg-blue-600/5 rounded-[2rem] border border-blue-600/20 shadow-inner">
        <div className="flex items-center gap-2 mb-6">
          <Info size={16} className="text-blue-400" />
          <h4 className="text-blue-400 font-black uppercase tracking-widest text-xs">Project Significance & RQ Findings</h4>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div className="space-y-2">
            <h5 className="text-white font-bold text-sm">RQ1: Normalization Impact</h5>
            <p className="text-xs text-slate-500 leading-relaxed italic">
              "The custom deobfuscation layer successfully handled string-concatenation and base64-encoding patterns, 
              improving model focus on semantic bytecode."
            </p>
          </div>
          <div className="space-y-2 border-l border-slate-800 pl-8">
            <h5 className="text-white font-bold text-sm">RQ2: Confidence Calibration</h5>
            <p className="text-xs text-slate-500 leading-relaxed italic">
              "Expected Calibration Error was reduced significantly, ensuring that alerts presented in the 
              Threat Detection UI correlate to actual statistical risk."
            </p>
          </div>
          <div className="space-y-2 border-l border-slate-800 pl-8">
            <h5 className="text-white font-bold text-sm">RQ3: Behavioral Mapping</h5>
            <p className="text-xs text-slate-500 leading-relaxed italic">
              "CodeBERT's attention mechanism demonstrated high precision in distinguishing File Operations 
              from actual Exfiltration intent."
            </p>
          </div>
        </div>
      </div>

    </div>
  );
};

export default StatisticsTab;