from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


def save_user_date_to_session(request, date_str):
    """Save user's birth date to session in multiple formats"""
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
def DateofBirth(request):
    saved_date = get_user_date_from_session(request, format='slash')
    if request.method == "POST":
        date = request.POST.get('date')
        if date:
            save_user_date_to_session(request, date)

        try:
            # Try HTML date format first
            dob = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            try:
                # Try DD/MM/YYYY
                dob = datetime.strptime(date, "%d/%m/%Y")
            except ValueError:
                return JsonResponse(
                    {"error": "Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD"},
                    status=400
                )

        day = str(dob.day)
        month = str(dob.month)
        year = str(dob.year)
        a = [int(d) for part in (day, month, year) for d in part]
        k = set(a)
        o = list(k)
        print(o)
        m = sum([int(d) for d in day])
        b = sum(a)
        mulakn = 0
        bagiyank = 0
        if m > 9:
            for i in str(m):
                mulakn += int(i)
        else:
            mulakn = m
        if b > 9:
            for i in str(b):
                bagiyank += int(i)
        else:
            bagiyank = b

        print(mulakn,bagiyank)
        x = [4,9,2,3,5,7,8,1,6]
        y = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        for i in x:
            if i in o or i == mulakn or i == bagiyank:
                y[x.index(i)] = i
        matrix = [y[i * 3:(i + 1) * 3] for i in range(3)]
        print(matrix)
        messages = {'mind_plane':[],'heart_plane':[],'practical_plane':[],'vision_plane':[],'will_plane':[],'action_plane':[],'rajyog':[]}
        mini_diag = [matrix[0][0],matrix[1][1],matrix[2][2]]
        anti_diag = [matrix[0][2],matrix[1][1],matrix[2][0]]

        if matrix[0] == [4,9,2]:
            messages['mind_plane'].append("Mind plane is 100% active.")
            messages['mind_plane'].append("Uses mind while making any decision")
            messages['mind_plane'].append("Logical person")
            messages['mind_plane'].append("The Person is Genius")

        elif 4 in matrix[0] and 9 in matrix[0]:
                messages['mind_plane'].append("67% Mind Plane Complete")
                messages['mind_plane'].append("Struggle with health(stress, leg problem, knee)")
                messages['mind_plane'].append("Legal matters may happen")

        elif 4 in matrix[0] and 2 in matrix[0]:
                messages['mind_plane'].append(" May involve in Bad company.")
                messages['mind_plane'].append(" Get Blame for other's misbehaviour.")
                messages['mind_plane'].append("An intelligent person.")
                messages['mind_plane'].append(" Family problems (elder sibling or mother)")

        elif 9 in matrix[0] and 2 in matrix[0]:
                messages['mind_plane'].append("Helps the society")
                messages['mind_plane'].append("Bad with love relations (especially girls)")
                messages['mind_plane'].append("Gets Support from (powerful / Elder)people")
                messages['mind_plane'].append("Spiritual person")

        elif 4 in matrix[0]:
                messages['mind_plane'].append("33% Mind Plane Complete")
                messages['mind_plane'].append("Flexible in Nature")
                messages['mind_plane'].append("Intelligent person")
                messages['mind_plane'].append("No Grey area in life")
                messages['mind_plane'].append("Does Not like manipulative people")
                messages['mind_plane'].append(" Hardworking but may face struggles in early life")

        elif 9 in matrix[0]:
                messages['mind_plane'].append("Religious Person")
                messages['mind_plane'].append(" Artistic, Short Tempered")
                messages['mind_plane'].append(" Loves to help needy people")
                messages['mind_plane'].append("Thinks from the heart")
                messages['mind_plane'].append(" Work for Society")

        elif 2 in matrix[0]:
                messages['mind_plane'].append("Caring Nature")
                messages['mind_plane'].append("Family oriented")
                messages['mind_plane'].append(" Simple person")
                messages['mind_plane'].append("Take decisions considering the family in his/her mind")

        if matrix[1] == [3,5,7]:
            messages['heart_plane'].append("100% Heart plane Complete ")
            messages['heart_plane'].append("Artistic Nature")
            messages['heart_plane'].append("Satisfaction in life")
            messages['heart_plane'].append( "Good learner")
            messages['heart_plane'].append(" Very emotional person")
            messages['heart_plane'].append(" Golden heart")

        elif 3 in matrix[1] and 5 in matrix[1]:
               messages['heart_plane'].append("67% Heart Plane Complete")
               messages['heart_plane'].append(" Rational behavior")
               messages['heart_plane'].append(" Lucky in money matters")
               messages['heart_plane'].append("Good communicator")
               messages['heart_plane'].append("Good for education business")

        elif 5 in matrix[1] and 7 in matrix[1]:
                messages['heart_plane'].append("Attractive personality")
                messages['heart_plane'].append(" Business oriented ")
                messages['heart_plane'].append("If 5 comes two times and 7 comes")
                messages['heart_plane'].append("one time, people learn by themselves and start earning well")

        elif 3 in matrix[1] and 7 in matrix[1]:
                messages['heart_plane'].append(" Lucky person")
                messages['heart_plane'].append("Skilled person")
                messages['heart_plane'].append("Good in occult science")
                messages['heart_plane'].append(" Emotional person")

        elif 3 in matrix[1]:
                messages['heart_plane'].append(" 33% Heart Plane Complete")
                messages['heart_plane'].append(" Knowledgable")
                messages['heart_plane'].append(" Lazy")
                messages['heart_plane'].append("Quick Learner")

        elif 5 in matrix[1]:
                messages['heart_plane'].append("Multiple experiences in life")
                messages['heart_plane'].append(" Enjoy life to the fullest")

        elif 7 in matrix[1]:
                messages['heart_plane'].append(" Intuitive person")
                messages['heart_plane'].append(" Researcher")
                messages['heart_plane'].append(" Don't believe people easily")
                messages['heart_plane'].append("May face minimum two or more break-ups in life")

        if matrix[2] == [8,1,6]:
            messages['practical_plane'].append(" 100% Practical plane Complete")
            messages['practical_plane'].append(" Very practical nature")
            messages['practical_plane'].append("Believes in materialistic gains in life")
            messages['practical_plane'].append(" Romantic nature")
            messages['practical_plane'].append(" Loves power and authority in jobs/business and also in relationships")

        elif 8 in matrix[2] and 1 in matrix[2]:
                messages['practical_plane'].append(" 67% Practical Plane Complete ")
                messages['practical_plane'].append("Aggressive nature")
                messages['practical_plane'].append("Image conscious")
                messages['practical_plane'].append(" Insult or accusation of a crime may arise in life at least once")
                messages['practical_plane'].append(" Loves variety in career")
                messages['practical_plane'].append(" His/her spouse may face frequent health issues")
                messages['practical_plane'].append(" Loves being in authority or power")

        elif 1 in matrix[2] and 6 in matrix[2]:
                messages['practical_plane'].append(" Not very good for married life")
                messages['practical_plane'].append("Luxury comes into life")
                messages['practical_plane'].append("Prefer looking groomed and rich")

        elif 8 in matrix[2] and 6 in matrix[2]:
                messages['practical_plane'].append("Somehow Money finds its way when they are in need")
                messages['practical_plane'].append("May face eyes related problems")
                messages['practical_plane'].append("May face genital-related problems")

        elif 8 in matrix[2]:
                    messages['practical_plane'].append(" 33% Practical Plane Complete")
                    messages['practical_plane'].append("Manages money well")
                    messages['practical_plane'].append("Always speaks the truth and hates liars too much")
                    messages['practical_plane'].append(" Justice lover")

        elif 1 in matrix[2]:
                    messages['practical_plane'].append("Good in communication")
                    messages['practical_plane'].append(" Good memory and grasping power")

        elif 6 in matrix[2]:
                    messages['practical_plane'].append("Family oriented")
                    messages['practical_plane'].append(" Loves luxury around them")
                    messages['practical_plane'].append(" Have Attractive personality")
                    messages['practical_plane'].append("Art lover")

        #  Vision plane

        if matrix[0][0] == 4 and matrix[1][0] == 3 and matrix[2][0] == 8:
                messages['vision_plane'].append("100% Vision plane Complete")
                messages['vision_plane'].append("Strong thinking power")
                messages['vision_plane'].append("Very good in brain-related work")
                messages['vision_plane'].append("Visionary")
                messages['vision_plane'].append(" May get airborne diseases very easily")
                messages['vision_plane'].append(" Good in practical planning of any work")

        elif 4 in matrix[0] and 3 in matrix[1]:
                messages['vision_plane'].append("  67% Vision Plane Complete")
                messages['vision_plane'].append("This combination is not very good for fame and art-related work but gives good results in the technical field")
                messages['vision_plane'].append("A person wants to be organised but can face problems in keeping everything under control")
                messages['vision_plane'].append(" Intelligent person")

        elif 3 in matrix[1] and 8 in matrix[2]:
                messages['vision_plane'].append("Good for real estate and medical field")
                messages['vision_plane'].append("Love to learn new things")

        elif 4 in matrix[0] and 8 in matrix[2]:
                messages['vision_plane'].append("Straight forward nature")
                messages['vision_plane'].append("Small friend circle")
                messages['vision_plane'].append("May make enemies because of their words")
                messages['vision_plane'].append("Delayed success but not denied")
                messages['vision_plane'].append("Life can change 180 degrees if he/she continues to work hard")

        elif 4 != matrix[0][0] or 3 !=  matrix[1][0] or 8 !=  matrix[2][0]:
            messages['vision_plane'].append("If the vision plane is completely missing, a person may suggest something to others but people tend to overlook him")

        # Will plane
        if matrix[0][0] == 9 and matrix[1][0] == 5 and matrix[2][0] == 1:
                messages['will_plane'].append("100% Will plane Complete")
                messages['will_plane'].append("Immense willpower ")
                messages['will_plane'].append("May face difficulties in settling down till the age of 28 but after that, they earn very well")
                messages['will_plane'].append("Usually settles in the 32nd year")
                messages['will_plane'].append(" Many successful people have these numbers ")
                messages['will_plane'].append(" Dominating Personality ")
                messages['will_plane'].append("Fight back attitude")

        elif 9 in matrix[0] and 1 in matrix[1]:
                messages['will_plane'].append("67% Vision Plane Complete")
                messages['will_plane'].append(" Commanding nature")
                messages['will_plane'].append("Leadership qualities")
                messages['will_plane'].append("Respect is everything")
                messages['will_plane'].append("May go for higher education")

        elif 9 in matrix[0] and 5 in matrix[2]:
                messages['will_plane'].append(" Kind-hearted person")
                messages['will_plane'].append("Strong will power")
                messages['will_plane'].append("Manipulates to get his work done")
                messages['will_plane'].append(" Strong communication skills")

        elif 1 in matrix[1] and 5 in matrix[2]:
                messages['will_plane'].append(" Sharp minded people ")
                messages['will_plane'].append(" Good business sense ")
                messages['will_plane'].append(" Good with father/son but possibly one person shines at a time. ")

        elif 9 != matrix[0][1] or 5 != matrix[1][1] or 1 != matrix[2][1]:
            messages['will_plane'].append("If a plane is missing, a person can lose hope in life easily. One or two failures can break his motivation for a long time.")
        #  Action plane

        if matrix[0][0] == 2 and matrix[1][0] == 7 and matrix[2][0] == 6:
                messages['action_plane'].append("  100% Action plane Complete ")
                messages['action_plane'].append("  Action takers (doers) ")
                messages['action_plane'].append("  Quick decision maker  ")
                messages['action_plane'].append("  Good in sports  ")
                messages['action_plane'].append("  Opportunity grabber  ")
                messages['action_plane'].append("  If the mental plane is missing he can't make decisions without proper thinking  ")

        elif 2 in matrix[0] and 7 in matrix[1]:
                messages['action_plane'].append("Caring nature")
                messages['action_plane'].append("  Spiritually inclined   ")
                messages['action_plane'].append("  Highly intuitive  ")
                messages['action_plane'].append("  Sensitive  ")
                messages['action_plane'].append("  Good in occult science  ")
                messages['action_plane'].append("   Money is not their priority  ")

        elif 2 in matrix[0] and 6 in matrix[2]:
                messages['action_plane'].append("   Good looking   ")
                messages['action_plane'].append("   Caring nature   ")
                messages['action_plane'].append("   Art lover    ")
                messages['action_plane'].append("   Prone to water-related diseases   ")
                messages['action_plane'].append("   Loves family too much (may become a hurdle in growth)    ")

        elif 7 in matrix[1] and 6 in matrix[2]:
                messages['action_plane'].append("   Metal elements traits will be there  ")
                messages['action_plane'].append("   Attraction towards the opposite sex  ")
                messages['action_plane'].append("   Indulge in More than one love relationship  ")
                messages['action_plane'].append("   Chances of an extra marital affair  ")

        elif 2 != matrix[0][2] or 7 != matrix[1][2] or 6 != matrix[2][2]:
            messages['action_plane'].append(" If this plane is missing, the person may be lazy and have weak decision-making power.")

        if mini_diag == [4,5,6]:
            messages['rajyog'].append("Rajyog Detected: Support & Stability (4-5-6)")
            messages['rajyog'].append("- Strong family bonds and loyal friends")
            messages['rajyog'].append("- Harmonious relationships with spouse/children")
            messages['rajyog'].append("- Universal support in achieving goals")

        elif anti_diag == [2,5,8]:
            messages['rajyog'].append("Rajyog Detected:Property & Wealth (2-5-8)")
            messages['rajyog'].append("- Success in real estate and land investments")
            messages['rajyog'].append("- Talent in architecture/interior design")
            messages['rajyog'].append("- Agricultural or natural resource prosperity")

        if not messages['rajyog']:
            messages['rajyog'].append("No Rajyog patterns in diagonals")


        print(messages)
        context = {
            'matrix': matrix,
            'messages': messages,
            'is_authenticated': request.user.is_authenticated,
            'user_date': saved_date,
        }
        return render(request, 'table.html', context)
    return render(request, 'table.html')