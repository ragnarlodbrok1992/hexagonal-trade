// Global imports
#import "Basic";
#import "Window_Creation";
#import "Input";

// Named imports
getrect :: #import "GetRect";

// Engine constants
BAR_TITLE :: "Hexagonal Trade Engine";
WINDOW_WIDTH :: 800;
WINDOW_HEIGHT :: 600;
ENGINE_RUNNING := true;

// Main entry function
main :: () {
  print("Hexagonal Trade engine.\n");
  defer print("Exiting...\n");

  // Window creation
  window := create_window(WINDOW_WIDTH, WINDOW_HEIGHT, BAR_TITLE);

  while ENGINE_RUNNING {
    // Start of frame
    reset_temporary_storage();
    update_window_events();

    for events_this_frame {
      getrect.getrect_handle_event(it);

      if it.type == {
        case .QUIT;
          ENGINE_RUNNING = false;
        case .KEYBOARD;
          if it.key_code == .ESCAPE {
            ENGINE_RUNNING = false;
          }
      }
    }
  }
}

