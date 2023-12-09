// Global imports
#import "Basic";
#import "Window_Creation";
#import "GL";
#import "String";
#import "Input";
#import "System";

// Named imports
Simp    :: #import "Simp";
GetRect :: #import "GetRect";

// Local imports
#load "shaders.jai";
#load "entities/triangle.jai";

// Engine constants
BAR_TITLE :: "Hexagonal Trade Engine";
WINDOW_WIDTH :: 800;
WINDOW_HEIGHT :: 600;
ENGINE_RUNNING := true;


// Main entry function
main :: () {
  print("Hexagonal Trade engine.\n");
  defer print("Exiting...\n");

  // Some window stuf
  #if OS == .WINDOWS
  {
    win32 :: #import "Windows";
    win32.SetProcessDPIAware();
  }

  // Working directory
  executable_path := path_strip_filename(get_path_of_running_executable());
  set_working_directory(executable_path);

  // Window creation
  window := create_window(WINDOW_WIDTH, WINDOW_HEIGHT, BAR_TITLE);

  // Render target for simp
  // @TODO(ragnar): It doesn't work for me
  Simp.set_render_target(window);

  // Loading shaders and stuff
  default_shader_program := load_shaders();

  // DEBUG STUFF
  // Debug triangle
  triangle : DebugTriangle;

  #if 0
    print("Default shader program: %\n", default_shader_program);
  #if 1 {
    print("Triangle vertices and colors: %\n", triangle.TRIANGLE_VERTICES_AND_COLORS);
    print("Triangle indices:             %\n", triangle.TRIANGLE_INDICES);
  }

  while ENGINE_RUNNING {
    // Start of frame
    reset_temporary_storage();
    update_window_events();

    // Updating events
    for events_this_frame {
      GetRect.getrect_handle_event(it);

      if it.type == {
        case .QUIT;
          ENGINE_RUNNING = false;
        case .KEYBOARD;
          if it.key_code == .ESCAPE {
            ENGINE_RUNNING = false;
          }
      }
    }
    // End of updating events

    // Graphics Library stuff
    glDepthMask(GL_TRUE);
    glEnable(GL_DEPTH_TEST);

    // Clearing the screen
    Simp.update_window(window);
    Simp.clear_render_target(0.2, 0.2, 0.3, 1);

    // Swapping buffers
    Simp.swap_buffers(window);
  }
}

