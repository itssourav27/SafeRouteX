import gradio as gr
from backend.api import compute_route_logic, list_districts
from app.visualization.map import build_map_html


def run_route(start, end):
    result = compute_route_logic(start, end)
    if "error" in result:
        return result["error"], "<p>No map</p>"

    map_html = build_map_html(
        result["coordinates"],
        start,
        end,
        result["safehouses"]
    )

    return result["summary"], map_html


with gr.Blocks(title="🚨 Evacuation Planner (Backend-First)") as demo:
    gr.Markdown("## 🚨 Evacuation Planner")

    districts = list_districts()

    with gr.Row():
        start = gr.Dropdown(districts, label="Start District")
        end = gr.Dropdown(districts, label="Destination District")

    run_btn = gr.Button("🧭 Compute Evacuation Route")

    summary = gr.Textbox(label="Route Summary", lines=6)
    map_view = gr.HTML(label="Evacuation Map")

    run_btn.click(
        run_route,
        inputs=[start, end],
        outputs=[summary, map_view]
    )

def launch_app():
    demo.launch(server_name="0.0.0.0", server_port=7860)
