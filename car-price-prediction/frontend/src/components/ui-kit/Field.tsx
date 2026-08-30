import type { ReactNode } from "react";

export function Field({
  label,
  hint,
  children,
  className = "",
}: {
  label: string;
  hint?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={className}>
      <div className="mb-2 flex items-baseline justify-between gap-3">
        <label className="font-accent text-sm font-medium">{label}</label>
        {hint ? <span className="font-accent text-xs text-muted-foreground">{hint}</span> : null}
      </div>
      {children}
    </div>
  );
}

export const inputClass =
  "w-full rounded-[10px] border border-input bg-card px-3.5 py-2.5 font-accent text-sm outline-none transition-all duration-200 focus:border-primary focus:ring-4 focus:ring-primary/15";

export function RangeInput({
  value,
  min,
  max,
  step = 1,
  onChange,
}: {
  value: number;
  min: number;
  max: number;
  step?: number;
  onChange: (v: number) => void;
}) {
  const pct = ((value - min) / (max - min)) * 100;
  return (
    <input
      type="range"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      className="h-1.5 w-full cursor-pointer appearance-none rounded-full outline-none [&::-webkit-slider-thumb]:size-4 [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary [&::-webkit-slider-thumb]:shadow-[0_2px_8px_oklch(0_0_0/0.2)] [&::-moz-range-thumb]:size-4 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-primary"
      style={{
        background: `linear-gradient(to right, var(--primary) ${pct}%, var(--border) ${pct}%)`,
      }}
    />
  );
}

export function ChipGroup<T extends string>({
  options,
  value,
  onChange,
}: {
  options: readonly T[];
  value: T;
  onChange: (v: T) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((option) => (
        <button
          key={option}
          type="button"
          onClick={() => onChange(option)}
          className={`rounded-lg border px-3.5 py-2 font-accent text-sm transition-all duration-200 ${
            value === option
              ? "border-primary bg-primary/15 text-foreground shadow-[var(--shadow-soft)]"
              : "border-border bg-card text-muted-foreground hover:border-primary/50"
          }`}
        >
          {option}
        </button>
      ))}
    </div>
  );
}
