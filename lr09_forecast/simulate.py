import csv, math, random, sys

def simulate(velocities, remaining, runs=10000, seed=42):
    rnd = random.Random(seed)
    results = []
    for _ in range(runs):
        left, sprints = remaining, 0
        while left > 0:
            left -= rnd.choice(velocities)  # тягнемо velocity одного зі спринтів
            sprints += 1
            if sprints > 1000:  # захист від нульової velocity
                break
        results.append(sprints)
    results.sort()
    p = lambda q: results[math.ceil(q * runs) - 1]  # перцентиль, цілі спринти
    return p(0.5), p(0.85)

def load(path, rows=None):
    with open(path, encoding="utf-8") as f:
        data = list(csv.DictReader(f))
    if rows:
        data = [r for r in data if int(r["sprint"]) in rows]
    return [float(r["points_done"]) for r in data]

if __name__ == "__main__":
    mine = load("velocity.csv")
    print("Мої, весь реліз 37:", simulate(mine, 37))
    print("Мої, залишок 21:", simulate(mine, 21))
    ref = sys.argv[1] if len(sys.argv) > 1 else "lr09_reference_velocity.csv"
    for name, rows in [("усі 12", None), ("1 і 2", {1, 2}), ("5 і 6", {5, 6})]:
        print("Навчальні", name, simulate(load(ref, rows), 220))
