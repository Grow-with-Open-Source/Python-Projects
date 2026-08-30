import { useEffect, useState } from "react";
import { Car, Github } from "lucide-react";

const LINKS = [
  { label: "Home", href: "#home" },
  { label: "Features", href: "#features" },
  { label: "Estimate", href: "#estimate" },
  { label: "Data Science", href: "#data-science" },
];

export function Navbar({ apiStatus, apiVersion }: { apiStatus: boolean | null; apiVersion?: string }) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-500 ${
        scrolled ? "bg-background/90 shadow-[var(--shadow-soft)] backdrop-blur-md" : "bg-transparent"
      }`}
    >
      <nav className="mx-auto flex h-[72px] max-w-6xl items-center justify-between px-5">
        <a href="#home" className="flex items-center gap-2.5">
          <span className="flex size-9 items-center justify-center rounded-xl bg-primary/15 text-primary">
            <Car className="size-5" />
          </span>
          <span className="font-display text-lg font-semibold tracking-tight">
            Car<span className="text-primary">Cast</span>
          </span>
        </a>

        <ul className="hidden items-center gap-8 md:flex">
          {LINKS.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="group relative font-accent text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
                <span className="absolute -bottom-1.5 left-0 h-px w-0 bg-primary transition-all duration-300 group-hover:w-full" />
              </a>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-3">
          <span
            className={`hidden rounded-full px-3 py-1 font-accent text-xs md:inline-flex ${
              apiStatus === null
                ? "bg-ring text-muted-foreground"
                : apiStatus
                  ? "bg-secondary text-primary"
                  : "bg-destructive/15 text-destructive"
            }`}
          >
            {apiStatus === null
              ? "Checking API..."
              : apiStatus
                ? `API ${apiVersion ?? ""}`.trim()
                : "Model unavailable"}
          </span>

          <a
            href="https://github.com/dhwanit10/Car-price-prediction-project"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-lg border border-border bg-card px-3.5 py-2 font-accent text-sm transition-colors hover:border-primary hover:text-primary"
          >
            <Github className="size-4" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </div>
      </nav>
    </header>
  );
}
