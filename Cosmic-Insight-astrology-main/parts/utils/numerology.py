from django.shortcuts import render
def transfer_points(male_lines, female_lines):
    MAGIC_PLANS = [
        {4, 9, 2}, {3, 5, 7}, {8, 1, 6},   # rows
        {4, 3, 8}, {9, 5, 1}, {2, 7, 6},   # cols
        {4, 5, 6}, {2, 5, 8}               # diagonals
    ]

    RAJYOG_PLANS = [{4, 5, 6}, {2, 5, 8}]

    def flatten(lines):
        return {x for row in lines for x in row}

    def has_rajyog(lines):
        for row in lines:
            s = set(row)
            if any(plan.issubset(s) for plan in RAJYOG_PLANS):
                return True
        return False

    points = 0

    for row_m in male_lines:
        for row_f in female_lines:
            if set(row_m) == set(row_f) and row_m:   # row matches
                points += 20

                return {"points": points}


    for giver, receiver in [(male_lines, female_lines), (female_lines, male_lines)]:
        for plan in MAGIC_PLANS:
            for row in receiver:
                missing = plan - set(row)
                if len(missing) == 1 and list(missing)[0] in flatten(giver):
                    row.append(list(missing)[0])   # transfer number
                    points += 20                    # +5 for transfer
                    if has_rajyog(male_lines) or has_rajyog(female_lines):
                        points += 20               # +5 extra for Rajyog
                    return {"points": points}

    return {"points": points}

def find_lines(matrix):
    def get_cell_value(cell):
        if isinstance(cell, str) and cell.strip() == '':
            return None
        try:
            return int(cell)
        except (TypeError, ValueError):
            return None

    n = 3
    values = [[get_cell_value(matrix[i][j]) for j in range(n)] for i in range(n)]

    # define rows, cols, diagonals
    lines = []
    for i in range(n):
        lines.append([(i, j) for j in range(n)])  # rows
    for j in range(n):
        lines.append([(i, j) for i in range(n)])  # cols
    lines.append([(0, 0), (1, 1), (2, 2)])       # main diagonal
    lines.append([(0, 2), (1, 1), (2, 0)])       # anti diagonal

    result = []
    for line in lines:
        vals = [values[i][j] for (i, j) in line if values[i][j] is not None]
        if len(vals) >= 2:
            result.append(vals)

    return result


# Test
male_input = [[' 4', ' 9', '2'], [' ', ' 5', ' '], ['8', '1', ' ']]
female_input = [[' 4', ' 9', ' '], [' ', '5', '7'], [' 8', '1 ', ' ']]

male_lines = find_lines(male_input)
female_lines = find_lines(female_input)

print("Male Lines:", male_lines)
print("Female Lines:", female_lines)

