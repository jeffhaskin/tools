"""Simple 3D visualization of the file system using Panda3D."""

import os
import subprocess
from pathlib import Path

from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    AmbientLight,
    DirectionalLight,
    NodePath,
    TextNode,
    CollisionTraverser,
    CollisionHandlerQueue,
    CollisionNode,
)
from direct.gui.OnscreenText import OnscreenText


class FileFantasyGame(ShowBase):
    """Visualize the file system as a library of rooms and books."""

    def __init__(self, start_path: str | None = None):
        super().__init__()
        self.disableMouse()  # use custom camera controls
        self.start_path = Path(start_path or os.getcwd())
        self.current_path = self.start_path
        self.title = OnscreenText(
            text=str(self.current_path),
            pos=(0, 0.9),
            scale=0.07,
            align=TextNode.ACenter,
            mayChange=True,
        )
        self.setup_lights()
        self.load_room(self.current_path)
        self.accept("escape", self.userExit)

    def setup_lights(self):
        """Create simple ambient and directional lighting."""
        ambient = AmbientLight("ambient")
        ambient.setColor((0.4, 0.4, 0.4, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        directional = DirectionalLight("directional")
        directional.setColor((0.8, 0.8, 0.8, 1))
        directional_np = self.render.attachNewNode(directional)
        directional_np.setHpr(-45, -45, 0)
        self.render.setLight(directional_np)

    def clear_room(self):
        """Remove existing room objects."""
        if hasattr(self, "room"):
            self.room.removeNode()
        self.room = NodePath("room")
        self.room.reparentTo(self.render)

    def load_room(self, path: Path):
        """Create a simple room representing a directory."""
        self.clear_room()
        self.title.setText(str(path))
        # Floor
        cm = self.loader.loadModel("models/box")
        floor = cm.copyTo(self.room)
        floor.setScale(10, 10, 0.1)
        floor.setPos(0, 0, -0.1)

        # Books for files
        for i, file in enumerate(sorted(p for p in path.iterdir() if p.is_file())):
            book = cm.copyTo(self.room)
            book.setScale(0.2, 0.5, 0.6)
            book.setPos(-4 + (i % 8) * 1, 2 + (i // 8) * 1.2, 0.3)
            book.setColor(0.6, 0.2, 0.2, 1)
            book.setTag("filepath", str(file))

        # Doors for subdirectories
        for i, sub in enumerate(sorted(p for p in path.iterdir() if p.is_dir())):
            door = cm.copyTo(self.room)
            door.setScale(1, 0.2, 2)
            door.setPos(-8 + i * 4, -4, 1)
            door.setColor(0.2, 0.2, 0.6, 1)
            door.setTag("dirpath", str(sub))

        # Simple picking with mouse click
        self.accept("mouse1", self.on_click)

    def on_click(self):
        if not self.mouseWatcherNode.hasMouse():
            return
        mpos = self.mouseWatcherNode.getMouse()
        picker_ray = self.camLens.makePickRay(mpos.getX(), mpos.getY())
        traverser = self.cTrav
        if traverser is None:
            self.cTrav = traverser = CollisionTraverser()
            self.picker = CollisionHandlerQueue()
            self.picker_node = CollisionNode('mouseRay')
            self.pickerNP = self.camera.attachNewNode(self.picker_node)
            traverser.addCollider(self.pickerNP, self.picker)
        self.picker_node.clearSolids()
        self.picker_node.addSolid(picker_ray)
        traverser.traverse(self.render)
        if self.picker.getNumEntries() > 0:
            self.picker.sortEntries()
            picked = self.picker.getEntry(0).getIntoNodePath()
            if picked.hasTag("dirpath"):
                self.current_path = Path(picked.getTag("dirpath"))
                self.load_room(self.current_path)
            elif picked.hasTag("filepath"):
                self.edit_file(Path(picked.getTag("filepath")))

    def edit_file(self, path: Path):
        """Open the file in the default system text editor."""
        try:
            subprocess.call([os.environ.get("EDITOR", "nano"), str(path)])
        except FileNotFoundError:
            print("No editor found. Set the EDITOR environment variable.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Navigate the file system in 3D")
    parser.add_argument("start", nargs="?", default=os.getcwd(), help="Starting directory")
    args = parser.parse_args()
    app = FileFantasyGame(args.start)
    app.run()


if __name__ == "__main__":
    main()
