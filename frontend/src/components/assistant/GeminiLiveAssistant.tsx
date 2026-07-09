"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Mic, X, Send, Sparkles } from "lucide-react";

export default function GeminiLiveAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [query, setQuery] = useState("");
  const [responses, setResponses] = useState<{role: 'user'|'ai', text: string}[]>([
    { role: 'ai', text: 'Hello. I am the NEXOVA Intelligence layer. How can I assist with stadium operations today?' }
  ]);

  const toggleAssistant = () => setIsOpen(!isOpen);
  const toggleListening = () => setIsListening(!isListening);

  const handleSend = () => {
    if (!query.trim()) return;
    
    setResponses(prev => [...prev, { role: 'user', text: query }]);
    setQuery("");
    
    // Simulate AI response for the UI prototype
    setTimeout(() => {
      setResponses(prev => [...prev, { 
        role: 'ai', 
        text: 'Analyzing real-time data... I have routed security to Gate B and updated the dynamic wayfinding screens to divert crowd flow to Gate A to reduce density.' 
      }]);
    }, 1500);
  };

  return (
    <>
      {/* Floating Action Button */}
      <motion.button
        className="fixed bottom-6 right-6 h-14 w-14 rounded-full bg-primary text-primary-foreground shadow-[0_0_30px_rgba(59,130,246,0.5)] flex items-center justify-center z-[5000] hover:scale-105 transition-transform"
        onClick={toggleAssistant}
        aria-label="Toggle AI Assistant"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Sparkles className="h-6 w-6" />
      </motion.button>

      {/* Assistant Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-24 right-6 w-[380px] h-[550px] bg-background/80 backdrop-blur-2xl border border-border rounded-2xl premium-shadow overflow-hidden flex flex-col z-[5000]"
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.3 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border/50 bg-secondary/50">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center">
                  <Sparkles className="h-4 w-4 text-primary" />
                </div>
                <span className="font-semibold text-sm tracking-wide uppercase">Nexova AI</span>
              </div>
              <button 
                onClick={toggleAssistant}
                className="h-8 w-8 rounded-full hover:bg-white/10 flex items-center justify-center transition-colors"
                aria-label="Close Assistant"
              >
                <X className="h-4 w-4 text-muted-foreground" />
              </button>
            </div>

            {/* Chat Area */}
            <div className="flex-1 p-4 overflow-y-auto space-y-4 flex flex-col">
              {responses.map((msg, idx) => (
                <div 
                  key={idx} 
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div 
                    className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                      msg.role === 'user' 
                        ? 'bg-primary text-primary-foreground rounded-tr-sm' 
                        : 'bg-secondary text-secondary-foreground rounded-tl-sm border border-border/50'
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
            </div>

            {/* Input Area */}
            <div className="p-4 bg-background border-t border-border">
              <div className="relative flex items-center">
                <button 
                  onClick={toggleListening}
                  className={`absolute left-2 h-8 w-8 rounded-full flex items-center justify-center transition-all ${
                    isListening ? 'bg-red-500/20 text-red-500 animate-pulse' : 'hover:bg-secondary text-muted-foreground'
                  }`}
                  aria-label="Toggle Voice Input"
                >
                  <Mic className="h-4 w-4" />
                </button>
                
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                  placeholder={isListening ? "Listening..." : "Ask NEXOVA..."}
                  className="w-full bg-secondary/50 border border-border rounded-full py-3 pl-12 pr-12 text-sm focus:outline-none focus:ring-1 focus:ring-primary/50 transition-all placeholder:text-muted-foreground/50"
                  aria-label="Query input"
                />

                <button 
                  onClick={handleSend}
                  disabled={!query.trim()}
                  className="absolute right-2 h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center disabled:opacity-50 disabled:bg-secondary disabled:text-muted-foreground transition-all"
                  aria-label="Send query"
                >
                  <Send className="h-3 w-3" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
