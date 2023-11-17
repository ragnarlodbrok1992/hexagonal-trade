import numpy as np
from OpenGL.GL import *
import glfw
from glm import *

# Shader source code
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 ourColor;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    ourColor = aColor;
}
"""

fragment_shader_source = """
#version 330 core

in vec3 ourColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(ourColor, 1.0f);
}
"""

# Cube data
vertices = np.array([
    # Positions        # Colors
    -0.5, -0.5, -0.5,   1.0, 0.0, 0.0,
     0.5, -0.5, -0.5,   0.0, 1.0, 0.0,
     0.5,  0.5, -0.5,   0.0, 0.0, 1.0,
    -0.5,  0.5, -0.5,   1.0, 1.0, 0.0,
    -0.5, -0.5,  0.5,   1.0, 0.0, 1.0,
     0.5, -0.5,  0.5,   0.0, 1.0, 1.0,
     0.5,  0.5,  0.5,   1.0, 1.0, 1.0,
    -0.5,  0.5,  0.5,   0.5, 0.5, 0.5,
], dtype=np.float32)

indices = np.array([
    0, 1, 2, 2, 3, 0,
    4, 5, 6, 6, 7, 4,
    0, 4, 7, 7, 3, 0,
    1, 5, 6, 6, 2, 1,
    0, 1, 5, 5, 4, 0,
    2, 3, 7, 7, 6, 2,
], dtype=np.uint32)

# Callback functions
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

# Initialize glfw
if not glfw.init():
    raise Exception("glfw initialization failed")

# Configure glfw
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "Colored Cube", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window creation failed")

# Make the window's context current
glfw.make_context_current(window)
glfw.set_key_callback(window, key_callback)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Compile shaders
shader_program = glCreateProgram()
vertex_shader = glCreateShader(GL_VERTEX_SHADER)
fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

glShaderSource(vertex_shader, vertex_shader_source)
glCompileShader(vertex_shader)
if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
    raise Exception("Vertex shader compilation failed: " + glGetShaderInfoLog(vertex_shader).decode())

glShaderSource(fragment_shader, fragment_shader_source)
glCompileShader(fragment_shader)
if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
    raise Exception("Fragment shader compilation failed: " + glGetShaderInfoLog(fragment_shader).decode())

glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)
if not glGetProgramiv(shader_program, GL_LINK_STATUS):
    raise Exception("Shader program linking failed: " + glGetProgramInfoLog(shader_program).decode())

glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)

# Create VAO, VBO, and EBO
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
ebo = glGenBuffers(1)

glBindVertexArray(vao)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# Position attribute
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

# Color attribute
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
glEnableVertexAttribArray(1)

# Unbind VAO
glBindVertexArray(0)

# Main loop
while not glfw.window_should_close(window):
    # Poll for and process events
    glfw.poll_events()

    # Clear the color and depth buffers
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Use the shader program
    glUseProgram(shader_program)

    # Set the model, view, and projection matrices
    model = mat4(1.0)
    view = lookAt(vec3(1, 1, 3), vec3(0, 0, 0), vec3(0, 1, 0))
    projection = perspective(radians(45.0), 800 / 600, 0.1, 100.0)

    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "view")
    projection_loc = glGetUniformLocation(shader_program, "projection")

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, value_ptr(model))
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, value_ptr(view))
    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, value_ptr(projection))

    # Draw the cube
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    # Swap front and back buffers
    glfw.swap_buffers(window)

# Clean up
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo, ebo])
glDeleteProgram(shader_program)

# Terminate glfw
glfw.terminate()
