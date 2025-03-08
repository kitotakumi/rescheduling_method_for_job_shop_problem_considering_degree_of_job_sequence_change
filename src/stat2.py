import csv
import numpy as np
import os
import main_stability_scheduling


def main():
    index = 100
    data = [
        ["makespan", "stability", "changed_sum", "distance_mean","distance_sum", "changed_first", "changed_secound", "changed_third", "changed_4th", "changed_5th", "changed_6th", "changed_7th", "changed_8th", "changed_9th", "changed_10th"]
    ]  # fmt:skip
    special_data = [
        ["makespan", "stability", "changed_sum", "distance_mean","distance_sum", "changed_first", "changed_secound", "changed_third", "changed_4th", "changed_5th", "changed_6th", "changed_7th", "changed_8th", "changed_9th", "changed_10th"]
    ]  # fmt:skip
    count = 0
    sum = 0
    while sum < index:
        row = main_stability_scheduling.main()
        row = [row[0]] + list(row[1])
        if row[0] == 1080 and row[2] == 3:
            row = [1079, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        data.append(list(row))
        if row[0] != 1079 and row[1] != 3:
            special_data.append(list(row))
            count += 1
        sum += 1

    data.append(list(np.mean(data[1:], axis=0)))
    print("統計値", np.mean(data[1:], axis=0))
    data.append(list(np.mean(special_data[1:], axis=0)))

    with open("output_x=0_2_v2_rankdiff.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("収束確率", (sum - count) / sum)
    print("収束回数", sum - count)
    print("非収束回数", count)
    print("収束を除いた統計値", np.mean(special_data[1:], axis=0))


if __name__ == "__main__":
    main()
