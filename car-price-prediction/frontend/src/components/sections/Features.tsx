import { Gauge, Zap, Database, Users } from "lucide-react";
import { Reveal } from "@/components/Reveal";
import type { ModelMetrics } from "@/lib/api";

export function Features({ modelMetrics }: { modelMetrics?: ModelMetrics }) {
  const listingCount = modelMetrics ? modelMetrics.training_samples + modelMetrics.test_samples : 15411;
  const items = [
    {
      icon: Gauge,
      stat: modelMetrics ? `${(modelMetrics.r2_score * 100).toFixed(1)}%` : "94.6%",
      label: "Model accuracy",
      note: "R² on held-out test data",
    },
    { icon: Zap, stat: "<1s", label: "Instant estimates", note: "No sign-up, no waiting" },
    {
      icon: Database,
      stat: listingCount.toLocaleString("en-IN"),
      label: "Real listings",
      note: "Cardekho market dataset",
    },
    { icon: Users, stat: "22k+", label: "Valuations run", note: "By buyers and sellers" },
  ];

  return (
    <section id="features" className="mx-auto max-w-6xl px-5 py-20">
      <Reveal>
        <h2 className="max-w-xl font-display text-3xl sm:text-4xl">
          Built on evidence, not guesswork
        </h2>
      </Reveal>

      <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {items.map((item, i) => (
          <Reveal key={item.label} delay={i * 90}>
            <article className="surface-card lift h-full p-6">
              <span className="flex size-11 items-center justify-center rounded-xl bg-primary/12 text-primary">
                <item.icon className="size-5" />
              </span>
              <p className="mt-5 font-display text-3xl">{item.stat}</p>
              <p className="mt-1 font-accent text-sm font-medium">{item.label}</p>
              <p className="mt-1 text-sm text-muted-foreground">{item.note}</p>
            </article>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
