from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

def save_user_date_to_session(request, date_str):
    try:
        if not date_str:
            return False
        date_str = str(date_str).strip()
        if '/' in date_str:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        elif '-' in date_str:
            parts = date_str.split('-')
            if len(parts[0]) == 4:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        else:
            return False

        slash_str = date_obj.strftime('%d/%m/%Y')
        dash_str = date_obj.strftime('%Y-%m-%d')
        request.session['user_birth_date_slash'] = slash_str
        request.session['user_birth_date_dash'] = dash_str
        request.session['user_birth_date_object'] = dash_str
        request.session['dob'] = slash_str
        request.session['birthDate'] = slash_str
        request.session.modified = True
        return True
    except Exception as e:
        print(f"Error saving date to session: {e}")
        return False

def get_user_date_from_session(request, format='slash'):
    if format == 'dash':
        return request.session.get('user_birth_date_dash') or request.session.get('birthDate')
    return request.session.get('user_birth_date_slash') or request.session.get('dob') or request.session.get('birthDate')

def numbers_role(request):
    date = None
    if request.method == "POST":
        date = request.POST.get('birthDate')
        if date:
            save_user_date_to_session(request, date)

    if not date:
        date = get_user_date_from_session(request, format='slash')

    mulakn = 0
    bagiyank = 0
    lucky_number = []
    unlucky_number = []

    if date:
        try:
            date_str = date.strip()
            if '/' in date_str:
                parts = date_str.split('/')
                day, month, year = parts[0], parts[1], parts[2]
            elif '-' in date_str:
                parts = date_str.split('-')
                if len(parts[0]) == 4:
                    year, month, day = parts[0], parts[1], parts[2]
                else:
                    day, month, year = parts[0], parts[1], parts[2]

            a = [int(d) for part in (day, month, year) for d in part]
            m = sum([int(d) for d in day])
            b = sum(a)

            if m > 9:
                for i in str(m):
                    mulakn += int(i)
            else:
                mulakn = m

            if b > 9:
                for i in str(b):
                    bagiyank += int(i)
                    if bagiyank > 9:
                        bagiyank -= 9
            else:
                bagiyank = b

            z = {
                1: {'friend': [1, 2, 3, 5, 6, 9], 'enemy': [8], 'neutral': [4, 7]},
                2: {'friend': [1, 2, 3, 5], 'enemy': [8, 4, 9], 'neutral': [7, 6]},
                3: {'friend': [1, 2, 3, 5, 7], 'enemy': [6], 'neutral': [4, 8, 7, 9]},
                4: {'friend': [1, 5, 7, 6, 4, 8], 'enemy': [2, 9, 4, 8], 'neutral': [3]},
                5: {'friend': [1, 2, 3, 5, 6], 'enemy': [None], 'neutral': [4, 7, 8, 9]},
                6: {'friend': [1, 4, 5, 6, 7], 'enemy': [3], 'neutral': [2, 8, 9]},
                7: {'friend': [1, 3, 5, 4, 6], 'enemy': [None], 'neutral': [8, 2, 7, 9]},
                8: {'friend': [5, 3, 6, 7, 4, 8], 'enemy': [1, 2, 4, 8], 'neutral': [9]},
                9: {'friend': [1, 3, 5], 'enemy': [4, 2], 'neutral': [9, 7, 6, 8]}
            }

            all_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if mulakn in z and bagiyank in z:
                lucky_number = [i for i in all_nums if i in z[bagiyank]['friend'] and i not in z[bagiyank]['enemy'] and i not in z[bagiyank]['neutral'] and i in z[mulakn]['friend'] and i not in z[mulakn]['enemy'] and i not in z[mulakn]['neutral']]
                unlucky_number = [i for i in all_nums if i not in lucky_number]
        except Exception as e:
            print(f"Error calculating lucky numbers: {e}")

    saved_date = get_user_date_from_session(request, format='slash')
    return render(request, 'create.html', context={
        'bagiyank': bagiyank,
        'mulakn': mulakn,
        'lucky_number': lucky_number,
        'unlucky_number': unlucky_number,
        'user_birth_date': saved_date,
    })
