import { useState } from "react";
import { MessageCircle, X, ArrowUp } from "lucide-react";

const QUESTIONS = [
  "What factors affect car price?",
  "How accurate is the prediction?",
  "Tell me about the model",
];

export function FloatingWidgets() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        aria-label="Back to top"
        className="fixed bottom-6 left-6 z-40 flex size-11 items-center justify-center rounded-full border border-border bg-card text-muted-foreground shadow-[var(--shadow-soft)] transition-colors hover:border-primary hover:text-primary"
      >
        <ArrowUp className="size-4" />
      </button>

      {open ? (
        <div className="fixed bottom-24 right-6 z-50 w-[20rem] animate-rise surface-card overflow-hidden">
          <div className="hero-gradient flex items-center justify-between px-5 py-4 text-[oklch(0.96_0.01_80)]">
            <p className="font-display text-base">CarCast Assistant</p>
            <button type="button" onClick={() => setOpen(false)} aria-label="Close chat">
              <X className="size-4 opacity-75 transition-opacity hover:opacity-100" />
            </button>
          </div>
          <div className="p-5">
            <span className="rounded-full bg-primary/15 px-3 py-1 font-accent text-xs text-primary">
              Coming soon
            </span>
            <p className="mt-3 text-sm text-muted-foreground">
              Ask anything about pricing, features and how the model reasons. Conversations go live
              with the next release.
            </p>
            <ul className="mt-4 space-y-2">
              {QUESTIONS.map((question) => (
                <li key={question}>
                  <button
                    type="button"
                    disabled
                    className="w-full cursor-not-allowed rounded-lg border border-border bg-secondary/70 px-3.5 py-2.5 text-left font-accent text-xs text-muted-foreground"
                  >
                    {question}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : null}

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-label="Open assistant"
        className="cta-gradient fixed bottom-6 right-6 z-50 flex size-14 items-center justify-center rounded-full text-accent-foreground shadow-[var(--shadow-card)] transition-transform duration-300 hover:scale-105"
      >
        <MessageCircle className="size-5" />
      </button>
    </>
  );
}
