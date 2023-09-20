# Sway WM: The Godot Language Server does not work 
# if Godot is not on an active workspace...

# Exec Flags for the Godot editor
# --server ./godothost --remote-send "<C-\><C-N>:n {file}<CR>{line}G{col}|"
nvim --listen ./godothost
