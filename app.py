# app.py
"""
Gradio interface for the Multi-Agent Transit Anomaly Detection system.

Usage from main.ipynb:
    from app import launch_app
    launch_app(
        run_agent_with_supervisor=run_agent_with_supervisor,
        build_data_agent_prompt=_build_data_agent_prompt,
        build_baseline_prompt=_build_baseline_prompt,
        build_outlier_prompt=_build_outlier_prompt,
        build_risk_prompt=_build_risk_prompt,
        build_report_prompt=_build_report_prompt,
        validators={
            "data_agent": validate_data_agent_output,
            "baseline":   validate_baseline_output,
            "outlier":    validate_outlier_output,
            "risk":       validate_risk_output,
            "report":     validate_report_output,
        },
        output_dir=OUTPUT_DIR,
        set_user_query=lambda q: globals().__setitem__("USER_QUERY", q),
    )
"""

import os
import math
import pandas as pd
import gradio as gr
import plotly.graph_objects as go


# ──────────────────────────────────────────────────────────────────────
# Airport reference (lat, lon, full name) — IATA codes seen in the dataset
# ──────────────────────────────────────────────────────────────────────
AIRPORTS = {
    # Italy
    "FCO": {"lat": 41.8003, "lon": 12.2389, "name": "Roma Fiumicino"},
    "CIA": {"lat": 41.7994, "lon": 12.5949, "name": "Roma Ciampino"},
    "MXP": {"lat": 45.6306, "lon": 8.7281,  "name": "Milano Malpensa"},
    "LIN": {"lat": 45.4451, "lon": 9.2767,  "name": "Milano Linate"},
    "BGY": {"lat": 45.6739, "lon": 9.7042,  "name": "Bergamo Orio al Serio"},
    "VCE": {"lat": 45.5053, "lon": 12.3519, "name": "Venezia"},
    "TSF": {"lat": 45.6484, "lon": 12.1944, "name": "Treviso"},
    "BLQ": {"lat": 44.5354, "lon": 11.2887, "name": "Bologna"},
    "FLR": {"lat": 43.8100, "lon": 11.2051, "name": "Firenze Peretola"},
    "PSA": {"lat": 43.6839, "lon": 10.3927, "name": "Pisa"},
    "PEG": {"lat": 43.0959, "lon": 12.5132, "name": "Perugia"},
    "NAP": {"lat": 40.8860, "lon": 14.2908, "name": "Napoli"},
    "BRI": {"lat": 41.1389, "lon": 16.7606, "name": "Bari"},
    "CTA": {"lat": 37.4668, "lon": 15.0664, "name": "Catania Fontanarossa"},
    "PMO": {"lat": 38.1759, "lon": 13.0910, "name": "Palermo"},
    "TRN": {"lat": 45.2008, "lon": 7.6496,  "name": "Torino"},
    "VRN": {"lat": 45.3957, "lon": 10.8885, "name": "Verona"},

    # United Kingdom
    "LHR": {"lat": 51.4700, "lon": -0.4543, "name": "London Heathrow"},
    "LGW": {"lat": 51.1537, "lon": -0.1821, "name": "London Gatwick"},
    "STN": {"lat": 51.8860, "lon": 0.2389,  "name": "London Stansted"},
    "LCY": {"lat": 51.5053, "lon": 0.0553,  "name": "London City"},
    "LTN": {"lat": 51.8747, "lon": -0.3683, "name": "London Luton"},
    "MAN": {"lat": 53.3537, "lon": -2.2750, "name": "Manchester"},
    "EDI": {"lat": 55.9500, "lon": -3.3725, "name": "Edinburgh"},
    "BRS": {"lat": 51.3827, "lon": -2.7191, "name": "Bristol"},

    # Europe & Mediterranean
    "IST": {"lat": 41.2753, "lon": 28.7519, "name": "Istanbul Airport"},
    "SAW": {"lat": 40.8986, "lon": 29.3092, "name": "Istanbul Sabiha Gokcen"},
    "TIA": {"lat": 41.4147, "lon": 19.7206, "name": "Tirana"},
    "EVN": {"lat": 40.1473, "lon": 44.3959, "name": "Yerevan"},

    # Middle East / Africa
    "TUN": {"lat": 36.8510, "lon": 10.2272, "name": "Tunis"},
    "CMN": {"lat": 33.3675, "lon": -7.5898, "name": "Casablanca"},
    "RAK": {"lat": 31.6069, "lon": -8.0363, "name": "Marrakech"},
    "SSH": {"lat": 27.9773, "lon": 34.3950, "name": "Sharm el-Sheikh"},
    "AMM": {"lat": 31.7226, "lon": 35.9933, "name": "Amman"},
    "DOH": {"lat": 25.2731, "lon": 51.6080, "name": "Doha"},
    "DSS": {"lat": 14.6701, "lon": -17.0731, "name": "Dakar Blaise Diagne"},

    # Asia
    "DEL": {"lat": 28.5562, "lon": 77.1000,  "name": "Delhi"},
    "PEK": {"lat": 40.0801, "lon": 116.5846, "name": "Beijing"},
    "SZX": {"lat": 22.6393, "lon": 113.8108, "name": "Shenzhen"},
    "MLE": {"lat": 4.1918,  "lon": 73.5290,  "name": "Male"},

    # Americas
    "JFK": {"lat": 40.6413, "lon": -73.7781, "name": "New York JFK"},
    "DFW": {"lat": 32.8998, "lon": -97.0403, "name": "Dallas Fort Worth"},
    "GRU": {"lat": -23.4356, "lon": -46.4731, "name": "Sao Paulo Guarulhos"},
}

