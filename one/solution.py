def main():
    first = []
    second = []
    with open("input.txt", "r") as f:
        for line in f:
            nums = line.strip().split()
            first.append(int(nums[0]))
            second.append(int(nums[1]))


    first.sort()
    second.sort()

    part_one = 0
    for i, each in enumerate(first):
        dist = abs(each-second[i])
        part_one += dist
        i += 1

    print(f"{part_one=}")

    part_two = 0
    for each in first:
        part_two += each * second.count(each)

    print(f"{part_two=}")

if __name__ == "__main__":
    main()
