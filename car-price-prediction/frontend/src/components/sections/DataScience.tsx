import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { BookOpen, Database, Github } from "lucide-react";
import { Reveal } from "@/components/Reveal";
import type { ModelInfoResponse } from "@/lib/api";
import { FEATURE_IMPORTANCE } from "@/lib/car-data";

const DEFAULT_DESCRIPTION =
  "Gradient-boosted trees over 15,411 listings, with target encoding for brand and model and log-transformed prices.";

const LINKS = [
  {
    icon: Github,
    label: "Training notebooks",
    href: "https://github.com/dhwanit10/Car-price-prediction-project/tree/main/backend/notebooks",
  },
  {
    icon: Database,
    label: "Cardekho dataset",
    href: "https://www.kaggle.com/datasets/dhwanit10/car-price-dataset",
  },
  {
    icon: BookOpen,
    label: "Model documentation",
    href: "https://github.com/dhwanit10/Car-price-prediction-project/tree/main/backend/notebooks",
  },
];

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export function DataScience({
  modelInfo,
  apiError,
}: {
  modelInfo?: ModelInfoResponse;
  apiError?: string | null;
}) {
  const metrics = modelInfo?.model_metrics;
  const metricCards = metrics
    ? [
        { label: "R² score", value: metrics.r2_score.toFixed(4), note: "Test set" },
        { label: "MAE", value: formatCurrency(metrics.mae), note: "Mean absolute error" },
        { label: "RMSE", value: formatCurrency(metrics.rmse), note: "Root mean squared error" },
        {
          label: "Model",
          value: metrics.model_name,
          note: `${metrics.features_count} features`,
        },
      ]
    : [
        { label: "R² score", value: "0.9459", note: "Test set" },
        { label: "MAE", value: "₹97,149", note: "Mean absolute error" },
        { label: "RMSE", value: "₹1,84,320", note: "Root mean squared error" },
        { label: "Model", value: "XGBoost", note: "400 estimators, depth 8" },
      ];

  return (
    <section id="data-science" className="border-y border-border bg-secondary/60 py-20">
      <div className="mx-auto max-w-6xl px-5">
        <Reveal>
          <h2 className="max-w-xl font-display text-3xl sm:text-4xl">The data science behind it</h2>
          <p className="mt-3 max-w-xl text-muted-foreground">
            {metrics?.description ?? DEFAULT_DESCRIPTION}
          </p>
          {apiError ? (
            <p className="mt-2 text-sm text-destructive">
              Live model metrics are unavailable: {apiError}
            </p>
          ) : null}
        </Reveal>

        <div className="mt-10 grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
          <Reveal>
            <div className="grid h-full gap-5 sm:grid-cols-2">
              {metricCards.map((metric) => (
                <div key={metric.label} className="surface-card lift p-6">
                  <p className="font-accent text-xs uppercase tracking-[0.18em] text-muted-foreground">
                    {metric.label}
                  </p>
                  <p className="mt-3 font-display text-2xl">{metric.value}</p>
                  <p className="mt-1 text-xs text-muted-foreground">{metric.note}</p>
                </div>
              ))}
            </div>
          </Reveal>

          <Reveal delay={110}>
            <div className="surface-card h-full p-6">
              <h3 className="font-display text-xl">Feature importance</h3>
              <div className="mt-4 h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={FEATURE_IMPORTANCE}
                    layout="vertical"
                    margin={{ left: 16, right: 16 }}
                  >
                    <CartesianGrid horizontal={false} stroke="var(--border)" />
                    <XAxis type="number" hide />
                    <YAxis
                      type="category"
                      dataKey="feature"
                      width={104}
                      tickLine={false}
                      axisLine={false}
                      tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                    />
                    <Tooltip
                      cursor={{ fill: "var(--muted)" }}
                      formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
                      contentStyle={{
                        borderRadius: 12,
                        border: "1px solid var(--border)",
                        fontSize: 12,
                      }}
                    />
                    <Bar dataKey="importance" fill="var(--gold)" radius={[0, 6, 6, 0]} barSize={14} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </Reveal>
        </div>

        <Reveal delay={80}>
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            {LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                target="_blank"
                rel="noreferrer"
                className="surface-card lift flex items-center gap-3 p-5 font-accent text-sm"
              >
                <span className="flex size-10 items-center justify-center rounded-xl bg-primary/12 text-primary">
                  <link.icon className="size-4" />
                </span>
                {link.label}
              </a>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
