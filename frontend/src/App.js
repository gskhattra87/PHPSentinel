import React, { useState } from 'react';
import axios from 'axios';
import Editor from '@monaco-editor/react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { 
  Upload, FileCode, ShieldCheck, RefreshCw, 
  BarChart3, Terminal, Activity, ShieldAlert, Download
} from 'lucide-react';

import RiskProfile from './components/RiskProfile';
import StatisticsTab from './components/StatisticsTab';

function App() {
  const [activeTab, setActiveTab] = useState("analysis");
  const [viewMode, setViewMode] = useState("original");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [code, setCode] = useState("// 1. Upload a PHP payload via the sidebar\n// 2. Click 'SCAN PAYLOAD'\n// 3. Review AI-generated semantic risk profile");
  const [results, setResults] = useState(null);
  const [editorRef, setEditorRef] = useState(null);

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      const reader = new FileReader();
      reader.onload = (e) => setCode(e.target.result);
      reader.readAsText(uploadedFile);
      setResults(null); 
    }
  };

  const applyHighlights = (evidence) => {
    if (!editorRef || !evidence || !window.monaco) return;
    const decorations = evidence.map(item => ({
      range: new window.monaco.Range(item.line, 1, item.line, 1),
      options: {
        isWholeLine: true,
        className: 'bg-red-900/40', 
        glyphMarginClassName: 'bg-red-500 rounded-full',
        hoverMessage: { value: `**Semantic Warning:** ${item.intent} behavior detected.` }
      }
    }));
    editorRef.deltaDecorations([], decorations);
  };

  const analyzeMalware = async () => {
    if (!file) return alert("Please upload a file first.");
    loading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/scan", formData);
      const scanResults = response.data.results;
      setResults(scanResults);
      if (scanResults.evidence) applyHighlights(scanResults.evidence);
    } catch (error) {
      console.error("Analysis failed", error);
      alert("Backend connection failed. Ensure FastAPI is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!results) return;
    const reportElement = document.getElementById('report-area');
    
    try {
      const canvas = await html2canvas(reportElement, { backgroundColor: '#0f172a', scale: 2 });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      
      pdf.setFontSize(20);
      pdf.setTextColor(37, 99, 235);
      pdf.text("PHPSentinel Intelligence Report", 15, 20);
      
      pdf.setFontSize(10);
      pdf.setTextColor(100);
      pdf.text(`Target File: ${file.name} | Date: ${new Date().toLocaleString()}`, 15, 28);
      
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', 0, 40, pdfWidth, pdfHeight);
      pdf.save(`Intelligence_Report_${file.name}.pdf`);
    } catch (err) {
      console.error("PDF Generation failed", err);
      alert("Failed to generate PDF report.");
    }
  };

  return (
    <div className="flex h-screen w-screen bg-[#020617] text-slate-300 font-sans overflow-hidden">
      
      {/* GLOBAL SIDEBAR LAYER: Outside of tab conditions so it stays permanently mounted */}
      <aside className="w-72 bg-[#0f172a] border-r border-slate-800 flex flex-col p-6 z-50 shrink-0">
        <div className="flex items-center gap-3 mb-12">
          <div className="bg-blue-600 p-2.5 rounded-xl shadow-lg shadow-blue-500/20">
            <ShieldCheck className="text-white" size={26} />
          </div>
          <div>
            <h1 className="text-xl font-black text-white tracking-tight uppercase">PHPSentinel</h1>
            <p className="text-[9px] text-blue-500 font-black tracking-widest uppercase">Research Alpha v1.0</p>
          </div>
        </div>

        <nav className="flex flex-col gap-2 flex-1">
          <button 
            onClick={() => setActiveTab("analysis")} 
            className={`flex items-center gap-3 px-4 py-3.5 rounded-xl text-sm font-bold transition-all ${activeTab === 'analysis' ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20 shadow-[0_0_15px_rgba(37,99,235,0.1)]' : 'text-slate-500 hover:bg-slate-800/50 hover:text-slate-300'}`}
          >
            <Terminal size={18} /> Threat Detection
          </button>
          <button 
            onClick={() => setActiveTab("stats")} 
            className={`flex items-center gap-3 px-4 py-3.5 rounded-xl text-sm font-bold transition-all ${activeTab === 'stats' ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20 shadow-[0_0_15px_rgba(37,99,235,0.1)]' : 'text-slate-500 hover:bg-slate-800/50 hover:text-slate-300'}`}
          >
            <BarChart3 size={18} /> Model Analytics
          </button>
          
          <div className="mt-8 pt-8 border-t border-slate-800/50">
            <p className="text-[10px] text-slate-600 font-black uppercase tracking-widest px-4 mb-4">Operations</p>
            
            <label className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-slate-200 cursor-pointer text-sm font-bold transition-all border border-dashed border-slate-700 rounded-xl hover:border-slate-500 mb-4 bg-slate-900/30">
              <Upload size={18} className="text-blue-500" />
              <span className="truncate">{file ? file.name : "Upload PHP File"}</span>
              <input type="file" className="hidden" onChange={handleFileUpload} accept=".php" />
            </label>

            <button 
              onClick={analyzeMalware} 
              disabled={loading || !file} 
              className="w-full flex items-center justify-center gap-2 py-3.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-black shadow-lg shadow-blue-900/20 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <RefreshCw className="animate-spin" size={18} /> : <Activity size={18} />}
              {loading ? "SCANNING..." : "SCAN PAYLOAD"}
            </button>
          </div>
        </nav>

        <div className="mt-auto bg-slate-900/50 p-4 rounded-2xl border border-slate-800/50">
          <div className="flex items-center gap-2 text-blue-400 mb-2 font-black text-[10px] uppercase tracking-widest">
             <ShieldAlert size={14} /> Intelligence Status
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed font-medium">
            Model: CodeBERT Backbone<br/>
            Engine: XAI Semantic Active<br/>
            Status: System Online
          </p>
        </div>
      </aside>

      {/* CORE CANVAS WORKSPACE LAYER */}
      <main className="flex-1 flex flex-col min-w-0 relative h-full overflow-hidden">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-blue-600/5 blur-[120px] pointer-events-none rounded-full"></div>
        
        <header className="h-20 flex items-center justify-between px-10 border-b border-slate-800/50 backdrop-blur-sm z-10 shrink-0">
          <div className="flex items-center gap-4">
            <h2 className="text-sm font-black text-slate-400 uppercase tracking-widest">
              {activeTab === 'analysis' ? 'Malware Semantic Analysis' : 'Model Performance Matrix'}
            </h2>
          </div>
          
          {results && activeTab === 'analysis' && (
            <button 
              onClick={downloadReport} 
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-blue-400 rounded-lg text-xs font-bold border border-slate-700 transition-all shadow-lg"
            >
              <Download size={14} /> Export PDF Report
            </button>
          )}
        </header>

        {/* COMPONENT VIEWS MATRIX */}
        <section className="flex-1 p-8 overflow-y-auto">
          {activeTab === "analysis" ? (
            <div className="grid grid-cols-12 gap-8 h-full max-w-[1600px] mx-auto w-full" id="report-area">
              
              <div className="col-span-12 xl:col-span-8 flex flex-col gap-4">
                <div className="bg-[#0f172a] rounded-[2rem] border border-slate-800 overflow-hidden flex flex-col shadow-2xl h-[75vh]">
                  <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/30">
                    <div className="flex items-center gap-4">
                      <div className="flex gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/40"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/40"></div>
                        <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/40"></div>
                      </div>
                      <div className="flex items-center gap-2 border-l border-slate-700 pl-4">
                        <FileCode size={16} className="text-slate-500" />
                        <span className="text-[11px] font-mono text-slate-400 uppercase font-bold tracking-widest">
                          {viewMode === 'original' ? 'raw_source.php' : 'deobfuscated_output.php'}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex bg-slate-950 rounded-lg p-1 border border-slate-800">
                      <button 
                        onClick={() => setViewMode("original")} 
                        className={`px-4 py-1.5 text-[10px] font-black rounded-md transition-all ${viewMode === 'original' ? 'bg-slate-800 text-blue-400 shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
                      >
                        RAW SOURCE
                      </button>
                      <button 
                        onClick={() => setViewMode("normalized")} 
                        className={`px-4 py-1.5 text-[10px] font-black rounded-md transition-all ${viewMode === 'normalized' ? 'bg-slate-800 text-blue-400 shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
                      >
                        DEOBFUSCATED
                      </button>
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <Editor
                      theme="vs-dark"
                      defaultLanguage="php"
                      value={results ? (viewMode === "original" ? results.original_code : results.normalized_code) : code}
                      onMount={(editor) => setEditorRef(editor)}
                      options={{ 
                        minimap: { enabled: false }, 
                        fontSize: 14, 
                        fontFamily: "'Fira Code', monospace",
                        padding: { top: 20 },
                        readOnly: true,
                        glyphMargin: true,
                        renderLineHighlight: 'all',
                        scrollbar: { vertical: 'visible', horizontal: 'visible' }
                      }}
                    />
                  </div>
                </div>
              </div>

              <div className="col-span-12 xl:col-span-4 h-full">
                {results ? (
                  <div className="animate-in fade-in slide-in-from-right duration-500">
                    <RiskProfile data={results} />
                  </div>
                ) : (
                  <div className="h-full border-2 border-dashed border-slate-800 rounded-[2rem] flex flex-col items-center justify-center p-12 text-center opacity-40">
                    <div className="w-24 h-24 bg-slate-900 rounded-full flex items-center justify-center mb-6 shadow-inner border border-slate-800">
                      <ShieldCheck size={48} className="text-slate-600" />
                    </div>
                    <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest">Inference Pending</h3>
                    <p className="text-xs text-slate-600 mt-3 max-w-[200px] leading-relaxed">
                      Load a PHP payload and initialize the scan to map semantic risk and behavioral intent.
                    </p>
                  </div>
                )}
              </div>

            </div>
          ) : (
            <StatisticsTab />
          )}
        </section>
      </main>
    </div>
  );
}

export default App;