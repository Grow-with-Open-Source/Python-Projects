import { useEffect, useMemo, useState } from "react";
import { Loader2, RefreshCw, Sparkles, Minus, Plus, Trash2, Clock } from "lucide-react";
import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Reveal } from "@/components/Reveal";
import { Field, inputClass, RangeInput, ChipGroup } from "@/components/ui-kit/Field";
import { useCountUp } from "@/hooks/useReveal";
import {
  FUEL_TYPES,
  SAMPLE_CARS,
  SELLER_TYPES,
  formatINR,
  formatLakhs,
  type CarInput,
  type FuelType,
  type SellerType,
  type Transmission,
} from "@/lib/car-data";
import {
  fetchBrandModels,
  fetchBrands,
  predictCar,
  predictCarWithAsking,
  type PredictResponse,
  type PredictWithAskingResponse,
} from "@/lib/api";

const STORAGE_KEY = "CarCast.history";

const DEFAULT_CAR: CarInput = {
  brand: "Hyundai",
  model: "Creta",
  vehicle_age: 4,
  km_driven: 52000,
  fuel_type: "Petrol",
  transmission_type: "Manual",
  mileage: 18.5,
  engine: 1497,
  max_power: 113,
  seats: 5,
  seller_type: "Dealer",
};

type PredictionResult = {
  id: string;
  input: CarInput;
  predicted_price: number;
  predicted_price_lakhs: number;
  price_category: string;
  price_range: { low: number; high: number };
  confidence_score: number;
  timestamp: string;
  createdAt: number;
  asking_price?: number;
  price_difference?: number;
  deal_status?: string;
  deal_message?: string;
  savings?: number;
};

function toPredictionResult(
  input: CarInput,
  response: PredictResponse | PredictWithAskingResponse,
): PredictionResult {
  const parsedTime = Date.parse(response.timestamp);
  return {
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    input,
    predicted_price: response.predicted_price,
    predicted_price_lakhs: response.predicted_price_lakhs,
    price_category: response.price_category,
    price_range: response.price_range,
    confidence_score: response.confidence_score,
    timestamp: response.timestamp,
    createdAt: Number.isNaN(parsedTime) ? Date.now() : parsedTime,
    asking_price: "asking_price" in response ? response.asking_price : undefined,
    price_difference: "price_difference" in response ? response.price_difference : undefined,
    deal_status: "deal_status" in response ? response.deal_status : undefined,
    deal_message: "deal_message" in response ? response.deal_message : undefined,
    savings: "savings" in response ? response.savings : undefined,
  };
}

