from __future__ import annotations

from functools import total_ordering
from typing import List, Tuple, Optional


def get_data(file: str):
    with open("./puzzles/day_15/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_clean_string(data: str) -> str:
    return (
        data.replace("Sensor at ", "")
        .replace(" closest beacon is at ", "")
        .replace("x=", "")
        .replace(" y=", "")
    )


def get_sensor_data(data: str) -> Tuple[Vector, Vector]:
    sensor_with_beacon = []
    clean_string = get_clean_string(data)
    for sensor_beacon_string in clean_string.split(":"):
        sensor_beacon_data = []
        for sensor_beacon_coord in sensor_beacon_string.split(","):
            sensor_beacon_data.append(int(sensor_beacon_coord))
        sensor_with_beacon.append(Vector(*sensor_beacon_data))
    return tuple(sensor_with_beacon)


def get_sensors_beacons(file: str) -> Tuple[List[Vector], List[Vector]]:
    sensors = []
    beacons = []
    for data in get_data(file):
        sensor, beacon = get_sensor_data(data)
        sensors.append(sensor)
        beacons.append(beacon)
    return sensors, beacons


@total_ordering
class Coverage:
    def __init__(self, min: int, max: int) -> None:
        self.min = min
        self.max = max

    def __eq__(self, other: Coverage) -> bool:
        return (self.min == other.min) & (self.max == other.max)

    def __lt__(self, other: Coverage) -> bool:
        return (self.min < other.min) | (
            (self.min == other.min) & (self.max < other.max)
        )

    def __repr__(self) -> str:
        return f"Coverage(min={self.min}, max={self.max})"

    def __add__(self, other: Coverage) -> Optional[Coverage]:
        if (self.min <= other.min <= self.max + 1) | (
            other.min <= self.min <= other.max + 1
        ):
            return Coverage(min(self.min, other.min), max(self.max, other.max))
        else:
            None

    def __hash__(self) -> int:
        return hash((self.min, self.max))


def combine_coverages(covs: List[Coverage]) -> List[Coverage]:

    sorted_covs = sorted(covs)

    if len(sorted_covs) <= 1:
        return sorted_covs
    else:
        cov_0 = sorted_covs[0]
        other_covs = sorted_covs[1:]
        remaining_covs = []
        for other_cov in other_covs:
            if cov_0 + other_cov:
                cov_0 = cov_0 + other_cov
            else:
                remaining_covs.append(other_cov)
        combined_other_covs = combine_coverages(remaining_covs)
        return [cov_0] + combined_other_covs


class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"

    def __abs__(self) -> int:
        return abs(self.x) + abs(self.y)

    def __eq__(self, other: Vector) -> bool:
        return (self.x == other.x) & (self.y == other.y)

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def coverage_at_yhat(self, yhat: int, strength: int) -> List[Vector]:
        dist_to_yhat = abs(self - Vector(x=self.x, y=yhat))
        if strength > dist_to_yhat:
            remaining_strength = strength - dist_to_yhat
            return [
                Vector(self.x + xhat, yhat)
                for xhat in range(-remaining_strength, remaining_strength + 1)
            ]
        else:
            return []

    def simplified_coverage_at_yhat(
        self, yhat: int, strength: int, x_min: int, x_max: int
    ) -> Tuple[int, int]:
        dist_to_yhat = abs(self - Vector(x=self.x, y=yhat))
        if strength > dist_to_yhat:
            remaining_strength = strength - dist_to_yhat
            return Coverage(
                max(x_min, self.x - remaining_strength),
                min(x_max, self.x + remaining_strength),
            )
        else:
            return None


class Cave:
    def __init__(self, sensors: List[Vector], beacons: List[Vector]) -> None:
        self.sensors = sensors
        self.sensor_strenghts = self.get_sensor_strenghts(sensors, beacons)
        self.beacons = beacons

    def shift_all_items(self, shift_vect: Vector) -> None:

        shifted_sensors: List[Vector] = []
        for sensor in self.sensors:
            shifted_sensors.append(sensor + shift_vect)
        self.sensors = shifted_sensors

        shifted_beacons: List[Vector] = []
        for beacon in self.beacons:
            shifted_beacons.append(beacon + shift_vect)
        self.beacons = shifted_beacons

    def get_sensor_strenghts(
        self, sensors: List[Vector], beacons: List[Vector]
    ) -> List[int]:
        sensor_strengths = []
        for sensor, beacon in zip(sensors, beacons):
            sensor_strengths.append(abs(sensor - beacon))
        return sensor_strengths

    def coverage_at_yhat(self, yhat: int) -> List[Vector]:

        coverage = []

        for i in range(len(self.sensors)):

            strength = self.sensor_strenghts[i]
            ith_coverage = self.sensors[i].coverage_at_yhat(yhat, strength)
            coverage += ith_coverage

        sensors_set = set(self.sensors)
        beacons_set = set(self.beacons)

        coverage = list(set(coverage).difference(sensors_set).difference(beacons_set))

        return coverage

    def simplified_coverage_at_yhat(
        self, yhat: int, x_min: int, x_max: int
    ) -> List[Coverage]:

        coverages = []

        for i in range(len(self.sensors)):

            strength = self.sensor_strenghts[i]
            ith_coverage = self.sensors[i].simplified_coverage_at_yhat(
                yhat, strength, x_min, x_max
            )
            if ith_coverage:
                coverages.append(ith_coverage)

        return combine_coverages(coverages)


def part_1(file: str):

    sensors, beacons = get_sensors_beacons(file)
    cave = Cave(sensors, beacons)

    if file == "example.txt":
        cave.shift_all_items(Vector(-10, -10))
    else:
        cave.shift_all_items(Vector(-2_000_000, -2_000_000))

    print("Part 1:", len(cave.coverage_at_yhat(0)))


def part_2(file: str):

    sensors, beacons = get_sensors_beacons(file)
    cave = Cave(sensors, beacons)

    if file == "example.txt":
        x_min, x_max = 0, 20
        y_min, y_max = 0, 20
    else:
        x_min, x_max = 0, 4_000_000
        y_min, y_max = 0, 4_000_000

    for yhat in range(y_min, y_max + 1):
        coverages = cave.simplified_coverage_at_yhat(yhat, x_min, x_max)
        if len(coverages) > 1:
            break

    xhat = coverages[0].max + 1
    result = 4_000_000 * xhat + yhat

    print("Part 2:", result)


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("data.txt")
