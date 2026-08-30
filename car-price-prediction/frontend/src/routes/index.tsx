import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Hero } from "@/components/sections/Hero";
import { Features } from "@/components/sections/Features";
import { Predictor } from "@/components/sections/Predictor";
import { DataScience } from "@/components/sections/DataScience";
import { FloatingWidgets } from "@/components/sections/Chatbot";
import { fetchBootstrapData, isModelReady, type BootstrapData } from "@/lib/api";

const TITLE = "CarCast — Know Your Car's True Worth in Seconds";
const DESCRIPTION =
  "AI-powered used car valuation trained on 15,000+ real listings. Get an instant fair price, market comparison and deal analysis.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESCRIPTION },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  const [bootstrapData, setBootstrapData] = useState<BootstrapData | null>(null);
  const [apiReady, setApiReady] = useState<boolean | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    const loadBootstrapData = async () => {
      try {
        const data = await fetchBootstrapData();
        if (!mounted) return;

        setBootstrapData(data);
        setApiError(null);
        setApiReady(isModelReady(data.health) && data.modelInfo.is_loaded);
      } catch (error) {
        if (!mounted) return;
        setApiReady(false);
        setApiError(
          error instanceof Error ? error.message : "Unable to connect to the FastAPI backend.",
        );
      }
    };

    void loadBootstrapData();

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="min-h-screen">
      <Navbar apiStatus={apiReady} apiVersion={bootstrapData?.apiInfo.version} />
      {apiReady === false ? (
        <div className="border-b border-destructive/25 bg-destructive/10 px-5 py-2 text-center text-sm text-destructive">
          {bootstrapData
            ? "Backend is reachable but model is not ready. Please verify /health and model loading."
            : `Unable to connect to backend API. ${apiError ?? "Please check the base URL and backend server."}`}
        </div>
      ) : null}
      <main>
        <Hero
          modelName={bootstrapData?.modelInfo.model_metrics.model_name}
          r2Score={bootstrapData?.modelInfo.model_metrics.r2_score}
        />
        <Features modelMetrics={bootstrapData?.modelInfo.model_metrics} />
        <Predictor />
        <DataScience modelInfo={bootstrapData?.modelInfo} apiError={apiError} />
      </main>
      <Footer />
      <FloatingWidgets />
    </div>
  );
}
