import matplotlib.pyplot as plt

def draw_neural_network(ax, network_structure, layer_spacing=0.5, node_spacings=0.2,
                        node_color='white', edge_color='black', node_edge_color='black'):
    """Draw a neural network diagram with customizable spacing and colors.

    Parameters:
    - ax: matplotlib.axes.Axes object where the network will be drawn.
    - network_structure: dict mapping layer number to number of neurons (e.g., {1: 3, 2: 3, 3: 1}).
    - layer_spacing: float, controls horizontal spacing between layers.
    - node_spacings: float or list, controls vertical spacing between nodes.
        - If a single float is provided, it applies to all layers.
        - If a list is provided, spacings are applied to layers based on index.
        - Throws an error if more spacings are provided than layers.
        - If fewer spacings are provided than layers, the remaining layers use default spacing.
    - node_color: color of the nodes.
    - edge_color: color of the edges (connections).
    - node_edge_color: color of the node borders.
    """
    # Sort layers by layer number
    layer_numbers = sorted(network_structure.keys())
    layer_sizes = [network_structure[layer_num] for layer_num in layer_numbers]
    n_layers = len(layer_numbers)

    # Handle node_spacings
    default_spacing = 1.0  # Default spacing for layers without specified spacing
    if isinstance(node_spacings, (int, float)):
        node_spacings = [node_spacings] * n_layers
    else:
        if len(node_spacings) > n_layers:
            raise ValueError("Length of node_spacings cannot be greater than the number of layers.")
        elif len(node_spacings) < n_layers:
            # Extend node_spacings with default spacing for remaining layers
            node_spacings.extend([default_spacing] * (n_layers - len(node_spacings)))

    # Calculate horizontal positions of layers and center them
    total_width = (n_layers - 1) * layer_spacing
    h_positions = [i * layer_spacing - total_width / 2 for i in range(n_layers)]

    # Store vertical positions for each layer
    layer_v_positions = []
    max_heights = []

    # Calculate maximum vertical extent for centering
    for i, (layer_size, node_spacing) in enumerate(zip(layer_sizes, node_spacings)):
        layer_height = (layer_size - 1) * node_spacing
        max_heights.append(layer_height / 2)

    max_height = max(max_heights)

    # Draw nodes and connections
    for i, (layer_size, node_spacing) in enumerate(zip(layer_sizes, node_spacings)):
        layer_x = h_positions[i]
        # Center layers vertically
        layer_height = (layer_size - 1) * node_spacing
        y_center_offset = max_height - (layer_height / 2)
        # Vertical positions of nodes in this layer
        v_positions = [j * node_spacing + y_center_offset for j in range(layer_size)]
        layer_v_positions.append(v_positions)
        for j, layer_y in enumerate(v_positions):
            # Draw node
            circle = plt.Circle(
                (layer_x, layer_y),
                0.05,
                color=node_color,
                ec=node_edge_color,
                lw=1.5,
                zorder=4
            )
            ax.add_patch(circle)
            # Draw connections to previous layer
            if i > 0:
                prev_layer_x = h_positions[i - 1]
                prev_v_positions = layer_v_positions[i - 1]
                for prev_layer_y in prev_v_positions:
                    ax.plot(
                        [prev_layer_x, layer_x],
                        [prev_layer_y, layer_y],
                        color=edge_color,
                        lw=0.8,
                        zorder=1
                    )

    # Set plot limits to center the network
    x_margin = layer_spacing / 2
    y_margin = max_height + max(node_spacings)
    ax.set_xlim(-total_width / 2 - x_margin, total_width / 2 + x_margin)
    ax.set_ylim(-y_margin, 2 * max_height + y_margin)
    
    