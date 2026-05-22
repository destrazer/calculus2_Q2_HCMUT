import html
import math
import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
    function_exponentiation,
)

try:
    from st_keyup import st_keyup
except ImportError:
    st.set_page_config(page_title="Directional Derivative Visualizer", layout="wide")
    st.error("Missing package: streamlit-keyup")
    st.code("pip install streamlit-keyup")
    st.stop()

# =====================================================
# 1. Page configuration
# =====================================================
st.set_page_config(
    page_title="Directional Derivative Visualizer",
    layout="wide"
)

# =====================================================
# 2. CSS
# =====================================================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 4.2rem !important;
        padding-left: 2.4rem !important;
        padding-right: 2.4rem !important;
        padding-bottom: 2rem !important;
        max-width: 1550px;
    }

    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        margin-top: 0rem;
        margin-bottom: 0.25rem;
        line-height: 1.2;
    }

    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #666;
        margin-bottom: 0.75rem;
    }

    .preview-raw {
        text-align: center;
        font-size: 27px;
        font-weight: 500;
        color: #1f1f1f;
        font-family: "Times New Roman", "Cambria Math", serif;
        min-height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        white-space: pre-wrap;
        word-break: break-word;
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
    }

    .preview-empty {
        text-align: center;
        font-size: 25px;
        color: #999;
        min-height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
    }

    .section-title {
        font-size: 19px;
        font-weight: 750;
        margin-top: 0.25rem;
        margin-bottom: 0.45rem;
    }

    .small-title {
        font-size: 15px;
        font-weight: 700;
        margin-top: 0.3rem;
        margin-bottom: 0.35rem;
        color: #333;
    }

    .stButton > button {
        height: 34px !important;
        min-height: 34px !important;
        padding: 0px 3px !important;
        font-size: 15px !important;
        border-radius: 7px !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        line-height: 1 !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.18rem !important;
    }

    div[data-testid="column"] {
        padding-left: 0.01rem !important;
        padding-right: 0.01rem !important;
    }

    input {
        font-size: 15px !important;
    }

    .compact-caption {
        color: #777;
        font-size: 13px;
        margin-top: 0.2rem;
        margin-bottom: 0.3rem;
    }

    hr {
        margin-top: 0.6rem !important;
        margin-bottom: 0.6rem !important;
    }

    .result-card {
        border: 1px solid #e2e2e2;
        border-radius: 12px;
        padding: 14px 16px;
        background-color: #f8f9fa;
        min-height: 96px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .result-label {
        font-size: 14px;
        color: #333333;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .result-value {
        font-size: 24px;
        color: #1f2937;
        font-weight: 650;
        line-height: 1.25;
        word-break: break-word;
        white-space: normal;
    }

    .result-value-small {
        font-size: 21px;
        color: #1f2937;
        font-weight: 650;
        line-height: 1.25;
        word-break: break-word;
        white-space: normal;
    }

    .info-line {
        font-size: 16px;
        margin-bottom: 10px;
        color: #222;
    }

    .submitted-formula-box {
        border: 1px solid #e5e7eb;
        background-color: #fbfbfb;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 14px;
    }

    .success-box {
        background-color: #e6f7ec;
        color: #087f23;
        padding: 16px 18px;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 16px;
    }

    .warning-box {
        background-color: #fff3cd;
        color: #8a5a00;
        padding: 16px 18px;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 16px;
    }

    .neutral-box {
        background-color: #e7f3ff;
        color: #075985;
        padding: 16px 18px;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 3. Session state
# =====================================================
if "draft_expr" not in st.session_state:
    st.session_state.draft_expr = "x^2 + y^2"

if "submitted_data" not in st.session_state:
    st.session_state.submitted_data = None

if "keyboard_version" not in st.session_state:
    st.session_state.keyboard_version = 0


def bump_keyboard_version():
    st.session_state.keyboard_version += 1


def append_token(token):
    st.session_state.draft_expr += token
    bump_keyboard_version()


def clear_expression():
    st.session_state.draft_expr = ""
    bump_keyboard_version()


def backspace_expression():
    st.session_state.draft_expr = st.session_state.draft_expr[:-1]
    bump_keyboard_version()


# =====================================================
# 4. Header
# =====================================================
st.markdown(
    '<div class="main-title">Directional Derivative Visualizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Calculate and visualize the geometric meaning of the directional derivative.</div>',
    unsafe_allow_html=True
)

# =====================================================
# 5. Symbols and parser
# =====================================================
x, y = sp.symbols("x y")

transformations = (
    standard_transformations
    + (implicit_multiplication_application, convert_xor, function_exponentiation)
)

local_dict = {
    "x": x,
    "y": y,

    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "sec": sp.sec,
    "csc": sp.csc,
    "cot": sp.cot,

    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "arcsin": sp.asin,
    "arccos": sp.acos,
    "arctan": sp.atan,

    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,

    "sqrt": sp.sqrt,
    "log": sp.log,
    "ln": sp.log,
    "exp": sp.exp,
    "abs": sp.Abs,

    "pi": sp.pi,
    "e": sp.E,
    "E": sp.E,

    "log10": lambda z: sp.log(z, 10),
}


def parse_math_expression(expr_text):
    expr_text = expr_text.strip()

    if expr_text == "":
        raise ValueError("Expression is empty.")

    expr = parse_expr(
        expr_text,
        local_dict=local_dict,
        transformations=transformations,
        evaluate=True
    )

    if not expr.free_symbols.issubset({x, y}):
        raise ValueError("The expression can only contain variables x and y.")

    return expr


def format_number(value, max_digits=6):
    value = float(value)

    if not math.isfinite(value):
        return str(value)

    if abs(value) < 1e-12:
        return "0"

    if abs(value - round(value)) < 1e-10:
        return str(int(round(value)))

    text = f"{value:.{max_digits}f}"
    text = text.rstrip("0").rstrip(".")

    if text == "-0":
        text = "0"

    return text


def format_pair(a, b, max_digits=6):
    return f"({format_number(a, max_digits)}, {format_number(b, max_digits)})"


# =====================================================
# 6. Button grid helper
# =====================================================
def button_grid(buttons, cols_per_row, group_name):
    for row_start in range(0, len(buttons), cols_per_row):
        row_buttons = buttons[row_start: row_start + cols_per_row]
        cols = st.columns(cols_per_row, gap="small")

        for j, item in enumerate(row_buttons):
            label, token, action = item
            unique_key = f"{group_name}_{row_start}_{j}_{label}_{token}"

            if action == "append":
                cols[j].button(
                    label,
                    key=unique_key,
                    use_container_width=True,
                    on_click=append_token,
                    args=(token,)
                )

            elif action == "clear":
                cols[j].button(
                    label,
                    key=unique_key,
                    use_container_width=True,
                    on_click=clear_expression
                )

            elif action == "backspace":
                cols[j].button(
                    label,
                    key=unique_key,
                    use_container_width=True,
                    on_click=backspace_expression
                )


# =====================================================
# 7. Preview display
# =====================================================
def render_expression_preview(expr_text):
    expr_text = expr_text.strip()

    if expr_text == "":
        st.markdown(
            '<div class="preview-empty">f(x, y) =</div>',
            unsafe_allow_html=True
        )
        return False

    try:
        expr = parse_math_expression(expr_text)
        st.latex(r"f(x,y)=" + sp.latex(expr))
        return True

    except Exception:
        escaped = html.escape(expr_text)
        st.markdown(
            f'<div class="preview-raw">f(x, y) = {escaped}</div>',
            unsafe_allow_html=True
        )
        return False


# =====================================================
# 8. Cached calculation and plotting data
# =====================================================
@st.cache_data(show_spinner=False)
def generate_plot_data(expr_string, u1, u2, x0, y0, radius, grid_size):
    f_expr = parse_math_expression(expr_string)

    fx_expr = sp.diff(f_expr, x)
    fy_expr = sp.diff(f_expr, y)

    z0 = float(f_expr.subs({x: x0, y: y0}))
    fx0 = float(fx_expr.subs({x: x0, y: y0}))
    fy0 = float(fy_expr.subs({x: x0, y: y0}))

    grad = np.array([fx0, fy0], dtype=float)
    u = np.array([u1, u2], dtype=float)

    norm_u = np.linalg.norm(u)

    if norm_u == 0:
        raise ValueError("Direction vector u cannot be the zero vector.")

    unit_u = u / norm_u
    directional_derivative = float(np.dot(grad, unit_u))

    custom_numpy_modules = {
        "sec": lambda z: 1 / np.cos(z),
        "csc": lambda z: 1 / np.sin(z),
        "cot": lambda z: 1 / np.tan(z),
        "Abs": np.abs,
    }

    f_num = sp.lambdify(
        (x, y),
        f_expr,
        modules=[custom_numpy_modules, "numpy"]
    )

    def safe_eval(X_input, Y_input):
        with np.errstate(all="ignore"):
            Z_output = f_num(X_input, Y_input)

        if np.isscalar(Z_output):
            Z_output = np.full_like(X_input, Z_output, dtype=complex)

        Z_output = np.array(Z_output)

        if np.iscomplexobj(Z_output):
            imag_abs = np.abs(np.imag(Z_output))
            Z_output = np.where(imag_abs < 1e-8, np.real(Z_output), np.nan)

        Z_output = np.array(Z_output, dtype=float)
        Z_output[~np.isfinite(Z_output)] = np.nan

        return Z_output

    X_vals = np.linspace(x0 - radius, x0 + radius, grid_size)
    Y_vals = np.linspace(y0 - radius, y0 + radius, grid_size)

    X_grid, Y_grid = np.meshgrid(X_vals, Y_vals)
    Z_grid = safe_eval(X_grid, Y_grid)

    Z_tangent_plane = z0 + fx0 * (X_grid - x0) + fy0 * (Y_grid - y0)

    t_vals = np.linspace(-radius, radius, 300)

    X_curve = x0 + t_vals * unit_u[0]
    Y_curve = y0 + t_vals * unit_u[1]
    Z_curve = safe_eval(X_curve, Y_curve)

    Z_tangent_line = z0 + directional_derivative * t_vals

    return {
        "f_expr_latex": sp.latex(f_expr),
        "fx_expr_latex": sp.latex(fx_expr),
        "fy_expr_latex": sp.latex(fy_expr),

        "z0": z0,
        "fx0": fx0,
        "fy0": fy0,
        "unit_u_0": unit_u[0],
        "unit_u_1": unit_u[1],
        "directional_derivative": directional_derivative,

        "X_grid": X_grid,
        "Y_grid": Y_grid,
        "Z_grid": Z_grid,
        "Z_tangent_plane": Z_tangent_plane,

        "t_vals": t_vals,
        "X_curve": X_curve,
        "Y_curve": Y_curve,
        "Z_curve": Z_curve,
        "Z_tangent_line": Z_tangent_line,
    }


# =====================================================
# 9. Formula area and realtime source input
# =====================================================
_, mid_col, _ = st.columns([1, 2.6, 1])

with mid_col:
    formula_placeholder = st.empty()

    current_source = st_keyup(
        "Equation source",
        value=st.session_state.draft_expr,
        key=f"equation_source_keyup_{st.session_state.keyboard_version}",
        debounce=0
    )

    if current_source is not None and current_source != st.session_state.draft_expr:
        st.session_state.draft_expr = current_source

    with formula_placeholder.container():
        render_expression_preview(st.session_state.draft_expr)

st.markdown("---")

# =====================================================
# 10. Keyboard
# =====================================================
st.markdown('<div class="section-title">Math Keyboard</div>', unsafe_allow_html=True)

left_keyboard, spacer_col, right_keyboard = st.columns([1.02, 0.045, 1.22], gap="small")

with left_keyboard:
    st.markdown('<div class="small-title">Basic</div>', unsafe_allow_html=True)

    basic_rows = [
        [
            ("x", "x", "append"),
            ("y", "y", "append"),
            ("π", "pi", "append"),
            ("e", "e", "append"),
            ("7", "7", "append"),
            ("8", "8", "append"),
            ("9", "9", "append"),
            ("×", " * ", "append"),
            ("÷", " / ", "append"),
        ],
        [
            ("x²", "x^2", "append"),
            ("y²", "y^2", "append"),
            ("□²", "^2", "append"),
            ("□ⁿ", "^", "append"),
            ("4", "4", "append"),
            ("5", "5", "append"),
            ("6", "6", "append"),
            ("+", " + ", "append"),
            ("−", " - ", "append"),
        ],
        [
            ("√", "sqrt(", "append"),
            ("| |", "abs(", "append"),
            ("(", "(", "append"),
            (")", ")", "append"),
            ("1", "1", "append"),
            ("2", "2", "append"),
            ("3", "3", "append"),
            ("a/b", "/", "append"),
            ("⌫", "", "backspace"),
        ],
        [
            (",", ",", "append"),
            (".", ".", "append"),
            ("0", "0", "append"),
            ("ln", "ln(", "append"),
            ("log", "log(", "append"),
            ("exp", "exp(", "append"),
            (")", ")", "append"),
            ("Clear", "", "clear"),
            ("=", "", "append"),
        ],
    ]

    for idx, row in enumerate(basic_rows):
        button_grid(row, cols_per_row=9, group_name=f"basic_row_{idx}")

with spacer_col:
    st.write("")

with right_keyboard:
    st.markdown('<div class="small-title">Functions</div>', unsafe_allow_html=True)

    function_rows = [
        [
            ("sin", "sin(", "append"),
            ("cos", "cos(", "append"),
            ("tan", "tan(", "append"),
            ("sec", "sec(", "append"),
            ("csc", "csc(", "append"),
            ("cot", "cot(", "append"),
        ],
        [
            ("sin⁻¹", "asin(", "append"),
            ("cos⁻¹", "acos(", "append"),
            ("tan⁻¹", "atan(", "append"),
            ("sinh", "sinh(", "append"),
            ("cosh", "cosh(", "append"),
            ("tanh", "tanh(", "append"),
        ],
        [
            ("log₁₀", "log10(", "append"),
            ("sqrt", "sqrt(", "append"),
            ("abs", "abs(", "append"),
            ("exp", "exp(", "append"),
            ("ln", "ln(", "append"),
            ("log", "log(", "append"),
        ],
    ]

    for idx, row in enumerate(function_rows):
        button_grid(row, cols_per_row=6, group_name=f"function_row_{idx}")

# =====================================================
# 11. Parameters and graph settings
# =====================================================
st.markdown("---")
st.markdown('<div class="section-title">Parameters and Graph Settings</div>', unsafe_allow_html=True)

param_col, graph_col, action_col = st.columns([1.1, 1.1, 0.85], gap="large")

with param_col:
    st.markdown("**Direction vector** $\\vec{u}=(u_1,u_2)$")

    u_col_1, u_col_2 = st.columns(2)

    with u_col_1:
        draft_u1 = st.number_input("u₁", value=1.0)

    with u_col_2:
        draft_u2 = st.number_input("u₂", value=1.0)

    st.markdown("**Point** $M_0=(x_0,y_0)$")

    p_col_1, p_col_2 = st.columns(2)

    with p_col_1:
        draft_x0 = st.number_input("x₀", value=1.0)

    with p_col_2:
        draft_y0 = st.number_input("y₀", value=2.0)

with graph_col:
    draft_radius = 3.00
    draft_grid_size = 80
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    draft_show_tangent_plane = st.checkbox("Show tangent plane", value=True)
    draft_show_direction_arrow = st.checkbox("Show tangent direction vector", value=True)

with action_col:
    st.write("")
    st.write("")

    visualize_clicked = st.button(
        "Visualize",
        type="primary",
        use_container_width=True,
        key="visualize_button"
    )

    if visualize_clicked:
        st.session_state.submitted_data = {
            "expr": st.session_state.draft_expr,
            "u1": draft_u1,
            "u2": draft_u2,
            "x0": draft_x0,
            "y0": draft_y0,
            "radius": draft_radius,
            "grid_size": draft_grid_size,
            "show_tangent_plane": draft_show_tangent_plane,
            "show_direction_arrow": draft_show_direction_arrow,
        }

    st.markdown(
        '<div class="compact-caption">Use this button to render the 3D graph.</div>',
        unsafe_allow_html=True
    )

# =====================================================
# 12. Stop before visualization
# =====================================================
if st.session_state.submitted_data is None:
    st.info("Enter a function and parameters, then press **Enter / Visualize** to generate the graph.")
    st.stop()

data_input = st.session_state.submitted_data

if st.session_state.draft_expr != data_input["expr"]:
    st.warning(
        "The formula above has changed, but the graph below still uses the last submitted expression. "
        "Press Enter / Visualize to update it."
    )

# =====================================================
# 13. Generate plot data
# =====================================================
try:
    with st.spinner("Calculating and generating graph..."):
        plot_data = generate_plot_data(
            data_input["expr"],
            data_input["u1"],
            data_input["u2"],
            data_input["x0"],
            data_input["y0"],
            data_input["radius"],
            data_input["grid_size"],
        )

except Exception:
    st.error("The submitted expression is incomplete or invalid, so the graph cannot be generated yet.")
    st.info("Please complete the expression, then press Enter / Visualize again.")
    st.stop()

# =====================================================
# 14. Calculation result
# =====================================================
st.markdown("---")
st.subheader("Calculation Result")

result_col_1, result_col_2 = st.columns([0.95, 1.35], gap="large")

with result_col_1:
    st.latex(r"f(x,y)=" + plot_data["f_expr_latex"])
    st.latex(r"f_x(x,y)=" + plot_data["fx_expr_latex"])
    st.latex(r"f_y(x,y)=" + plot_data["fy_expr_latex"])

with result_col_2:
    st.markdown("<b>Submitted function:</b>", unsafe_allow_html=True)
    st.markdown('<div class="submitted-formula-box">', unsafe_allow_html=True)
    st.latex(r"f(x,y)=" + plot_data["f_expr_latex"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="info-line">
            <b>Point</b> M<sub>0</sub> = ({format_number(data_input['x0'])}, {format_number(data_input['y0'])})
        </div>
        <div class="info-line">
            <b>Direction vector</b> u = ({format_number(data_input['u1'])}, {format_number(data_input['u2'])})
        </div>
        """,
        unsafe_allow_html=True
    )

    card_1, card_2, card_3 = st.columns([1.0, 1.25, 1.1], gap="small")

    with card_1:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">f(x₀, y₀)</div>
                <div class="result-value">{format_number(plot_data['z0'])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card_2:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">∇f(x₀, y₀)</div>
                <div class="result-value-small">
                    {format_pair(plot_data['fx0'], plot_data['fy0'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card_3:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Directional derivative</div>
                <div class="result-value">{format_number(plot_data['directional_derivative'])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="info-line" style="margin-top: 16px;">
            <b>Unit direction vector:</b>
            {format_pair(plot_data['unit_u_0'], plot_data['unit_u_1'])}
        </div>
        """,
        unsafe_allow_html=True
    )

    if plot_data["directional_derivative"] > 0:
        st.markdown(
            '<div class="success-box">The surface increases in the chosen direction.</div>',
            unsafe_allow_html=True
        )
    elif plot_data["directional_derivative"] < 0:
        st.markdown(
            '<div class="warning-box">The surface decreases in the chosen direction.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="neutral-box">The surface is locally flat in the chosen direction.</div>',
            unsafe_allow_html=True
        )

# =====================================================
# 15. Graphics View
# =====================================================
st.markdown("---")
st.subheader("Graphics View")

graph_tab_3d, graph_tab_2d = st.tabs(
    ["3D Surface View", "2D Direction View"]
)

with graph_tab_3d:
    fig3d = go.Figure()

    fig3d.add_trace(
        go.Surface(
            x=plot_data["X_grid"],
            y=plot_data["Y_grid"],
            z=plot_data["Z_grid"],
            opacity=0.78,
            colorscale="Viridis",
            showscale=False,
            name="Surface z = f(x, y)"
        )
    )

    if data_input["show_tangent_plane"]:
        fig3d.add_trace(
            go.Surface(
                x=plot_data["X_grid"],
                y=plot_data["Y_grid"],
                z=plot_data["Z_tangent_plane"],
                opacity=0.35,
                colorscale="Oranges",
                showscale=False,
                name="Tangent plane"
            )
        )

    fig3d.add_trace(
        go.Scatter3d(
            x=plot_data["X_curve"],
            y=plot_data["Y_curve"],
            z=plot_data["Z_curve"],
            mode="lines",
            line=dict(width=7),
            name="Direction curve on surface"
        )
    )

    fig3d.add_trace(
        go.Scatter3d(
            x=plot_data["X_curve"],
            y=plot_data["Y_curve"],
            z=plot_data["Z_tangent_line"],
            mode="lines",
            line=dict(width=5, dash="dash"),
            name="Tangent line"
        )
    )

    fig3d.add_trace(
        go.Scatter3d(
            x=[data_input["x0"]],
            y=[data_input["y0"]],
            z=[plot_data["z0"]],
            mode="markers+text",
            marker=dict(size=7),
            text=["M₀"],
            textposition="top center",
            name="Point M₀"
        )
    )

    if data_input["show_direction_arrow"]:
        arrow_length = data_input["radius"] * 0.45

        fig3d.add_trace(
            go.Cone(
                x=[data_input["x0"]],
                y=[data_input["y0"]],
                z=[plot_data["z0"]],
                u=[arrow_length * plot_data["unit_u_0"]],
                v=[arrow_length * plot_data["unit_u_1"]],
                w=[arrow_length * plot_data["directional_derivative"]],
                anchor="tail",
                sizemode="absolute",
                sizeref=0.4,
                name="Tangent direction vector",
                showscale=False
            )
        )

    fig3d.update_layout(
        height=760,
        title="Geometric Meaning of the Directional Derivative",
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="z",
            aspectmode="cube",
        ),
        margin=dict(l=0, r=0, t=45, b=0),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor="rgba(255,255,255,0.7)"
        )
    )

    st.plotly_chart(fig3d, use_container_width=True)

with graph_tab_2d:
    st.markdown(
        "This view shows the one-variable function obtained by moving from "
        "$M_0$ in the direction of $\\hat{u}$:"
    )

    st.latex(
        r"g(t)=f(x_0+t\hat{u}_1,\;y_0+t\hat{u}_2)"
    )

    st.markdown(
        "The slope of the tangent line at $t=0$ is the directional derivative."
    )

    fig2d = go.Figure()

    fig2d.add_trace(
        go.Scatter(
            x=plot_data["t_vals"],
            y=plot_data["Z_curve"],
            mode="lines",
            line=dict(width=4),
            name="g(t)=f(M₀+tû)"
        )
    )

    fig2d.add_trace(
        go.Scatter(
            x=plot_data["t_vals"],
            y=plot_data["Z_tangent_line"],
            mode="lines",
            line=dict(width=3, dash="dash"),
            name="Tangent line at t=0"
        )
    )

    fig2d.add_trace(
        go.Scatter(
            x=[0],
            y=[plot_data["z0"]],
            mode="markers+text",
            marker=dict(size=10),
            text=["t=0"],
            textposition="top center",
            name="M₀"
        )
    )

    fig2d.update_layout(
        height=520,
        title="Directional Derivative as the Slope of a Cross-section Curve",
        xaxis_title="t",
        yaxis_title="z",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig2d, use_container_width=True)