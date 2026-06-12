def pick_winner(participants_csv: str) -> str:
    import random

    names = [n.strip() for n in participants_csv.split(",") if n.strip()]
    if not names:
        return "No participants provided."
    return f"Winner: {random.choice(names)}"


def weighted_draw(entries_csv: str, weights_csv: str) -> str:
    import random

    names = [n.strip() for n in entries_csv.split(",") if n.strip()]
    weights = [float(w.strip()) for w in weights_csv.split(",") if w.strip()]
    if not names or not weights or len(names) != len(weights):
        return "Mismatched entries and weights."
    return f"Winner: {random.choices(names, weights=weights, k=1)[0]}"


def multi_round(names_csv: str, rounds: int = 3) -> str:
    import random

    names = [n.strip() for n in names_csv.split(",") if n.strip()]
    results = []
    for r in range(rounds):
        random.shuffle(names)
        results.append(f"Round {r + 1}: {names[:3]}")
    return "\n".join(results)