# Backward-compatible coordinate lookup (used by load_risk_report and build_world_map)
AIRPORT_COORDS = {code: (info["lat"], info["lon"]) for code, info in AIRPORTS.items()}

# Name lookup (used by build_iata_block_for_prompt in the notebook)
AIRPORT_NAMES = {code: info["name"] for code, info in AIRPORTS.items()}


RISK_COLORS = {
    "CRITICAL": "#d62728",   # red
    "HIGH":     "#ff7f0e",   # orange
    "MEDIUM":   "#f1c40f",   # yellow
    "LOW":      "#2ca02c",   # green
}

RISK_WIDTHS = {
    "CRITICAL": 4.0,
    "HIGH":     3.0,
    "MEDIUM":   2.0,
    "LOW":      1.2,
}


# ──────────────────────────────────────────────────────────────────────
# Risk report parsing
# ──────────────────────────────────────────────────────────────────────
def _split_group_key(group_key: str):
    """
    group_key format: 'departure|arrival' (lowercase IATA-like codes).
    Returns (dep_iata_upper, arr_iata_upper) or (None, None) if malformed.
    """
    if not isinstance(group_key, str) or "|" not in group_key:
        return None, None
    parts = group_key.split("|")
    if len(parts) != 2:
        return None, None
    dep, arr = parts[0].strip().upper(), parts[1].strip().upper()
    if not dep or not arr:
        return None, None
    return dep, arr


def load_risk_report(output_dir: str) -> pd.DataFrame:
    """
    Load risk_report.csv and enrich it with:
      - dep_iata, arr_iata (uppercase, parsed from group_key)
      - dep_lat, dep_lon, arr_lat, arr_lon (from AIRPORT_COORDS)
      - route_label (e.g. 'TIA → BGY')
      - mappable (bool: True if both endpoints have coordinates)
    Rows where either endpoint is unknown remain in the dataframe but
    are marked mappable=False (they will be skipped by the map but kept
    in the table).
    """
    path = os.path.join(output_dir, "risk_report.csv")
    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path)
    if df.empty:
        return df

    deps, arrs = [], []
    dep_lats, dep_lons, arr_lats, arr_lons = [], [], [], []
    mappable = []

    for gk in df.get("group_key", []):
        dep, arr = _split_group_key(gk)
        deps.append(dep)
        arrs.append(arr)

        dep_xy = AIRPORT_COORDS.get(dep) if dep else None
        arr_xy = AIRPORT_COORDS.get(arr) if arr else None

        if dep_xy is None and dep:
            print(f"[map] skipping unknown IATA: {dep}")
        if arr_xy is None and arr:
            print(f"[map] skipping unknown IATA: {arr}")

        dep_lats.append(dep_xy[0] if dep_xy else None)
        dep_lons.append(dep_xy[1] if dep_xy else None)
        arr_lats.append(arr_xy[0] if arr_xy else None)
        arr_lons.append(arr_xy[1] if arr_xy else None)
        mappable.append(dep_xy is not None and arr_xy is not None)

    df["dep_iata"] = deps
    df["arr_iata"] = arrs
    df["dep_lat"] = dep_lats
    df["dep_lon"] = dep_lons
    df["arr_lat"] = arr_lats
    df["arr_lon"] = arr_lons
    df["mappable"] = mappable
    df["route_label"] = [
        f"{d} → {a}" if d and a else "?" for d, a in zip(deps, arrs)
    ]

    # Normalize risk_level just in case
    if "risk_level" in df.columns:
        df["risk_level"] = df["risk_level"].astype(str).str.upper().str.strip()

    return df