export function Predictor() {
  const [car, setCar] = useState<CarInput>(DEFAULT_CAR);
  const [brandOptions, setBrandOptions] = useState<string[]>([]);
  const [modelOptions, setModelOptions] = useState<string[]>([]);
  const [brandsLoading, setBrandsLoading] = useState(true);
  const [modelsLoading, setModelsLoading] = useState(false);
  const [brandsError, setBrandsError] = useState<string | null>(null);
  const [modelsError, setModelsError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [askingLoading, setAskingLoading] = useState(false);
  const [predictError, setPredictError] = useState<string | null>(null);
  const [askingError, setAskingError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [history, setHistory] = useState<PredictionResult[]>([]);
  const [asking, setAsking] = useState("");
  const [sampleIndex, setSampleIndex] = useState(0);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Array<
          PredictionResult & { confidence?: number; timestamp?: string; createdAt?: number }
        >;
        const normalized = parsed.map((entry) => {
          const fallbackTime = entry.timestamp ? Date.parse(entry.timestamp) : NaN;
          return {
            ...entry,
            confidence_score: entry.confidence_score ?? entry.confidence ?? 0,
            createdAt:
              entry.createdAt ??
              (Number.isNaN(fallbackTime) ? Date.now() : fallbackTime),
            predicted_price_lakhs:
              entry.predicted_price_lakhs ?? Number((entry.predicted_price / 100000).toFixed(2)),
          };
        });
        setHistory(normalized);
      }
    } catch {
      /* ignore corrupt storage */
    }
  }, []);

  useEffect(() => {
    let active = true;
    setBrandsLoading(true);

    const loadBrands = async () => {
      try {
        const brands = await fetchBrands();
        if (!active) return;

        setBrandOptions(brands);
        setBrandsError(null);
        setCar((prev) => {
          if (brands.includes(prev.brand)) return prev;
          return { ...prev, brand: brands[0] ?? "", model: "" };
        });
      } catch (error) {
        if (!active) return;

        setBrandsError(error instanceof Error ? error.message : "Failed to fetch brands.");
        setBrandOptions([]);
      } finally {
        if (active) setBrandsLoading(false);
      }
    };

    void loadBrands();

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    if (!car.brand) {
      setModelOptions([]);
      setModelsError(null);
      return () => {
        active = false;
      };
    }

    setModelsLoading(true);
    setModelsError(null);

    const selectedBrand = car.brand;
    const loadModels = async () => {
      try {
        const models = await fetchBrandModels(selectedBrand);
        if (!active) return;

        setModelOptions(models);
        setCar((prev) => {
          if (prev.brand !== selectedBrand) return prev;
          if (models.includes(prev.model)) return prev;
          return { ...prev, model: models[0] ?? "" };
        });
      } catch (error) {
        if (!active) return;

        setModelsError(error instanceof Error ? error.message : "Failed to fetch models.");
        setModelOptions([]);
        setCar((prev) => (prev.brand === selectedBrand ? { ...prev, model: "" } : prev));
      } finally {
        if (active) setModelsLoading(false);
      }
    };

    void loadModels();

    return () => {
      active = false;
    };
  }, [car.brand]);

  const persist = (next: PredictionResult[]) => {
    setHistory(next);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      /* storage unavailable */
    }
  };

  const pushHistory = (entry: PredictionResult) => {
    setHistory((prev) => {
      const next = [entry, ...prev].slice(0, 20);
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      } catch {
        /* storage unavailable */
      }
      return next;
    });
  };

  const set = <K extends keyof CarInput>(key: K, value: CarInput[K]) =>
    setCar((prev) => ({ ...prev, [key]: value }));

  const canSubmit = car.brand.length > 0 && car.model.length > 0 && !brandsLoading && !modelsLoading;

  const fillSample = () => {
    const sample = SAMPLE_CARS[sampleIndex % SAMPLE_CARS.length] ?? DEFAULT_CAR;
    setSampleIndex((i) => i + 1);
    setCar(sample);
  };

  const submit = async () => {
    setLoading(true);
    setPredictError(null);
    setAskingError(null);
    try {
      const response = await predictCar(car);
      const prediction = toPredictionResult(car, response);
      setResult(prediction);
      setAsking("");
      pushHistory(prediction);
      document.getElementById("result")?.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      setPredictError(error instanceof Error ? error.message : "Failed to predict car price.");
    } finally {
      setLoading(false);
    }
  };

  const analyzeAskingPrice = async () => {
    if (!result) return;

    const askingPrice = Number(asking.replace(/[^0-9.]/g, ""));
    if (!(askingPrice > 0)) {
      setAskingError("Please enter a valid asking price.");
      return;
    }

    setAskingLoading(true);
    setAskingError(null);
    try {
      const response = await predictCarWithAsking({
        ...result.input,
        asking_price: askingPrice,
      });
      const updated = toPredictionResult(result.input, response);
      setResult(updated);
      pushHistory(updated);
    } catch (error) {
      setAskingError(
        error instanceof Error ? error.message : "Failed to evaluate asking price.",
      );
    } finally {
      setAskingLoading(false);
    }
  };

  return (
    <>
      <section id="estimate" className="mx-auto max-w-6xl px-5 py-20">
        <Reveal>
          <div className="max-w-xl">
            <h2 className="font-display text-3xl sm:text-4xl">Tell us about the car</h2>
            <p className="mt-3 text-muted-foreground">
              Eleven inputs — the same features the model was trained on. Brand/model options and
              predictions are fetched from the FastAPI backend.
            </p>
          </div>
        </Reveal>

        <Reveal delay={80}>
          <div className="surface-card mt-9 p-6 sm:p-9">
            <div className="grid gap-x-8 gap-y-6 md:grid-cols-2">
              <Field label="Brand">
                <select
                  className={inputClass}
                  value={car.brand}
                  disabled={brandsLoading}
                  onChange={(e) => {
                    const brand = e.target.value;
                    setCar((prev) => ({
                      ...prev,
                      brand,
                      model: "",
                    }));
                  }}
                >
                  <option value="" disabled>
                    {brandsLoading ? "Loading brands..." : "Select brand"}
                  </option>
                  {brandOptions.map((brand) => (
                    <option key={brand} value={brand}>
                      {brand}
                    </option>
                  ))}
                </select>
                {brandsError ? (
                  <p className="mt-2 text-xs text-destructive">Unable to load brands: {brandsError}</p>
                ) : null}
              </Field>

              <Field label="Model">
                <select
                  className={inputClass}
                  value={car.model}
                  disabled={!car.brand || modelsLoading || modelOptions.length === 0}
                  onChange={(e) => set("model", e.target.value)}
                >
                  <option value="" disabled>
                    {!car.brand
                      ? "Select brand first"
                      : modelsLoading
                        ? "Loading models..."
                        : modelOptions.length === 0
                          ? "No models available"
                          : "Select model"}
                  </option>
                  {modelOptions.map((model) => (
                    <option key={model} value={model}>
                      {model}
                    </option>
                  ))}
                </select>
                {modelsError ? (
                  <p className="mt-2 text-xs text-destructive">Unable to load models: {modelsError}</p>
                ) : null}
              </Field>

              <Field
                label="Vehicle age"
                hint={car.vehicle_age === 0 ? "Brand new" : `${car.vehicle_age} years old`}
              >
                <div className="flex items-center gap-4">
                  <RangeInput
                    value={car.vehicle_age}
                    min={0}
                    max={30}
                    onChange={(v) => set("vehicle_age", v)}
                  />
                  <input
                    type="number"
                    min={0}
                    max={30}
                    value={car.vehicle_age}
                    onChange={(e) => set("vehicle_age", Number(e.target.value))}
                    className={`${inputClass} w-24`}
                  />
                </div>
              </Field>

              <Field label="Kilometres driven" hint={`${car.km_driven.toLocaleString("en-IN")} km`}>
                <div className="flex items-center gap-4">
                  <RangeInput
                    value={car.km_driven}
                    min={0}
                    max={300000}
                    step={1000}
                    onChange={(v) => set("km_driven", v)}
                  />
                  <input
                    type="number"
                    min={0}
                    value={car.km_driven}
                    onChange={(e) => set("km_driven", Number(e.target.value))}
                    className={`${inputClass} w-28`}
                  />
                </div>
              </Field>

              <Field label="Fuel type">
                <ChipGroup
                  options={FUEL_TYPES}
                  value={car.fuel_type}
                  onChange={(v) => set("fuel_type", v as FuelType)}
                />
              </Field>

              <Field label="Transmission">
                <ChipGroup
                  options={["Manual", "Automatic"] as const}
                  value={car.transmission_type}
                  onChange={(v) => set("transmission_type", v as Transmission)}
                />
              </Field>

              <Field label="Mileage" hint="km/l">
                <input
                  type="number"
                  step="0.1"
                  min={0}
                  max={50}
                  value={car.mileage}
                  onChange={(e) => set("mileage", Number(e.target.value))}
                  className={inputClass}
                />
              </Field>

              <Field label="Engine" hint="CC">
                <input
                  type="number"
                  min={0}
                  max={8000}
                  value={car.engine}
                  onChange={(e) => set("engine", Number(e.target.value))}
                  className={inputClass}
                />
              </Field>

              <Field label="Max power" hint="bhp">
                <input
                  type="number"
                  min={0}
                  max={1000}
                  value={car.max_power}
                  onChange={(e) => set("max_power", Number(e.target.value))}
                  className={inputClass}
                />
              </Field>

              <Field label="Seats">
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    aria-label="Fewer seats"
                    onClick={() => set("seats", Math.max(1, car.seats - 1))}
                    className="flex size-10 items-center justify-center rounded-[10px] border border-border bg-card transition-colors hover:border-primary hover:text-primary"
                  >
                    <Minus className="size-4" />
                  </button>
                  <input
                    type="number"
                    min={1}
                    max={10}
                    value={car.seats}
                    onChange={(e) => set("seats", Number(e.target.value))}
                    className={`${inputClass} text-center`}
                  />
                  <button
                    type="button"
                    aria-label="More seats"
                    onClick={() => set("seats", Math.min(10, car.seats + 1))}
                    className="flex size-10 items-center justify-center rounded-[10px] border border-border bg-card transition-colors hover:border-primary hover:text-primary"
                  >
                    <Plus className="size-4" />
                  </button>
                </div>
              </Field>

              <Field label="Seller type">
                <select
                  className={inputClass}
                  value={car.seller_type}
                  onChange={(e) => set("seller_type", e.target.value as SellerType)}
                >
                  {SELLER_TYPES.map((type) => (
                    <option key={type}>{type}</option>
                  ))}
                </select>
              </Field>
            </div>

            <div className="mt-9 flex flex-wrap items-center gap-4 border-t border-border pt-7">
              <button
                type="button"
                onClick={fillSample}
                className="group inline-flex items-center gap-2 rounded-lg border border-border bg-card px-4 py-3 font-accent text-sm transition-colors hover:border-primary hover:text-primary"
              >
                <RefreshCw className="size-4 transition-transform duration-500 group-hover:rotate-180" />
                Fill sample data
              </button>

              <button
                type="button"
                onClick={submit}
                disabled={loading || !canSubmit}
                className="cta-gradient inline-flex items-center gap-2 rounded-lg px-7 py-3 font-accent text-sm font-medium text-accent-foreground shadow-[var(--shadow-soft)] transition-all duration-300 hover:shadow-[var(--shadow-lift)] disabled:opacity-70"
              >
                {loading ? (
                  <>
                    <Loader2 className="size-4 animate-spin" />
                    Valuing your car…
                  </>
                ) : (
                  <>
                    <Sparkles className="size-4" />
                    Predict price
                  </>
                )}
              </button>
            </div>
            {predictError ? (
              <p className="mt-3 text-sm text-destructive">Prediction failed: {predictError}</p>
            ) : null}
          </div>
        </Reveal>
      </section>

      <div id="result">
        {result ? (
          <ResultBlock
            key={result.id}
            result={result}
            asking={asking}
            onAsking={setAsking}
            onAnalyzeAsking={analyzeAskingPrice}
            askingLoading={askingLoading}
            askingError={askingError}
          />
        ) : null}
      </div>

      {history.length > 0 ? (
        <section className="mx-auto max-w-6xl px-5 py-16">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <h2 className="font-display text-3xl">Recent valuations</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Saved locally on this device — up to 20 entries.
              </p>
            </div>
            <button
              type="button"
              onClick={() => persist([])}
              className="inline-flex items-center gap-2 rounded-lg border border-border px-4 py-2.5 font-accent text-sm text-muted-foreground transition-colors hover:border-destructive hover:text-destructive"
            >
              <Trash2 className="size-4" />
              Clear history
            </button>
          </div>

          <div className="mt-8 flex snap-x gap-5 overflow-x-auto pb-4">
            {history.map((entry) => (
              <button
                key={entry.id}
                type="button"
                onClick={() => {
                  setCar(entry.input);
                  setResult(entry);
                  setAsking(entry.asking_price ? String(entry.asking_price) : "");
                  setAskingError(null);
                  document.getElementById("result")?.scrollIntoView({ behavior: "smooth" });
                }}
                className="surface-card lift min-w-[16rem] shrink-0 snap-start p-5 text-left"
              >
                <p className="font-accent text-sm text-muted-foreground">{entry.input.brand}</p>
                <p className="font-display text-xl">{entry.input.model}</p>
                <p className="mt-3 font-display text-2xl text-primary">
                  {formatINR(entry.predicted_price)}
                </p>
                <p className="mt-3 flex items-center gap-1.5 font-accent text-xs text-muted-foreground">
                  <Clock className="size-3.5" />
                  {new Date(entry.createdAt).toLocaleString("en-IN", {
                    dateStyle: "medium",
                    timeStyle: "short",
                  })}
                </p>
              </button>
            ))}
          </div>
        </section>
      ) : null}
    </>
  );
}

