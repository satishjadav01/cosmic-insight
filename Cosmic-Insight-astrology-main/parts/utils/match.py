from django.shortcuts import render
from django.http import JsonResponse

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
        """Check if any row contains all elements of Rajyog plans"""
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


def marriage_score(request):
    malemulakn, femalemulakn = 0, 0
    malebhagiyank, femalebhagiyank = 0, 0
    male_matrix = []
    female_matrix = []
    total = 0

    if request.method == "POST":
        male = request.POST.get('dob1')
        female = request.POST.get('dob2')
        print(male, female)
        if not male or not female:
            return JsonResponse({"error": 'Date is not valid'}, status=400)

        mday, mmonth, myear = male.split('/')
        fday, fmonth, fyear = female.split('/')

        malem = [int(d) for part in (mday, mmonth, myear) for d in part]
        femalem = [int(d) for part in (fyear, fmonth, fday) for d in part]

        # malem = set(malem)
        # malem = list(malem)
        print(malem)
        # femalem = set(femalem)
        # femalem = list(femalem)
        print(femalem)
        malemm = sum([int(d) for d in mday])
        maleb = sum(malem)
        femalemm = sum([int(d) for d in fday])
        femaleb = sum(femalem)

        if malemm > 9:
            for i in str(malemm):
                malemulakn += int(i)
        else:
            malemulakn = malemm

        if femalemm > 9:
            for i in str(femalemm):
                femalemulakn += int(i)
        else:
            femalemulakn = femalemm

        if maleb > 9:
            for i in str(maleb):
                malebhagiyank += int(i)
                if malebhagiyank > 9:
                    malebhagiyank -= 9
        else:
            malebhagiyank = maleb

        if femaleb > 9:
            for i in str(femaleb):
                femalebhagiyank += int(i)
                if femalebhagiyank > 9:
                    femalebhagiyank -= 9
        else:
            femalebhagiyank = femaleb

        print(malemulakn, malebhagiyank, femalemulakn, femalebhagiyank)

        x = [4, 9, 2, 3, 5, 7, 8, 1, 6]
        y = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        for i in x:
            if i in malem or i == malemulakn or i == malebhagiyank:
                y[x.index(i)] = i
        male_matrix = [y[i * 3:(i + 1) * 3] for i in range(3)]
        print(male_matrix)
        mmini_diag = [male_matrix[0][0], male_matrix[1][1], male_matrix[2][2]]
        manti_diag = [male_matrix[0][2], male_matrix[1][1], male_matrix[2][0]]

        y = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        for i in x:
            if i in femalem or i == femalemulakn or i == femalebhagiyank:
                # print("Here i=",i)
                y[x.index(i)] = i
        female_matrix = [y[i * 3:(i + 1) * 3] for i in range(3)]
        print("thik hey ::=>", female_matrix)
        femini_diag = [female_matrix[0][0], female_matrix[1][1], female_matrix[2][2]]
        feanti_diag = [female_matrix[0][2], female_matrix[1][1], female_matrix[2][0]]

        data = {1: {'friend': [1, 2, 3, 5, 6, 9], 'neutral': [4, 7]},
                2: {'friend': [1, 2, 3, 5], 'neutral': [7, 6]},
                3: {'friend': [1, 2, 3, 5, 7], 'neutral': [4, 8, 7, 9]},
                4: {'friend': [1, 5, 7, 6, 4, 8], 'neutral': [3]},
                5: {'friend': [1, 2, 3, 5, 6], 'neutral': [4, 7, 8, 9]},
                6: {'friend': [1, 4, 5, 6, 7], 'neutral': [2, 8, 9]},
                7: {'friend': [1, 3, 5, 4, 6], 'neutral': [8, 2, 7, 9]},
                8: {'friend': [5, 3, 6, 7, 4, 8], 'neutral': [9]},
                9: {'friend': [1, 3, 5], 'neutral': [9, 7, 6, 8]}
                }

        print("Male Matrix ::=>")
        print("Female Matrix ::=>")

        if femalemulakn in data[malemulakn]['friend']:
            print("5 marks")
            total += 20
            print("mittra", male_matrix, female_matrix)

        male_lines = find_lines(male_matrix)
        female_lines = find_lines(female_matrix)
        print("male_line:", male_lines, "female_line:", female_lines)

        points = transfer_points(male_lines, female_lines)['points']
        total += points

        if len(male_matrix) >= 3 and len(female_matrix) >= 3:
            if (male_matrix[0] == [4, 9, 2] or female_matrix[0] == [4, 9, 2] or male_matrix[1] == [3, 5, 7] or
                female_matrix[1] == [3, 5, 7] or male_matrix[2] == [8, 1, 6] or female_matrix[2] == [8, 1, 6] or
                male_matrix[0][0] == 4 and male_matrix[1][0] == 3 and male_matrix[2][0] == 8 and female_matrix[0][
                    0] == 4 and female_matrix[1][0] == 3 and female_matrix[2][0] == 8 or
                male_matrix[0][0] == 9 and male_matrix[1][0] == 5 and male_matrix[2][0] == 1 and female_matrix[0][
                    0] == 9 and female_matrix[1][0] == 5 and female_matrix[2][0] == 1 or
                male_matrix[0][0] == 2 and male_matrix[1][0] == 7 and male_matrix[2][0] == 6 and female_matrix[0][
                    0] == 2 and female_matrix[1][0] == 7 and female_matrix[2][0] == 6 or
                mmini_diag == [4, 5, 6] or femini_diag == [4, 5, 6]) or (
                    manti_diag == [2, 5, 8] or feanti_diag == [2, 5, 8]):
                print("5 marks")
                total += 20
                print("nokw", male_matrix, female_matrix)
        # transfer_points already called on line 191 with correct args
        # (removed broken call that passed raw date strings)
        if 5 in male_matrix[1] or 6 in male_matrix[2] or 5 in female_matrix[1] or 6 in female_matrix[2]:
            print("5 marks")
            total += 20
            print("recveried", male_matrix, female_matrix)
        else:
            print("0 marks")

    # Build highlighted number sets for template matrix display
    male_highlighted = [cell for row in male_matrix for cell in row if cell != ' '] if male_matrix else []
    female_highlighted = [cell for row in female_matrix for cell in row if cell != ' '] if female_matrix else []

    return render(request, 'basci.html', context={'malemulakn': malemulakn,
                                                  'malebhagiyank': malebhagiyank,
                                                  'femalemulakn': femalemulakn,
                                                  'femalebhagiyank': femalebhagiyank,
                                                  'male_matrix': male_matrix,
                                                  'female_matrix': female_matrix,
                                                  'male_highlighted': male_highlighted,
                                                  'female_highlighted': female_highlighted,
                                                  'points': total,
                                                  })