# Global imports
import glfw
import glm

# Global named imports
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Local imports
from entities.cube.cube import cube_vertices, cube_indices
from entities.triangle.triangle import triangle_vertices, triangle_indices

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Vertex shader
VERTEX_SHADER_SOURCE = """
# version 330 core

layout (location = 0) in vec3 aPos;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
  gl_Position = projection * view * model * vec4(aPos, 1.0);
}
"""

# Fragment shader
FRAGMENT_SHADER_SOURCE = """
# version 330 core

out vec4 FragColor;

void main()
{
  FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
"""

# Callback functions
def mouse_callback(window, xpos, ypos):
    print(f"Mouse moved - xpos: {xpos}, ypos: {ypos}")

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def framebuffer_size_callback(window, width, height):
    print(f"Framebuffer size - width: {width}, height: {height}")


def main():
    global delta_time, last_frame, camera_pos, camera_front, camera_up, yaw, pitch, first_mouse

    # Global first frame defines
    camera_pos = glm.vec3(0.0, 0.0, 3.0)
    camera_front = glm.vec3(0.0, 0.0, -1.0)
    camera_up = glm.vec3(0.0, 1.0, 0.0)

    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Hexagonal Trade", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    # glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    # glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)

     # Compile shaders and link program
    shader = compileProgram(
        compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
    )

    # Create VBO and VAO
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 4 * len(cube_vertices), (GLfloat * len(cube_vertices))(*cube_vertices), GL_STATIC_DRAW)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(0))

    # Element buffer object (EBO)
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(cube_indices), (GLuint * len(cube_indices))(*cube_indices), GL_STATIC_DRAW)

    # Uniforms - MVP
    model_loc = glGetUniformLocation(shader, "model")
    view_loc = glGetUniformLocation(shader, "view")
    projection_loc = glGetUniformLocation(shader, "projection")

    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Use shader program
        glUseProgram(shader)

        # Set up view and projection matrices
        view_matrix = glm.lookAt(camera_pos, camera_pos + camera_front, camera_up)
        projection_matrix = glm.perspective(glm.radians(45), WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)

        # Push data into uniforms
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view_matrix))
        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection_matrix))

        # Draw cube
        for i in range(10):
            model_matrix = glm.mat4(1.0)
            # model_matrix = glm.translate(model_matrix, glm.vec3(1.0 * i, 0.0, 0.0))

            glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model_matrix))

            glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    # Last engine call
    glfw.terminate()

if __name__ == "__main__":
    print("Hexagonal Trade")

    first_mouse = True
    main()

    print("Goodbye!")

