import { Car, Github, Linkedin, Database } from "lucide-react";

const STACK = ["React", "TypeScript", "Tailwind", "XGBoost", "FastAPI", "Recharts"];

export function Footer() {
  return (
    <footer className="hero-gradient mt-24 text-[oklch(0.95_0.01_80)]">
      <div className="mx-auto grid max-w-6xl gap-10 px-5 py-16 md:grid-cols-3">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="flex size-9 items-center justify-center rounded-xl bg-primary/25 text-primary">
              <Car className="size-5" />
            </span>
            <span className="font-display text-lg font-semibold">CarCast</span>
          </div>
          <p className="mt-4 max-w-xs text-sm opacity-70">
            An XGBoost valuation engine trained on 15,000+ Cardekho listings, wrapped in a calm,
            honest interface.
          </p>
        </div>

        <div>
          <h3 className="font-accent text-xs uppercase tracking-[0.2em] opacity-60">Developer</h3>
          <p className="mt-4 font-display text-xl">Dhwanit Patel</p>
          <p className="text-sm opacity-70">Data Scientist & Full-stack Engineer</p>
          <div className="mt-4 flex gap-3">
            <a
              href="https://github.com/dhwanit10/Car-price-prediction-project"
              target="_blank"
              rel="noreferrer"
              className="inline-flex size-9 items-center justify-center rounded-lg bg-[oklch(1_0_0/0.1)] transition-colors hover:bg-primary hover:text-[oklch(0.2_0.01_60)]"
              aria-label="GitHub"
            >
              <Github className="size-4" />
            </a>
            <a
              href="https://www.linkedin.com/in/dhwanit-patel-062000318"
              target="_blank"
              rel="noreferrer"
              className="inline-flex size-9 items-center justify-center rounded-lg bg-[oklch(1_0_0/0.1)] transition-colors hover:bg-primary hover:text-[oklch(0.2_0.01_60)]"
              aria-label="LinkedIn"
            >
              <Linkedin className="size-4" />
            </a>
            <a
              href="https://www.kaggle.com/datasets/dhwanit10/car-price-dataset"
              target="_blank"
              rel="noreferrer"
              className="inline-flex size-9 items-center justify-center rounded-lg bg-[oklch(1_0_0/0.1)] transition-colors hover:bg-primary hover:text-[oklch(0.2_0.01_60)]"
              aria-label="Dataset"
            >
              <Database className="size-4" />
            </a>
          </div>
        </div>

        <div>
          <h3 className="font-accent text-xs uppercase tracking-[0.2em] opacity-60">Built with</h3>
          <ul className="mt-4 flex flex-wrap gap-2">
            {STACK.map((item) => (
              <li
                key={item}
                className="rounded-lg bg-[oklch(1_0_0/0.08)] px-3 py-1.5 font-accent text-xs opacity-85"
              >
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="border-t border-[oklch(1_0_0/0.1)] py-6 text-center text-xs opacity-55">
        © {new Date().getFullYear()} CarCast · Estimates are indicative, not an offer to buy.
      </div>
    </footer>
  );
}