# ──────────────────────────────────────────────────────────────────────
# World map (orthographic globe with route arcs)
# ──────────────────────────────────────────────────────────────────────
def build_world_map(df_risk: pd.DataFrame) -> go.Figure:
    """
    Build an orthographic world map showing all mappable routes from the
    risk_report, colored by risk level. Endpoints are shown as markers
    with hover info.
    """
    fig = go.Figure()

    if df_risk is None or df_risk.empty:
        fig.update_layout(
            title="No risk data available — run a query first",
            geo=dict(projection_type="orthographic", showland=True,
                     landcolor="#EAEAEA", oceancolor="#CFE3F2", showocean=True),
            margin=dict(l=0, r=0, t=40, b=0),
            height=600,
        )
        return fig

    df_map = df_risk[df_risk["mappable"]].copy()

    # One trace per risk level so the legend is clean and toggleable
    risk_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    for level in risk_order:
        sub = df_map[df_map["risk_level"] == level]
        if sub.empty:
            continue

        color = RISK_COLORS.get(level, "#888888")
        width = RISK_WIDTHS.get(level, 1.5)

        # Route lines (one segment per row, drawn as a single trace
        # using None separators between routes to keep legend compact)
        line_lats, line_lons, line_hover = [], [], []
        for _, row in sub.iterrows():
            line_lats += [row["dep_lat"], row["arr_lat"], None]
            line_lons += [row["dep_lon"], row["arr_lon"], None]
            hover = (
                f"<b>{row['route_label']}</b><br>"
                f"Risk: {level}<br>"
                f"Score: {row.get('risk_score', float('nan')):.2f}<br>"
                f"Dataset: {row.get('dataset', '?')}"
            )
            line_hover += [hover, hover, None]

        fig.add_trace(go.Scattergeo(
            lat=line_lats,
            lon=line_lons,
            mode="lines",
            line=dict(width=width, color=color),
            opacity=0.85,
            name=f"{level} ({len(sub)})",
            hoverinfo="text",
            text=line_hover,
        ))

        # Endpoint markers (departure + arrival) for this level
        marker_lats = list(sub["dep_lat"]) + list(sub["arr_lat"])
        marker_lons = list(sub["dep_lon"]) + list(sub["arr_lon"])
        marker_text = (
            [f"{r['dep_iata']} (departure)<br>{r['route_label']} — {level}"
             for _, r in sub.iterrows()] +
            [f"{r['arr_iata']} (arrival)<br>{r['route_label']} — {level}"
             for _, r in sub.iterrows()]
        )
        fig.add_trace(go.Scattergeo(
            lat=marker_lats,
            lon=marker_lons,
            mode="markers",
            marker=dict(size=6, color=color, line=dict(width=0.5, color="#333")),
            name=f"{level} airports",
            hoverinfo="text",
            text=marker_text,
            showlegend=False,
        ))

    fig.update_layout(
        title="Transit risk routes — world view",
        geo=dict(
            projection_type="orthographic",
            projection_rotation=dict(lon=10, lat=40, roll=0),  # centered on Europe
            showland=True, landcolor="#EAEAEA",
            showocean=True, oceancolor="#CFE3F2",
            showcountries=True, countrycolor="#FFFFFF",
            showcoastlines=True, coastlinecolor="#888888",
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=620,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.05,
            xanchor="center", x=0.5,
        ),
    )
    return fig

