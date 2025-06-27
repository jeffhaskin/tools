# File Fantasy

File Fantasy is a prototype 3D game that visualizes the host file system as a fantasy library.
Every directory becomes a room with doors leading to subdirectories and bookshelves representing
files. Books can be picked up and edited using the system's text editor.

## Features

- Navigate directories as rooms connected by doors.
- View files as books on shelves.
- Edit file contents by placing a book on the drafting table.
- Simple lighting (ambient and directional) to enhance depth perception.

## Requirements

File Fantasy uses [Panda3D](https://www.panda3d.org/). Install it with:

```bash
pip install panda3d
```

## Running

```bash
python -m file_fantasy.game /path/to/start/directory
```

By default the game starts in the current working directory.
