export type Evaluation = { decision:string; risk_score:number; confidence:number; reasons:string[]; triggered_policies:string[]; evidence_coverage:number; latency_ms:number; detectors_run:string[]; redacted_output?:string; };
export type Analytics = { evaluations:number; flagged:number; blocked:number; reviews:number; average_latency_ms:number; categories:{name:string; value:number}[]; trend:{day:string; risk:number; events:number}[]; };

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export async function evaluateInteraction(payload: { application:string; input:string; output:string; context:string[] }): Promise<Evaluation> {
  const response = await fetch(`${API_URL}/v1/evaluate`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload) });
  if (!response.ok) throw new Error("Evaluation service unavailable");
  return response.json();
}

export async function getAnalytics(): Promise<Analytics> {
  const response = await fetch(`${API_URL}/v1/analytics`, { cache:"no-store" });
  if (!response.ok) throw new Error("Analytics service unavailable");
  return response.json();
}

export async function getIncidents(): Promise<Evaluation[]> {
  const response = await fetch(`${API_URL}/v1/incidents`, { cache:"no-store" });
  if (!response.ok) throw new Error("Incident service unavailable");
  const payload = await response.json();
  return payload.items;
}