# ──────────────────────────────────────────────────────────────────────
# Partial pipeline runner (skips Profiling + Cleaning, reuses cached files)
# ──────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────
# Partial pipeline runner (skips Profiling + Cleaning, reuses cached files)
# ──────────────────────────────────────────────────────────────────────
def run_pipeline_partial(
    user_query: str,
    *,
    run_agent_with_supervisor,
    build_data_agent_prompt,
    build_baseline_prompt,
    build_outlier_prompt,
    build_risk_prompt,
    build_report_prompt,
    validators: dict,
    output_dir: str,
    scope_manifest_json: str,
    report_md_path: str,
    set_user_query,
):
    """
    Executes the agent pipeline starting from cleaned data:
      Data Agent (writes scope_manifest.json)
        → Baseline           (baseline_data.csv)
        → Outlier Detection  (outliers.csv)
        → Risk Profiling     (risk_report.csv)
        → Report             (anomaly_report.md)

    Assumes column_profiles.json, allarmi_clean.csv and tipologia_clean.csv
    already exist in `output_dir` (produced by a previous full run).

    All progress logs go to stdout (terminal / cell output), not the UI.

    Returns a dict with keys:
      - succeeded   (bool)
      - failed_at   (None or stage task_name)
      - report_md   (str, content of anomaly_report.md or "")
      - df_risk     (pd.DataFrame, parsed + enriched risk_report or empty)
    """
    print("\n" + "=" * 60)
    print(f"  GRADIO PIPELINE  |  query = {user_query!r}")
    print("=" * 60)

    # Push the query into the notebook's global USER_QUERY so the
    # prompt builders pick it up.
    set_user_query(user_query)

    # Each stage tuple: (task_name, prompt_builder, validator_key, output_path)
    # task_name MUST match the names used inside run_agent_with_supervisor
    # in the notebook.
    stages = [
        ("data_agent",        build_data_agent_prompt, "data_agent",
         scope_manifest_json),
        ("baseline",          build_baseline_prompt,   "baseline",
         os.path.join(output_dir, "baseline_data.csv")),
        ("outlier_detection", build_outlier_prompt,    "outlier",
         os.path.join(output_dir, "outliers.csv")),
        ("risk_profiling",    build_risk_prompt,       "risk",
         os.path.join(output_dir, "risk_report.csv")),
        ("report",            build_report_prompt,     "report",
         report_md_path),
    ]

    for task_name, prompt_builder, validator_key, out_path in stages:
        print(f"\n──  stage: {task_name}  ──")
        result = run_agent_with_supervisor(
            task_name=task_name,
            prompt=prompt_builder(),
            validator_fn=validators[validator_key],
            output_path=out_path,
            max_retries=3,
        )
        if not result.get("succeeded"):
            print(f"[pipeline] FAILED at stage: {task_name}")
            return {
                "succeeded": False,
                "failed_at": task_name,
                "report_md": "",
                "df_risk": pd.DataFrame(),
            }

    # Read final outputs
    report_md = ""
    if os.path.exists(report_md_path):
        with open(report_md_path, "r", encoding="utf-8") as f:
            report_md = f.read()

    df_risk = load_risk_report(output_dir)

    print("\n[pipeline] all stages succeeded.\n")
    return {
        "succeeded": True,
        "failed_at": None,
        "report_md": report_md,
        "df_risk": df_risk,
    }


