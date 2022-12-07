def get_data(file:str):
    with open("./puzzles/day_08/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            print(line.strip())

def main():
    get_data("part_1_data_example.txt")
    
if __name__ == "__main__":
    main()