function ResultBlock({
  result,
  asking,
  onAsking,
  onAnalyzeAsking,
  askingLoading,
  askingError,
}: {
  result: PredictionResult;
  asking: string;
  onAsking: (v: string) => void;
  onAnalyzeAsking: () => Promise<void>;
  askingLoading: boolean;
  askingError: string | null;
}) {
  const animated = useCountUp(result.predicted_price, 1400);

  const chartData = useMemo(
    () => [
      { name: "Low range", value: result.price_range.low, key: "low" },
      { name: "Predicted", value: result.predicted_price, key: "predicted" },
      { name: "High range", value: result.price_range.high, key: "high" },
    ],
    [result],
  );
  const dealTone = result.deal_status?.toLowerCase().includes("great")
    ? "good"
    : result.deal_status?.toLowerCase().includes("fair")
      ? "fair"
      : result.deal_status
        ? "high"
        : null;

  return (
    <section className="mx-auto max-w-6xl animate-rise px-5 pb-6">
      <div className="grid gap-6 lg:grid-cols-[1.05fr_1fr]">
        <article className="hero-gradient relative overflow-hidden rounded-2xl p-8 text-[oklch(0.96_0.01_80)] shadow-[var(--shadow-card)]">
          <div className="pointer-events-none absolute -right-16 -top-16 size-56 rounded-full bg-primary/25 blur-3xl" />
          <p className="font-accent text-xs uppercase tracking-[0.22em] opacity-65">
            Estimated fair price
          </p>
          <p className="mt-4 font-display text-5xl sm:text-6xl">{formatINR(animated)}</p>
          <p className="mt-2 font-accent text-sm opacity-75">
            {formatINR(result.price_range.low)} – {formatINR(result.price_range.high)} · approx{" "}
            {formatLakhs(result.predicted_price)}
          </p>

          <div className="mt-8">
            <div className="flex items-center justify-between font-accent text-xs opacity-75">
              <span>Model confidence</span>
              <span>{Math.round(result.confidence_score * 100)}%</span>
            </div>
            <div className="mt-2 h-2 overflow-hidden rounded-full bg-[oklch(1_0_0/0.15)]">
              <div
                className="h-full rounded-full bg-primary transition-[width] duration-1000 ease-out"
                style={{ width: `${result.confidence_score * 100}%` }}
              />
            </div>
          </div>

          <div className="mt-8 flex flex-wrap gap-2">
            <span className="rounded-lg bg-[oklch(1_0_0/0.12)] px-3 py-1.5 font-accent text-xs">
              {result.price_category} segment
            </span>
            <span className="rounded-lg bg-[oklch(1_0_0/0.12)] px-3 py-1.5 font-accent text-xs">
              {result.input.brand} {result.input.model}
            </span>
            <span className="rounded-lg bg-[oklch(1_0_0/0.12)] px-3 py-1.5 font-accent text-xs">
              {result.input.vehicle_age} yrs · {result.input.km_driven.toLocaleString("en-IN")} km
            </span>
          </div>
        </article>

        <div className="grid gap-6">
          <article className="surface-card p-6">
            <h3 className="font-display text-xl">Where it sits in the market</h3>
            <div className="mt-4 h-44">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ left: 8, right: 16 }}>
                  <XAxis type="number" hide />
                  <YAxis
                    type="category"
                    dataKey="name"
                    width={92}
                    tickLine={false}
                    axisLine={false}
                    tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                  />
                  <Tooltip
                    cursor={{ fill: "var(--muted)" }}
                    formatter={(value: number) => formatINR(value)}
                    contentStyle={{
                      borderRadius: 12,
                      border: "1px solid var(--border)",
                      fontSize: 12,
                    }}
                  />
                  <Bar dataKey="value" radius={[0, 8, 8, 0]} barSize={22}>
                    {chartData.map((entry) => (
                      <Cell
                        key={entry.key}
                        fill={
                          entry.key === "predicted"
                            ? "var(--coral)"
                            : entry.key === "low"
                              ? "var(--gold)"
                              : "var(--sage)"
                        }
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </article>

          <article className="surface-card p-6">
            <h3 className="font-display text-xl">Deal analyzer</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Enter the seller's asking price to see how it compares.
            </p>
            <input
              value={asking}
              onChange={(e) => onAsking(e.target.value)}
              inputMode="numeric"
              placeholder="e.g. 1850000"
              className={`${inputClass} mt-4`}
            />
            <button
              type="button"
              onClick={() => {
                void onAnalyzeAsking();
              }}
              disabled={askingLoading}
              className="cta-gradient mt-3 inline-flex items-center gap-2 rounded-lg px-5 py-2.5 font-accent text-sm font-medium text-accent-foreground shadow-[var(--shadow-soft)] transition-all duration-300 hover:shadow-[var(--shadow-lift)] disabled:opacity-70"
            >
              {askingLoading ? (
                <>
                  <Loader2 className="size-4 animate-spin" />
                  Checking deal...
                </>
              ) : (
                "Analyze asking price"
              )}
            </button>
            {askingError ? <p className="mt-3 text-sm text-destructive">{askingError}</p> : null}

            {result.deal_status ? (
              <div
                className="mt-4 animate-rise rounded-xl p-4"
                style={{
                  background:
                    dealTone === "good"
                      ? "color-mix(in oklab, var(--sage) 18%, transparent)"
                      : dealTone === "fair"
                        ? "color-mix(in oklab, var(--gold) 18%, transparent)"
                        : "color-mix(in oklab, var(--destructive) 14%, transparent)",
                }}
              >
                <p className="font-accent text-sm font-semibold">{result.deal_status}</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  {result.deal_message}
                </p>
                {typeof result.savings === "number" && result.savings > 0 ? (
                  <p className="mt-1 text-sm text-muted-foreground">
                    Estimated savings: {formatINR(result.savings)}
                  </p>
                ) : null}
              </div>
            ) : null}
          </article>
        </div>
      </div>
    </section>
  );
}
