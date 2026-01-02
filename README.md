# Procz's Dimension Visualizer

This is a Python script that visualizes dimensions from 0D (Point) up to 10D (Hypercube) smoothly.

## How to Run

1.  Make sure you have Python installed.
2.  Run the script:
    ```
    python main.py
    ```

## Controls

-   **Space**: Pause/Resume animation.
-   **Up Arrow**: Increase dimension.
-   **Down Arrow**: Decrease dimension.
-   **R**: Reset to 0D.

## Concept

The visualization uses an orthographic projection of high-dimensional vertices onto the 2D screen.
As dimensions increase, new basis vectors are introduced. The transitions are interpolated to show the "extrusion" effect where the previous shape is duplicated and connected to form the higher-dimensional shape.
