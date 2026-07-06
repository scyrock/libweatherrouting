import math
import time
import random
random.seed(1)
from weatherrouting import utils

def point_distance_run(lat_a, lon_a, lat_b, lon_b):
    start = time.perf_counter()
    dist_old = utils.point_distance(lat_a, lon_a, lat_b, lon_b,
                                    "nm", pyproj=False)
    t_old = time.perf_counter() - start
    start = time.perf_counter()
    dist_new = utils.point_distance(lat_a, lon_a, lat_b, lon_b,
                                    "nm", pyproj=True)
    t_new = time.perf_counter() - start
    err_rel = abs(dist_old-dist_new)/dist_old

    return t_old, t_new, err_rel

def routage_point_distance_run(lat_a, lon_a, d, hdg,):
    start = time.perf_counter()
    of_old = utils.routage_point_distance(lat_a, lon_a, d, hdg,
                                              "nm", pyproj=False)
    t_old = time.perf_counter() - start
    start = time.perf_counter()
    of_new = utils.routage_point_distance(lat_a, lon_a, d, hdg,
                                              "nm", pyproj=True)
    t_new = time.perf_counter() - start
    err = utils.point_distance(of_old[0], of_old[1], of_new[0], of_new[1], 
                                   "nm", pyproj=False)

    return t_old, t_new, err

def main():
    iterations = 100_000

    # utils.point_distance
    err_rel_pd = 0
    t_old_pd = 0
    t_new_pd = 0

    # routage_point_distance
    err_rp = 0
    t_old_rp = 0
    t_new_rp = 0

    for _ in range(iterations):
        lat_a = random.uniform(-90, 90)
        lon_a = random.uniform(-180, 180)
        lat_b = random.uniform(-90, 90)
        lon_b = random.uniform(-180, 180)
        d = random.uniform(0, 100)
        hdg = random.uniform(0, 2*math.pi)

        # utils.point_distance
        t_old, t_new, err_rel = point_distance_run(lat_a, lon_a, lat_b, lon_b)
        t_old_pd    += t_old
        t_new_pd    += t_new
        err_rel_pd  += err_rel

        # routage_point_distance
        t_old, t_new, err = routage_point_distance_run(lat_a, lon_a, d, hdg)
        t_old_rp    += t_old
        t_new_rp    += t_new
        err_rp  += err

    print(f"Number of iterations: {iterations}")

    print(f">> utils.point_distance <<")
    print(f"Sum relative error = {err_rel_pd:.6f}")
    print(f"latlon time:      {t_old_pd:.6f}")
    print(f"pyproj time time: {t_new_pd:.6f}")
    print(f"time reduction:   {t_old_pd/t_new_pd:.1f}x")

    print(f"\n>> utils.routage_point_distance <<")
    print(f"Sum errors =      {err_rp:.3E}")
    print(f"latlon time:      {t_old_rp:.6f}")
    print(f"pyproj time time: {t_new_rp:.6f}")
    print(f"time reduction:   {t_old_rp/t_new_rp:.1f}x")

if __name__ == "__main__":
    main()

