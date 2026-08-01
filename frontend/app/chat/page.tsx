"use client";

import React, { useEffect, useState, useRef, Suspense } from "react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import ChatBubble from "@/components/ChatBubble";
import Loader from "@/components/Loader";
import { 
  Send, 
  Plus, 
  Paperclip, 
  Mic, 
  Trash2, 
  Stethoscope, 
  Sparkles, 
  History,
  MessageSquare,
  Home,
  UserCheck
} from "lucide-react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";

function ChatContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const activeIdParam = searchParams.get("id");

  const [conversationId, setConversationId] = useState<number | null>(
    activeIdParam ? Number(activeIdParam) : null
  );
  const [messages, setMessages] = useState<any[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Load chat history & active conversation
  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    async function loadHistory() {
      try {
        const histData = await api.getChatHistory();
        setHistory(histData || []);

        if (activeIdParam) {
          const selectedConv = histData.find((c: any) => c.id === Number(activeIdParam));
          if (selectedConv) {
            setConversationId(selectedConv.id);
            setMessages(selectedConv.messages || []);
          }
        }
      } catch (err) {
        console.error("Failed to load chat history:", err);
      } finally {
        setInitialLoading(false);
      }
    }
    loadHistory();
  }, [activeIdParam, router]);

  const handleNewChat = () => {
    setConversationId(null);
    setMessages([]);
    router.push("/chat");
  };

  const handleSelectChat = (conv: any) => {
    setConversationId(conv.id);
    setMessages(conv.messages || []);
    router.push(`/chat?id=${conv.id}`);
  };

  const handleDeleteChat = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    try {
      await api.deleteConversation(id);
      setHistory(history.filter((c) => c.id !== id));
      if (conversationId === id) {
        handleNewChat();
      }
    } catch (err) {
      console.error("Delete conversation failed:", err);
    }
  };

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userText = inputMessage;
    setInputMessage("");

    // Optimistic UI append
    const tempUserMsg = {
      id: Date.now(),
      role: "user",
      content: userText,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, tempUserMsg]);
    setLoading(true);

    try {
      const res = await api.sendMessage(userText, conversationId || undefined);
      setConversationId(res.conversation_id);

      const assistantMsg = {
        id: Date.now() + 1,
        role: "assistant",
        content: res.reply,
        analysis: res.analysis,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMsg]);

      // Refresh sidebar history list
      const updatedHistory = await api.getChatHistory();
      setHistory(updatedHistory || []);
    } catch (err: any) {
      const errorMsg = {
        id: Date.now() + 2,
        role: "assistant",
        content: `Error: ${err.message || "Could not process consultation. Please try again."}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) {
    return (
      <div className="min-h-screen bg-[#0b1329] flex items-center justify-center">
        <Loader label="Connecting to HealthAI Clinical Triage Engine..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0b1329] flex">
      <Sidebar />

      {/* Main Consultation Layout */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        
        {/* Top Header Bar */}
        <header className="glass-panel border-b border-slate-800 p-4 sm:px-8 flex items-center justify-between z-20">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center">
              <Stethoscope className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <h1 className="font-extrabold text-white text-base flex items-center gap-2">
                HealthAI Consultation
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              </h1>
              <p className="text-[11px] text-slate-400">
                Context-Aware Triage Engine (Health Profile Injected)
              </p>
            </div>
          </div>

          <button
            onClick={handleNewChat}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-cyan-500/20 border border-cyan-500/40 text-cyan-300 font-bold text-xs hover:bg-cyan-500 hover:text-slate-950 transition-all"
          >
            <Plus className="w-4 h-4" />
            New Consultation
          </button>
        </header>

        {/* Middle Container: Left History Drawer & Right Chat Stream */}
        <div className="flex-1 flex overflow-hidden">
          
          {/* History Sidebar */}
          <div className="w-72 glass-panel border-r border-slate-800/80 p-4 hidden md:flex flex-col justify-between overflow-y-auto">
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                <span className="flex items-center gap-1.5">
                  <History className="w-4 h-4" />
                  Past Sessions
                </span>
                <span className="text-cyan-400">{history.length}</span>
              </div>

              {history.length > 0 ? (
                history.map((conv) => {
                  const isSelected = conversationId === conv.id;
                  return (
                    <div
                      key={conv.id}
                      onClick={() => handleSelectChat(conv)}
                      className={`p-3 rounded-2xl cursor-pointer border text-xs transition-all flex items-center justify-between group ${
                        isSelected
                          ? "bg-cyan-950/50 border-cyan-500/40 text-cyan-200 font-bold"
                          : "bg-slate-900/60 border-slate-800 text-slate-300 hover:border-slate-700"
                      }`}
                    >
                      <div className="truncate pr-2">
                        <p className="truncate">{conv.title}</p>
                        <span className="text-[10px] text-slate-500 block">
                          {new Date(conv.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <button
                        onClick={(e) => handleDeleteChat(e, conv.id)}
                        className="opacity-0 group-hover:opacity-100 p-1 text-slate-500 hover:text-rose-400 transition-opacity"
                        title="Delete"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  );
                })
              ) : (
                <p className="text-xs text-slate-500 italic p-2">
                  No saved consultations.
                </p>
              )}
            </div>
          </div>

          {/* Chat Stream Window */}
          <div className="flex-1 flex flex-col justify-between p-4 sm:p-6 overflow-y-auto relative">
            
            <div className="flex-1 overflow-y-auto space-y-6 pr-2">
              {messages.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center p-8 max-w-lg mx-auto space-y-4 my-auto">
                  <div className="w-16 h-16 rounded-3xl bg-cyan-500/10 border border-cyan-400/30 flex items-center justify-center">
                    <Sparkles className="w-8 h-8 text-cyan-400" />
                  </div>
                  <h2 className="text-xl font-extrabold text-white">
                    Describe your symptoms or questions
                  </h2>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    HealthAI automatically factors in your chronic conditions, allergies, current medications, and lifestyle goals.
                  </p>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-left w-full pt-4">
                    {[
                      "I have a fever, headache, and body aches",
                      "Feeling dizzy after workouts",
                      "How can I lower my stress level?",
                      "What diet helps with high blood pressure?"
                    ].map((sample, i) => (
                      <button
                        key={i}
                        onClick={() => {
                          setInputMessage(sample);
                        }}
                        className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-cyan-500/40 text-xs text-slate-300 text-left transition-all"
                      >
                        "{sample}"
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                messages.map((msg) => (
                  <ChatBubble
                    key={msg.id}
                    role={msg.role}
                    content={msg.content}
                    analysis={msg.analysis}
                    timestamp={msg.timestamp}
                  />
                ))
              )}

              {loading && (
                <div className="flex items-center gap-3 p-4 glass-panel rounded-3xl w-fit border border-cyan-500/30">
                  <Stethoscope className="w-5 h-5 text-cyan-400 animate-spin" />
                  <span className="text-xs font-semibold text-cyan-300 animate-pulse">
                    HealthAI is analyzing symptoms & matching clinical triage...
                  </span>
                </div>
              )}

              <div ref={chatEndRef} />
            </div>

            {/* Input Bar Container */}
            <form onSubmit={handleSendMessage} className="mt-4 pt-4 border-t border-slate-800/80">
              <div className="glass-panel p-2.5 rounded-3xl border border-slate-700/80 flex items-center gap-2 shadow-2xl">
                
                <button
                  type="button"
                  className="p-2.5 rounded-2xl text-slate-400 hover:text-cyan-400 hover:bg-slate-800 transition-all"
                  title="Attach Image / Document"
                >
                  <Paperclip className="w-5 h-5" />
                </button>

                <input
                  type="text"
                  placeholder="Describe your symptoms, duration, or health concern..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  className="flex-1 bg-transparent px-3 py-2 text-slate-100 placeholder-slate-500 text-sm focus:outline-none"
                />

                <button
                  type="button"
                  className="p-2.5 rounded-2xl text-slate-400 hover:text-teal-400 hover:bg-slate-800 transition-all hidden sm:flex"
                  title="Voice Input"
                >
                  <Mic className="w-5 h-5" />
                </button>

                <button
                  type="submit"
                  disabled={!inputMessage.trim() || loading}
                  className="p-3 rounded-2xl bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 font-bold hover:brightness-110 disabled:opacity-50 transition-all shadow-md shadow-cyan-500/20"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </form>

          </div>
        </div>

      </div>

      {/* Mobile Bottom Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 glass-panel border-t border-slate-800 py-3 px-6 flex items-center justify-around z-40 lg:hidden text-xs">
        <Link href="/dashboard" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <Home className="w-5 h-5" />
          <span>Home</span>
        </Link>
        <Link href="/chat" className="flex flex-col items-center text-cyan-400 font-bold">
          <MessageSquare className="w-5 h-5" />
          <span>Chat</span>
        </Link>
        <Link href="/history" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <History className="w-5 h-5" />
          <span>History</span>
        </Link>
        <Link href="/health-profile" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <UserCheck className="w-5 h-5" />
          <span>Health</span>
        </Link>
      </nav>
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#0b1329] flex items-center justify-center"><Loader label="Loading AI Chat..." /></div>}>
      <ChatContent />
    </Suspense>
  );
}