# ──────────────────────────────────────────────────────────────────────
# Gradio UI
# ──────────────────────────────────────────────────────────────────────
def launch_app(
    *,
    run_agent_with_supervisor,
    build_data_agent_prompt,
    build_baseline_prompt,
    build_outlier_prompt,
    build_risk_prompt,
    build_report_prompt,
    validators: dict,
    output_dir: str,
    scope_manifest_json: str,
    report_md_path: str,
    set_user_query,
    server_name: str = "127.0.0.1",
    server_port: int = 7864,
    share: bool = False,
):
    """
    Launches the Gradio interface.

    The pipeline runs partially (skips profiling + cleaning, reuses cached
    column_profiles.json + *_clean.csv files in output_dir).

    Logs go to stdout — the UI shows only the final report, the risky
    routes table, and the world map.
    """

    # Columns to display in the risky routes table (only the ones that
    # exist in the dataframe — the rest are silently skipped).
    PREFERRED_TABLE_COLS = [
        "route_label", "dataset", "risk_level", "risk_score",
        "rate", "z_score", "ratio_to_baseline",
        "n_records", "group_volume", "risk_reason",
    ]

    def _render_table(df_risk: pd.DataFrame) -> pd.DataFrame:
        if df_risk is None or df_risk.empty:
            return pd.DataFrame(columns=["route_label", "risk_level", "risk_reason"])
        cols = [c for c in PREFERRED_TABLE_COLS if c in df_risk.columns]
        # Sort by risk severity then score
        severity = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        df_sorted = df_risk.copy()
        df_sorted["_sev"] = df_sorted["risk_level"].map(severity).fillna(99)
        sort_cols = ["_sev"] + (["risk_score"] if "risk_score" in df_sorted.columns else [])
        df_sorted = df_sorted.sort_values(
            sort_cols, ascending=[True] + [False] * (len(sort_cols) - 1)
        ).drop(columns=["_sev"])
        # Round floats for readability
        for c in ("risk_score", "rate", "z_score", "ratio_to_baseline"):
            if c in df_sorted.columns:
                df_sorted[c] = pd.to_numeric(df_sorted[c], errors="coerce").round(3)
        return df_sorted[cols]
    
    def _on_submit(query: str):
        query = (query or "").strip()
        if not query:
            empty_fig = build_world_map(pd.DataFrame())
            return ("⚠️ Please enter a query first.",
                    pd.DataFrame(columns=["route_label", "risk_level", "risk_reason"]),
                    empty_fig)

        result = run_pipeline_partial(
            user_query=query,
            run_agent_with_supervisor=run_agent_with_supervisor,
            build_data_agent_prompt=build_data_agent_prompt,
            build_baseline_prompt=build_baseline_prompt,
            build_outlier_prompt=build_outlier_prompt,
            build_risk_prompt=build_risk_prompt,
            build_report_prompt=build_report_prompt,
            validators=validators,
            output_dir=output_dir,
            scope_manifest_json=scope_manifest_json,
            report_md_path=report_md_path,
            set_user_query=set_user_query,
        )

        if not result["succeeded"]:
            err = (f"❌ Pipeline failed at stage: **{result['failed_at']}**.\n\n"
                f"Check the terminal output for details.")
            return (err,
                    pd.DataFrame(columns=["route_label", "risk_level", "risk_reason"]),
                    build_world_map(pd.DataFrame()))

        # ── NEW: handle the "no anomalies found" case gracefully ──────────
        df_risk = result["df_risk"]
        if df_risk is None or df_risk.empty:
            msg = (
                "## ✅ No anomalies found\n\n"
                f"The pipeline ran successfully for your query, but **no risky routes** "
                f"were detected in the selected scope.\n\n"
                f"This is a valid result — it means the data in scope behaves within "
                f"the expected baseline.\n\n"
                f"Try a broader query (e.g. *show me all anomaly routes*) to explore "
                f"the full dataset."
            )
            # If the report agent still wrote something, prepend it
            if result["report_md"]:
                msg = result["report_md"] + "\n\n---\n\n" + msg
            return (msg,
                    pd.DataFrame(columns=["route_label", "risk_level", "risk_reason"]),
                    build_world_map(pd.DataFrame()))

        # Normal path: anomalies present
        report_md = result["report_md"] or "*(empty report)*"
        table = _render_table(df_risk)
        fig = build_world_map(df_risk)
        return report_md, table, fig

    with gr.Blocks(title="Transit Anomaly Detection — Multi-Agent",
                   theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            "# ✈️ Transit Anomaly Detection\n"
            "Multi-agent pipeline for identifying risky transit routes.\n\n"
            "Enter a natural-language query (e.g. *show me anomaly routes departing from Albania*, "
            "*anomaly flights arriving in Rome*."
        )

        with gr.Row():
            query_box = gr.Textbox(
                label="Query",
                placeholder="flights with anomalies from istanbul",
                lines=1,
                scale=5,
            )
            run_btn = gr.Button("Run pipeline", variant="primary", scale=1)

        with gr.Tabs():
            with gr.Tab("📋 Report"):
                report_out = gr.Markdown(
                    "*Submit a query to generate the Anomaly Report.*"
                )
            with gr.Tab("⚠️ Risky routes"):
                table_out = gr.Dataframe(
                    headers=["route_label", "risk_level", "risk_reason"],
                    interactive=False,
                    wrap=True,
                )
            with gr.Tab("🌍 World map"):
                map_out = gr.Plot(value=build_world_map(pd.DataFrame()))

        run_btn.click(
            fn=_on_submit,
            inputs=[query_box],
            outputs=[report_out, table_out, map_out],
        )
        query_box.submit(
            fn=_on_submit,
            inputs=[query_box],
            outputs=[report_out, table_out, map_out],
        )

    import socket

    def _find_free_port(start: int, attempts: int = 20) -> int:
        """Try ports start, start+1, ..., start+attempts-1 and return the first free one."""
        for p in range(start, start + attempts):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind((server_name, p))
                    return p
                except OSError:
                    continue
        raise RuntimeError(f"No free port found in range {start}-{start + attempts - 1}")

    actual_port = _find_free_port(server_port)
    if actual_port != server_port:
        print(f"[gradio] port {server_port} busy, using {actual_port} instead")
    demo.launch(server_name=server_name, server_port=actual_port, share=share)
    return demo