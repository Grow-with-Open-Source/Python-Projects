import { ArrowRight, Sparkles } from "lucide-react";
import heroCar from "@/assets/hero-car.png";

export function Hero({ modelName, r2Score }: { modelName?: string; r2Score?: number }) {
  const badgeModel = modelName ?? "XGBoost";
  const badgeR2 = (r2Score ?? 0.9459).toFixed(4);

  return (
    <section id="home" className="relative overflow-hidden pt-[72px]">
      <div className="pointer-events-none absolute -right-40 -top-32 size-[36rem] rounded-full bg-primary/12 blur-3xl" />
      <div className="pointer-events-none absolute -left-52 top-64 size-[30rem] rounded-full bg-accent/10 blur-3xl" />

      <div className="mx-auto grid min-h-[calc(100svh-72px)] max-w-6xl items-center gap-12 px-5 py-16 lg:grid-cols-[1.05fr_1fr]">
        <div className="animate-rise">
          <span className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3.5 py-1.5 font-accent text-xs tracking-wide text-primary">
            <Sparkles className="size-3.5" />
            {badgeModel} · R² {badgeR2}
          </span>

          <h1 className="mt-6 font-display text-5xl leading-[1.05] sm:text-6xl lg:text-7xl">
            Know your car's
            <span className="block gold-gradient-text">true worth.</span>
          </h1>

          <p className="mt-6 max-w-lg text-lg leading-relaxed text-muted-foreground">
            An honest, AI-powered valuation for any used car in India — trained on real Cardekho
            transactions and delivered in under a second.
          </p>

          <div className="mt-9 flex flex-wrap items-center gap-4">
            <a
              href="#estimate"
              className="cta-gradient group inline-flex items-center gap-2 rounded-lg px-6 py-3.5 font-accent text-sm font-medium text-accent-foreground shadow-[var(--shadow-soft)] transition-all duration-300 hover:shadow-[var(--shadow-lift)]"
            >
              Get your estimate
              <ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-1" />
            </a>
            <a
              href="#data-science"
              className="font-accent text-sm text-muted-foreground underline-offset-4 transition-colors hover:text-foreground hover:underline"
            >
              See the data science →
            </a>
          </div>
        </div>

        <div className="relative">
          <div className="absolute inset-x-8 bottom-6 h-8 rounded-[50%] bg-foreground/10 blur-2xl" />
          <img
            src={heroCar}
            alt="Premium used SUV valued by CarCast"
            width={1200}
            height={800}
            className="animate-float-car w-full drop-shadow-2xl"
          />
        </div>
      </div>
    </section>
  );
}
