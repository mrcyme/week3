from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import random

def generate_parametric_svg(small_square_width, small_square_spacing, large_square_spacing, N, M):
    # Calculate the total width and height needed for the small squares including their spacing
    total_small_squares_width = N * small_square_width + (N - 1) * small_square_spacing
    total_small_squares_height = M * small_square_width + (M - 1) * small_square_spacing
    
    # Adjust SVG dimensions to include the large square spacing
    svg_width = total_small_squares_width + 2 * large_square_spacing
    svg_height = total_small_squares_height + 2 * large_square_spacing

    # Create the SVG element
    svg = Element('svg', width=str(svg_width), height=str(svg_height), xmlns="http://www.w3.org/2000/svg")

    # Generate the large square, offset from the small squares by large_square_spacing
    big_square = SubElement(svg, 'rect', 
                            x=str(large_square_spacing - large_square_spacing), 
                            y=str(large_square_spacing - large_square_spacing),
                            width=str(total_small_squares_width + 2 * large_square_spacing), 
                            height=str(total_small_squares_height + 2 * large_square_spacing),
                            fill="none", stroke="black")

    # Generate the array of small squares without fill, starting from the large_square_spacing
    for row in range(M):
        for col in range(N):
            x = large_square_spacing + col * (small_square_width + small_square_spacing)
            y = large_square_spacing + row * (small_square_width + small_square_spacing)
            SubElement(svg, 'rect', x=str(x), y=str(y), width=str(small_square_width),
                       height=str(small_square_width), fill="none", stroke="#{:06x}".format(random.randint(0, 0xFFFFFF)))

    # Convert to a prettified (indented) string
    rough_string = tostring(svg, 'utf-8')
    reparsed = parseString(rough_string)
    svg_pretty = reparsed.toprettyxml(indent="  ")

    return svg_pretty

# Example parameters
small_square_width = 40
small_square_spacing = 10
large_square_spacing = 20
N = 10  # Number of square columns
M = 10  # Number of square rows

# Generate SVG content
svg_content = generate_parametric_svg(small_square_width, small_square_spacing, large_square_spacing, N, M)

# For demonstration purposes, here's how you might output or save the SVG content
print(svg_content)


# This is how you would save the SVG content to a file (adjust the path/to/save


# Example of saving the SVG content to a file (not executable here)
with open('./squares_with_spacing.svg', 'w') as file:
     file.write(svg_content)

# Print or return svg_content as needed
