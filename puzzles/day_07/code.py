from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from typing import List, Optional


@dataclass
class File:
    name: str
    size: int


@dataclass
class Dir:
    name: str = "/"
    dirs: Optional[List[Dir]] = None
    files: Optional[List[File]] = None
    parent_dir: Optional[Dir] = None

    def add_file(self, file: File) -> None:
        if self.files:
            self.files.append(file)
        else:
            self.files = [file]

    def add_dir(self, dir: Dir) -> None:
        dir.parent_dir = self
        if self.dirs:
            self.dirs.append(dir)
        else:
            self.dirs = [dir]

    def move_down(self, dir_name: str) -> Dir:
        dir = [dir for dir in self.dirs if dir.name == dir_name][0]
        return dir

    def move_up(self) -> Dir:
        return self.parent_dir

    @property
    def size(self) -> int:
        total_size = 0
        if self.files:
            for file in self.files:
                total_size += file.size
        if self.dirs:
            for dir in self.dirs:
                total_size += dir.size
        return total_size

    @property
    def full_name(self):
        if self.parent_dir:
            full_name = self.parent_dir.full_name + " > " + self.name
        else:
            full_name = self.name
        return full_name

    @property
    def size_counter(self):
        counter = Counter()
        counter[self.full_name] = self.size
        if self.dirs:
            for dir in self.dirs:
                counter += dir.size_counter
        return counter


def get_complete_dir_from_file(file: str) -> Dir:

    root_dir = Dir()

    with open("./puzzles/day_07/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            prompt = line.strip()
            if prompt == "$ cd /":
                current_dir = root_dir
            elif prompt == "$ cd ..":
                current_dir = current_dir.move_up()
            elif prompt.startswith("$ cd "):
                current_dir = current_dir.move_down(prompt[5:])
            elif prompt == "$ ls":
                pass
            elif prompt.startswith("dir "):
                current_dir.add_dir(Dir(prompt[4:]))
            else:
                file_info = prompt.split(" ")
                current_dir.add_file(File(file_info[1], int(file_info[0])))

    return root_dir


def main():
    root_dir = get_complete_dir_from_file("part_1_data.txt")
    size_counter = root_dir.size_counter

    # Part 1
    limited_sizes = [size for size in size_counter.values() if size <= 100_000]
    print(sum(limited_sizes))

    # Part 2
    free_volume = 70_000_000 - root_dir.size
    min_volume_to_delete = 30_000_000 - free_volume
    dirs_in_consideration = {
        name: size
        for (name, size) in size_counter.items()
        if size >= min_volume_to_delete
    }
    min_dir = min(dirs_in_consideration, key=dirs_in_consideration.get)
    print(min_dir, dirs_in_consideration[min_dir])


if __name__ == "__main__":
    main()
