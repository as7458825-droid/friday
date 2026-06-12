import React, { useState, useEffect, useRef } from 'react';
import { Send, Mic, Settings, Activity, Cpu, Shield, Terminal, TrendingUp, Lock } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const FRIDAY_API = 'http://localhost:8000';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'friday', text: 'FRIDAY Ultra — Neural Interface initialized. How can I assist you, Master?' }
  ]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [status, setStatus] = useState('online');
  const [securityStatus, setSecurityStatus] = useState('System Secure');
  const [marketData, setMarketData] = useState('Fetching...');
  const [amplitude, setAmplitude] = useState(Array(8).fill(4));
  const scrollRef = useRef(null);

  useEffect(() => {
    const fetchFinance = async () => {
      try {
        const res = await fetch(`${FRIDAY_API}/finance/market`);
        const data = await res.json();
        setMarketData(data.result || 'Market data unavailable');
      } catch (e) {}
    };
    fetchFinance();
    const interval = setInterval(fetchFinance, 30000);
    return () => clearInterval(interval);
  }, []);

  const runSecurityScan = async () => {
    setSecurityStatus('Scanning Network...');
    try {
      const res = await fetch(`${FRIDAY_API}/security/scan`);
      const data = await res.json();
      setSecurityStatus('Scan Complete');
      setMessages(prev => [...prev, { role: 'friday', text: data.result }]);
    } catch (e) {
      setSecurityStatus('Scan Failed');
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    let interval;
    if (isSpeaking) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${FRIDAY_API}/amplitude`);
          const data = await res.json();
          const newAmps = Array(8).fill(0).map(() => Math.max(4, data.amplitude * 24 * Math.random()));
          setAmplitude(newAmps);
        } catch (e) {}
      }, 100);
    } else {
      setAmplitude(Array(8).fill(4));
    }
    return () => clearInterval(interval);
  }, [isSpeaking]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);

    try {
      const response = await fetch(`${FRIDAY_API}/command`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: userMsg }),
      });
      const data = await response.json();

      if (data.responses && data.responses.length > 0) {
        setIsSpeaking(true);
        data.responses.forEach((resp, index) => {
          setTimeout(() => {
            setMessages(prev => [...prev, { role: 'friday', text: resp }]);
            if (index === data.responses.length - 1) setIsSpeaking(false);
          }, index * 500);
        });
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'friday', text: 'Connection to Core lost. Please verify bridge_api.py is running.' }]);
    }
  };

  return (
    <div className="h-screen w-screen bg-friday-dark text-friday-blue flex flex-col font-sans overflow-hidden">
      {/* Background Holographic Elements */}
      <div className="fixed inset-0 pointer-events-none opacity-20">
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute -top-1/2 -left-1/4 w-[1000px] h-[1000px] border border-friday-blue rounded-full"
        />
        <motion.div 
          animate={{ rotate: -360 }}
          transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
          className="absolute -bottom-1/2 -right-1/4 w-[800px] h-[800px] border border-friday-blue rounded-full"
        />
      </div>

      {/* Header */}
      <header className="z-10 h-16 border-b border-friday-blue/20 bg-friday-dark/80 backdrop-blur-md flex items-center justify-between px-8">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-full border-2 border-friday-blue flex items-center justify-center">
            <div className="w-4 h-4 bg-friday-blue rounded-full animate-pulse" />
          </div>
          <h1 className="text-xl font-bold tracking-widest uppercase">Friday Ultra</h1>
        </div>
        <div className="flex items-center space-x-6 text-sm">
          <div className="flex items-center space-x-2">
            <Cpu size={16} />
            <span className="opacity-70">CPU: 24%</span>
          </div>
          <div className="flex items-center space-x-2">
            <Activity size={16} />
            <span className="opacity-70">Neural: Active</span>
          </div>
          <div className="flex items-center space-x-2 text-green-400">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-ping" />
            <span className="font-bold">SYSTEM ONLINE</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex overflow-hidden z-10">
        {/* Sidebar */}
        <aside className="w-72 border-r border-friday-blue/20 bg-friday-dark/40 flex flex-col p-6 space-y-8 overflow-y-auto">
          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-tighter opacity-50">Security Protocol</h3>
            <button 
              onClick={runSecurityScan}
              className="w-full flex items-center justify-between p-3 rounded bg-friday-blue/10 border border-friday-blue/20 hover:bg-friday-blue/20 transition-all"
            >
              <div className="flex items-center space-x-3">
                <Shield size={18} />
                <span className="text-sm">Network Scan</span>
              </div>
              <span className="text-[10px] opacity-50 uppercase">{securityStatus}</span>
            </button>
            <div className="flex items-center space-x-3 p-3 rounded border border-white/10 opacity-50">
              <Lock size={18} />
              <span className="text-sm">Java Vault: Active</span>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-tighter opacity-50">Financial Intel</h3>
            <div className="p-3 rounded bg-white/5 border border-white/10">
              <div className="flex items-center space-x-2 mb-2 text-friday-blue">
                <TrendingUp size={16} />
                <span className="text-xs font-bold">Market Summary</span>
              </div>
              <p className="text-[10px] leading-relaxed opacity-80">{marketData}</p>
            </div>
          </div>

          <div className="flex-1" />
          
          <div className="p-4 border border-friday-blue/20 rounded-lg bg-friday-blue/5">
            <p className="text-xs opacity-70 mb-2 uppercase tracking-widest font-bold">Voice Sync</p>
            <div className="flex items-end space-x-1 h-8">
              {amplitude.map((h, i) => (
                <motion.div
                  key={i}
                  animate={{ height: h }}
                  className="flex-1 bg-friday-blue rounded-t"
                />
              ))}
            </div>
          </div>
        </aside>

        {/* Chat Area */}
        <section className="flex-1 flex flex-col bg-friday-dark/20 relative">
          <div 
            ref={scrollRef}
            className="flex-1 overflow-y-auto p-8 space-y-6"
          >
            <AnimatePresence>
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] p-4 rounded-xl border ${
                    msg.role === 'user' 
                      ? 'bg-friday-blue/10 border-friday-blue/40 text-friday-blue shadow-[0_0_15px_rgba(0,210,255,0.1)]' 
                      : 'bg-white/5 border-white/10 text-white'
                  }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          {/* Input Box */}
          <div className="p-8">
            <div className="relative group">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Initialize command..."
                className="w-full bg-white/5 border border-friday-blue/30 rounded-full py-4 px-6 pl-14 focus:outline-none focus:border-friday-blue transition-all placeholder-friday-blue/30 text-white"
              />
              <Terminal className="absolute left-6 top-1/2 -translate-y-1/2 text-friday-blue/50" size={20} />
              <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center space-x-2">
                <button 
                  onClick={sendMessage}
                  className="p-2 hover:bg-friday-blue hover:text-friday-dark rounded-full transition-colors"
                >
                  <Send size={20} />
                </button>
                <button className="p-2 hover:bg-friday-blue hover:text-friday-dark rounded-full transition-colors">
                  <Mic size={20} />
                </button>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
