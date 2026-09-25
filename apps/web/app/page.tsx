import React from "react";

async function fetchServiceHealth(url: string) {
  try {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err: any) {
    return { status: "unreachable", error: err.message };
  }
}

export default async function CockpitPage() {
  const apiHealthUrl = process.env.API_BASE_URL ? `${process.env.API_BASE_URL}/health` : "http://localhost:8000/health";
  const aiWorkerHealthUrl = process.env.AI_WORKER_URL ? `${process.env.AI_WORKER_URL}/health` : "http://localhost:8001/health";

  const [apiStatus, aiStatus] = await Promise.all([
    fetchServiceHealth(apiHealthUrl),
    fetchServiceHealth(aiWorkerHealthUrl),
  ]);

  return (
    <main style={{ minHeight: "100vh", padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <header style={{ borderBottom: "1px solid #1f2937", paddingBottom: "1.5rem", marginBottom: "2rem" }}>
        <h1 style={{ margin: 0, fontSize: "1.875rem", fontWeight: 700, color: "#f9fafb" }}>
          ⚡ AIOps SRE Developer Cockpit
        </h1>
        <p style={{ margin: "0.5rem 0 0", color: "#9ca3af" }}>
          Phase P1/P2 Operational Dashboard & Autonomous Self-Healing Pipeline
        </p>
      </header>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "1.5rem" }}>
        {/* Backend API Node */}
        <div style={{ backgroundColor: "#111827", borderRadius: "0.75rem", border: "1px solid #374151", padding: "1.5rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2 style={{ fontSize: "1.25rem", margin: 0, color: "#e5e7eb" }}>Backend API (:8000)</h2>
            <span style={{
              padding: "0.25rem 0.75rem",
              borderRadius: "9999px",
              fontSize: "0.75rem",
              fontWeight: 600,
              backgroundColor: apiStatus.status === "ok" ? "#064e3b" : "#7f1d1d",
              color: apiStatus.status === "ok" ? "#34d399" : "#f87171"
            }}>
              {apiStatus.status?.toUpperCase() || "UNKNOWN"}
            </span>
          </div>
          <p style={{ color: "#9ca3af", fontSize: "0.875rem", marginTop: "0.5rem" }}>
            Owner: Taranay (Backend Lead)
          </p>
          <pre style={{ backgroundColor: "#030712", padding: "1rem", borderRadius: "0.5rem", fontSize: "0.75rem", color: "#a7f3d0", overflowX: "auto" }}>
            {JSON.stringify(apiStatus, null, 2)}
          </pre>
        </div>

        {/* AI Worker Node (Rudra) */}
        <div style={{ backgroundColor: "#111827", borderRadius: "0.75rem", border: "1px solid #6366f1", padding: "1.5rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2 style={{ fontSize: "1.25rem", margin: 0, color: "#c7d2fe" }}>AI Worker & RAG (:8001)</h2>
            <span style={{
              padding: "0.25rem 0.75rem",
              borderRadius: "9999px",
              fontSize: "0.75rem",
              fontWeight: 600,
              backgroundColor: aiStatus.status === "ok" ? "#312e81" : "#7f1d1d",
              color: aiStatus.status === "ok" ? "#a5b4fc" : "#f87171"
            }}>
              {aiStatus.status?.toUpperCase() || "UNKNOWN"}
            </span>
          </div>
          <p style={{ color: "#9ca3af", fontSize: "0.875rem", marginTop: "0.5rem" }}>
            Owner: <strong>Rudra (AI / RAG Lead)</strong>
          </p>
          <pre style={{ backgroundColor: "#030712", padding: "1rem", borderRadius: "0.5rem", fontSize: "0.75rem", color: "#c4b5fd", overflowX: "auto" }}>
            {JSON.stringify(aiStatus, null, 2)}
          </pre>
        </div>
      </section>
    </main>
  );
}
