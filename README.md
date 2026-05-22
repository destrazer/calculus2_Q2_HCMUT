# calculus2_Q2_HCMUT
The code for answering the question 2 in calculus 2 from HK252-MT1005-CC04

This project is a Streamlit application for calculating and visualizing the directional derivative of a two-variable function $f(x, y)$. The application also can display the geometric meaning of the directional derivative through interactive 3D and 2D graphs.

## 1. What This Application Can Do

- Evaluate the function value $f(x_0,y_0)$ at a selected point.
- Calculate the directional derivative:

$$D_{\vec{u}}f(x_0,y_0)=\nabla f(x_0,y_0)\cdot \hat{u}$$

- Show whether the surface increases, decreases, or remains locally flat in the chosen direction.
- Visualize the surface $z=f(x,y)$ in 3D.
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

## 3. How to Run the Program

### 3.1 Clone the Repository

Open the terminal and run the following command:

```bash
git clone https://github.com/nhnk21/calculus2_Q2_HCMUT.git
```

After the repository is downloaded, move into the project folder:

```bash
cd calculus2_Q2_HCMUT
```

If you have already downloaded or cloned the repository, you can skip this step and open
the project folder directly.

### 3.2 Install Required Libraries

The required Python libraries are listed in the `requirements.txt` file.

To install all dependencies automatically, run:

```bash
pip install -r requirements.txt
```

This command installs the libraries needed to run the application, including Streamlit,
SymPy, NumPy, Plotly, and streamlit-keyup.

### 3.3 Run the Application Locally

After installing the required libraries, run the Streamlit application with:

```bash
streamlit run calculus2-Q2.py
```

If the command runs successfully, Streamlit will start a local server and open the
application in your browser.

The local address is usually:

```txt
http://localhost:8501
```

If the browser does not open automatically, copy this address and paste it into your
browser manually.

### 3.4 Use the Application

After opening the application, users can:

1. Enter a two-variable function $f(x,y)$.

   Example:

   ```txt
   x^2 + y^2
   ```

2. Change the direction vector $\vec{u}=(u_1,u_2)$. By default, the direction vector is
   set to $(1,1)$.

   Example:

   ```txt
   u = (6, 5)
   ```

3. Enter the point $M_0=(x_0,y_0)$, where the directional derivative is evaluated.

   Example:

   ```txt
   M0 = (1, 2)
   ```

4. Choose whether to display the tangent plane and the tangent direction vector.

5. Click the `Visualize` button.

The application will then show:

- the submitted function,
- the partial derivatives,
- the value of the function at the selected point,
- the gradient vector,
- the unit direction vector,
- the directional derivative,
- a short interpretation of the result,
- a 3D graph of the surface,
- the tangent plane,
- the direction curve on the surface,
- and a 2D cross-section graph.

## 4. Example

For example, if the input function is:

```txt
x^2 + y^2
```

with:

```txt
M0 = (1, 2)
u = (1, 1)
```

The application calculates:

$$f_x(x,y)=2x$$

$$f_y(x,y)=2y$$

At $M_0=(1,2)$, the gradient vector is:

$$
\nabla f(1,2)=(2,4)
$$

The direction vector $(1,1)$ is normalized to:

$$
\hat{u} = \left( \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}} \right)
$$

Then the directional derivative is calculated by:

$$
D_{\vec{u}}f(1,2) = \nabla f(1,2)\cdot \hat{u}
$$

If the result is positive, the surface increases in the chosen direction.  
If the result is negative, the surface decreases in the chosen direction.  
If the result is zero, the surface is locally flat in that direction.

