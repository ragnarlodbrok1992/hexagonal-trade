#import "Basic";
#import "Compiler";

// Main build function
build :: () {
  // Taken from basic metaprogram
  w := compiler_create_workspace("Target Program");
  if !w {
    print("Workspace creation failed.\n");
    return;
  }

  target_options := get_build_options(w);
  target_options.output_executable_name = "hexagonal-trade";
  set_build_options(target_options, w);

  compiler_begin_intercept(w);

  add_build_file(tprint("%/src/main.jai", #filepath), w);

  message_loop();

  compiler_end_intercept(w);

  print("Build complete.\n");

  set_build_options_dc(.{do_output=false});

}

// Message loop function
message_loop :: () {

  while true {
    message := compiler_wait_for_message();

    // Switching between message kinds
    if message.kind == {
      case .FILE;
        message_file := cast(*Message_File) message;
        print("  Loading file: %\n", message_file.fully_pathed_filename);
      case .IMPORT;
        import := cast(*Message_Import) message;
        print("  Importing module: %\n", import.module_name);
      case .TYPECHECKED;
        // print("  Typechecked: \n");
      case .PHASE;
        phase := cast(*Message_Phase) message;
        print("<--- Entering phase: %\n", phase.phase);

        if phase.phase == .POST_WRITE_EXECUTABLE {
          print("\n");
          if phase.executable_write_failed {
            print("FAILED writing '%' ! Linker exit code was %.\n", phase.executable_name, phase.linker_exit_code);
          } else {
            print("Success writing '%' ! Linker exit code was %.\n", phase.executable_name, phase.linker_exit_code);
          }
        }
      case .COMPLETE;
        print("  Complete: \n");
      case .ERROR;
        // @TODO(ragnar): Handle error messages from compiler
        print("  Error: \n");
      case;
        compiler_report(tprint("Unhandled message kind: %\n", message.kind));
    }
  }

}

// Main build function - running
#run build();

