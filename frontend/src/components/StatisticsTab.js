import React from 'react';
import { BarChart3, ShieldCheck, Cpu, Target } from 'lucide-react';

function StatisticsTab() {
  return (
    <div className="space-y-8 max-w-[1600px] mx-auto w-full p-2">
      
      {/* Top Level Metric Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-[#0f172a] border border-slate-800 p-6 rounded-2xl shadow-xl flex items-center gap-4">
          <div className="p-3 bg-blue-600/10 text-blue-400 rounded-xl border border-blue-500/20">
            <Target size={20} />
          </div>
          <div>
            <p className="text-[10px] uppercase tracking-widest font-black text-slate-500">Aggregate Accuracy</p>
            <h4 className="text-xl font-black text-white mt-0.5">99.36%</h4>
          </div>
        </div>

        <div className="bg-[#0f172a] border border-slate-800 p-6 rounded-2xl shadow-xl flex items-center gap-4">
          <div className="p-3 bg-emerald-600/10 text-emerald-400 rounded-xl border border-emerald-500/20">
            <ShieldCheck size={20} />
          </div>
          <div>
            <p className="text-[10px] uppercase tracking-widest font-black text-slate-500">Macro F1-Score</p>
            <h4 className="text-xl font-black text-white mt-0.5">0.943</h4>
          </div>
        </div>

        <div className="bg-[#0f172a] border border-slate-800 p-6 rounded-2xl shadow-xl flex items-center gap-4">
          <div className="p-3 bg-purple-600/10 text-purple-400 rounded-xl border border-purple-500/20">
            <Cpu size={20} />
          </div>
          <div>
            <p className="text-[10px] uppercase tracking-widest font-black text-slate-500">Inference Latency</p>
            <h4 className="text-xl font-black text-white mt-0.5">124 ms</h4>
          </div>
        </div>

        <div className="bg-[#0f172a] border border-slate-800 p-6 rounded-2xl shadow-xl flex items-center gap-4">
          <div className="p-3 bg-amber-600/10 text-amber-400 rounded-xl border border-amber-500/20">
            <BarChart3 size={20} />
          </div>
          <div>
            <p className="text-[10px] uppercase tracking-widest font-black text-slate-500">McNemar Chi-Squared</p>
            <h4 className="text-xl font-black text-white mt-0.5">131.79</h4>
          </div>
        </div>
      </div>

      {/* Main Dual Graph Display Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Confusion Matrix Container */}
        <div className="bg-[#0f172a] border border-slate-800 rounded-[2rem] p-6 flex flex-col shadow-2xl">
          <div className="flex items-center gap-2 mb-6 px-2">
            <div className="w-2 h-2 rounded-full bg-blue-500"></div>
            <h3 className="text-xs font-black uppercase tracking-widest text-slate-400">Confusion Matrix Evaluation</h3>
          </div>
          <div className="flex-1 bg-slate-950/40 rounded-2xl p-4 border border-slate-800/50 flex items-center justify-center min-h-[450px]">
            <img 
              src="/thesis_confusion_matrix.png" 
              alt="Thesis Confusion Matrix" 
              className="max-h-[420px] w-auto object-contain rounded-xl"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.parentNode.innerHTML = '<p class="text-xs text-slate-600 font-bold uppercase tracking-widest p-8 text-center">Asset Verification: Ensure thesis_confusion_matrix.png sits in frontend/public/</p>';
              }}
            />
          </div>
        </div>

        {/* Reliability Diagram Container */}
        <div className="bg-[#0f172a] border border-slate-800 rounded-[2rem] p-6 flex flex-col shadow-2xl">
          <div className="flex items-center gap-2 mb-6 px-2">
            <div className="w-2 h-2 rounded-full bg-purple-500"></div>
            <h3 className="text-xs font-black uppercase tracking-widest text-slate-400">Probability Reliability Diagram</h3>
          </div>
          <div className="flex-1 bg-slate-950/40 rounded-2xl p-4 border border-slate-800/50 flex items-center justify-center min-h-[450px]">
            <img 
              src="/thesis_reliability_diagram.png" 
              alt="Thesis Reliability Diagram" 
              className="max-h-[420px] w-auto object-contain rounded-xl"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.parentNode.innerHTML = '<p class="text-xs text-slate-600 font-bold uppercase tracking-widest p-8 text-center">Asset Verification: Ensure thesis_reliability_diagram.png sits in frontend/public/</p>';
              }}
            />
          </div>
        </div>

      </div>
    </div>
  );
}

export default StatisticsTab;