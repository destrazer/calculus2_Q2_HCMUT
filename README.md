# calculus2_Q2_HCMUT
the source code for answering the question 2 in calculus 2 from HK252-MT1005-CC04

The project is a Streamlit application for calculating and visualizing the directional derivative of a two-variable function \(f(x, y)\). Instead of only showing the final numerical result, the application also displays the geometric meaning of the directional derivative through interactive 3D and 2D graphs.

## 1. What This Application Can Do

This application can:

- Calculate the partial derivatives \(f_x(x,y)\) and \(f_y(x,y)\).
- Evaluate the function value \(f(x_0,y_0)\) at a selected point.
- Compute the gradient vector \(\nabla f(x_0,y_0)\).
- Normalize the direction vector \(\vec{u}=(u_1,u_2)\).
- Calculate the directional derivative:

\[
D_{\vec{u}}f(x_0,y_0)=\nabla f(x_0,y_0)\cdot \hat{u}
\]

- Show whether the surface increases, decreases, or remains locally flat in the chosen direction.
- Visualize the surface \(z=f(x,y)\) in 3D.
- Display the tangent plane at the selected point.
- Show the direction curve on the surface.
- Display the tangent line whose slope represents the directional derivative.
- Provide a 2D cross-section view to explain the directional derivative as the slope of a one-variable curve.

## 2. Libraries Used

The project uses the following Python libraries:

| Library | Purpose |
|---|---|
| `streamlit` | Builds and runs the interactive web application |
| `sympy` | Parses mathematical expressions and calculates symbolic derivatives |
| `numpy` | Handles numerical computation, vector operations, and grid generation |
| `plotly` | Creates interactive 3D and 2D graphs |
| `streamlit-keyup` | Supports real-time input behavior in Streamlit |

The following Python libraries are also imported in the source code, but they are built-in libraries and do not need to be installed separately:

| Library | Purpose |
|---|---|
| `math` | Handles basic mathematical operations |
| `html` | Escapes text safely when displaying invalid expressions |

## 3. Requirements

Create a file named `requirements.txt` in the project folder with the following content:

```txt
streamlit
sympy
numpy
plotly
streamlit-keyup