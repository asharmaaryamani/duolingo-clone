"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { getUserId, setUserId } from "@/lib/session";

export default function OnboardingGate({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);
  const [needsName, setNeedsName] = useState(false);
  const [name, setName] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (getUserId()) {
      setReady(true);
    } else {
      setNeedsName(true);
    }
  }, []);

  async function handleStart() {
    const trimmed = name.trim();
    if (!trimmed) return;
    setSubmitting(true);
    try {
      const user = await api.createSession(trimmed);
      setUserId(user.username);
      setNeedsName(false);
      setReady(true);
    } catch {
      setSubmitting(false);
    }
  }

  if (ready) return <>{children}</>;

  if (!needsName) {
    // brief moment while we check localStorage
    return <div className="min-h-screen bg-white" />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6 bg-white">
      <div className="max-w-sm w-full text-center">
        <div className="text-6xl mb-4">🦉</div>
        <h1 className="text-2xl font-extrabold text-duoText mb-2">Welcome to Duo Clone!</h1>
        <p className="text-duoGrayDark font-semibold mb-6">
          What should we call you? This creates your own learner profile — your
          progress won&apos;t be shared with anyone else using this app.
        </p>
        <input
          autoFocus
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleStart()}
          placeholder="Your name"
          maxLength={30}
          className="w-full border-2 border-duoGray focus:border-duoBlue rounded-2xl px-5 py-4 text-lg font-semibold outline-none mb-4"
        />
        <button
          onClick={handleStart}
          disabled={submitting || !name.trim()}
          className="btn-duo btn-duo-green w-full"
        >
          {submitting ? "Starting…" : "Let's go"}
        </button>
      </div>
    </div>
  );
}
