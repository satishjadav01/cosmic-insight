class NumerologyService:
    @staticmethod
    def calculate_mulank_bhagyank(day_str,month_str,year_str):

        day_sum = sum(int(d) for d in day_str)
        mulank = day_sum if day_sum <= 9 else sum(int(d) for d in str(day_sum))

        digits = [int(d) for part in (day_str,month_str,year_str) for d in part]
        total_sum = sum(digits)
        bhagyank = total_sum
        while bhagyank > 9:
            bhagyank = sum(int(d) for d in str(bhagyank))
        return mulank,bhagyank

    @staticmethod
    def generate_matrix(number_list,mulank,bhagyank):
        stanadard_grid = [4,9,2,3,5,7,8,1,6]
        flat_matrix = [' ' for _ in range(9)]

        for i,val in enumerate(stanadard_grid):
            if val in number_list or val == mulank or val == bhagyank:
                flat_matrix[i] = val

        return [flat_matrix[i:i+3] for i in range(0,9,3)]

class MarriageService:
    @staticmethod
    def calculate_fullmatch(dob_male,dob_female):
        return {
            "points":50,
            "malemulank":0,
            "malebhagiyank":0,
            "male_matrix":[],
            "femalemulank":0,
            "femalebhagiyank":0,
            "female_matrix":[],
        }