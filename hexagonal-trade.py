# Global imports
import glfw
import glm

# Global named imports
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Local imports
from entities.cube.cube import cube_vertices, cube_indices
from entities.triangle.triangle import triangle_vertices, triangle_indices
from entities.camera.camera import Camera, camera_pos, camera_front, camera_up
from entities.camera.camera import CAM_MOV_UP, CAM_MOV_DOWN, CAM_MOV_LEFT, CAM_MOV_RIGHT, CAM_MOV_FRONT, CAM_MOV_BACK

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Global initializations
LAST_MOUSE_XPOS = 0.0
LAST_MOUSE_YPOS = 0.0

SPACE_KEY_PRESSED = False

# Vertex shader
VERTEX_SHADER_SOURCE = """
# version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
  gl_Position = projection * view * model * vec4(aPos, 1.0);
  ourColor = aColor;
}
"""

# Fragment shader
FRAGMENT_SHADER_SOURCE = """
# version 330 core

in vec3 ourColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(ourColor, 1.0f);
}
"""

# Callback functions
def mouse_callback(window, xpos, ypos):
    global LAST_MOUSE_XPOS, LAST_MOUSE_YPOS
    global SPACE_KEY_PRESSED
    global camera_front

    # Calculate xpos and ypos difference
    x_diff = xpos - LAST_MOUSE_XPOS
    y_diff = ypos - LAST_MOUSE_YPOS

    # Update last xpos and ypos
    LAST_MOUSE_XPOS = xpos
    LAST_MOUSE_YPOS = ypos

    if SPACE_KEY_PRESSED:
        camera_front = Camera.rotate_yaw(camera_front, x_diff)
        camera_front = Camera.rotate_pitch(camera_front, y_diff)

def key_callback(window, key, scancode, action, mods):
    global SPACE_KEY_PRESSED
    global camera_pos, camera_front, camera_up
    global CAM_MOV_UP, CAM_MOV_DOWN, CAM_MOV_LEFT, CAM_MOV_RIGHT, CAM_MOV_FRONT, CAM_MOV_BACK

    # Engine exit
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    # Camera controls - rotation
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        SPACE_KEY_PRESSED = True
    if key == glfw.KEY_SPACE and action == glfw.RELEASE:
        SPACE_KEY_PRESSED = False

    # Camera controls - WASD
    if key == glfw.KEY_W and action == glfw.PRESS:
        CAM_MOV_UP = True
    elif key == glfw.KEY_S and action == glfw.PRESS:
        CAM_MOV_DOWN = True
    elif key == glfw.KEY_A and action == glfw.PRESS:
        CAM_MOV_LEFT = True
    elif key == glfw.KEY_D and action == glfw.PRESS:
        CAM_MOV_RIGHT = True
    elif key == glfw.KEY_Q and action == glfw.PRESS:
        CAM_MOV_FRONT = True
    elif key == glfw.KEY_E and action == glfw.PRESS:
        CAM_MOV_BACK = True

    if key == glfw.KEY_W and action == glfw.RELEASE:
        CAM_MOV_UP = False
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        CAM_MOV_DOWN = False
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        CAM_MOV_LEFT = False
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        CAM_MOV_RIGHT = False
    elif key == glfw.KEY_Q and action == glfw.RELEASE:
        CAM_MOV_FRONT = False
    elif key == glfw.KEY_E and action == glfw.RELEASE:
        CAM_MOV_BACK = False

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def main():
    global delta_time, last_frame, camera_pos, camera_front, camera_up, yaw, pitch, first_mouse
    global CAM_MOV_UP, CAM_MOV_DOWN, CAM_MOV_LEFT, CAM_MOV_RIGHT

    # Initialize the library
    if not glfw.init():
        return

    # Configure GLFW
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Hexagonal Trade", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    # GL depth testing
    glEnable(GL_DEPTH_TEST)

    # VSYNC
    glfw.swap_interval(1)

     # Compile shaders and link program
    shader = compileProgram(
        compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER),
        validate=True
    )

    # Create VBO and VAO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    # Vertex array object (VAO)
    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube_vertices.nbytes, cube_vertices, GL_STATIC_DRAW)

    # Element buffer object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)


    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)

    # Unbind VAO
    glBindVertexArray(0)

    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Camera movement
        Camera.camera_movement(camera_front, CAM_MOV_UP, CAM_MOV_DOWN, CAM_MOV_LEFT, CAM_MOV_RIGHT, CAM_MOV_FRONT, CAM_MOV_BACK)

        # Render here, e.g. using pyOpenGL
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Use shader program
        glUseProgram(shader)

        # Set up view and projection matrices
        model_matrix = glm.mat4(1.0)
        view_matrix = glm.lookAt(camera_pos, camera_pos + camera_front, camera_up)
        # view_matrix = glm.lookAt(glm.vec3(1, 1, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        projection_matrix = glm.perspective(glm.radians(45.0), WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)

        # Uniforms - MVP
        model_loc = glGetUniformLocation(shader, "model")
        view_loc = glGetUniformLocation(shader, "view")
        projection_loc = glGetUniformLocation(shader, "projection")

        # Set uniforms
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model_matrix))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view_matrix))
        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection_matrix))

        # Draw cube
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    # Last engine call
    glfw.terminate()

    # Clean up
    # glDeleteVertexArrays(1, [VAO])
    # glDeleteBuffers(1, [VBO, EBO])
    # glDeleteProgram(shader)

if __name__ == "__main__":
    print("Hexagonal Trade")

    first_mouse = True
    main()

    print("Goodbye!")

