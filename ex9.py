1)A machine has 12 items: 4 expired and 8 fresh. It has a bug: it never dispenses the same item twice in a row. If the last item dispensed was fresh, what is the probability the next item is expired?
def vending_machine_prob():
    print("Vending Machine Inventory Probability")
    try:
        # 1. Get Inventory Details from User
        total_items = int(input("Enter total items in machine: "))
        expired = int(input("Enter number of expired items: "))
        fresh = total_items - expired

        print(f" Calculated Fresh items: {fresh}")

        # 2. Logic: The 'available pool' (excluding the current item being viewed)
        available_pool = total_items - 1

        if available_pool <= 0:
            print("Error: Not enough items in the machine to calculate probability.")
            return None

        # 3. Calculation
        prob_expired = expired / available_pool

        # 4. Display Steps
        print("\n" + "="*40)
        print("="*40)
        print(f"Total Items:      {total_items}")
        print(f"Expired Items:    {expired}")
        print(f"Available Pool:   {total_items} - 1 = {available_pool}")
        print(f"Calculation:      {expired} / {available_pool}")
        print("="*40)

        return prob_expired

    except ValueError:
        print("Error: Please enter whole numbers for inventory items.")
        return None

# Run and Print Result
result = vending_machine_prob()
if result is not None:
    print(f"\nProb of Next is Expired: {result:.4f}")

Vending Machine Inventory Probability
Enter total items in machine: 12
Enter number of expired items: 4
 Calculated Fresh items: 8

========================================
========================================
Total Items:      12
Expired Items:    4
Available Pool:   12 - 1 = 11
Calculation:      4 / 11
========================================

2) An email filter is trained where of incoming emails are spam. Data shows that of spam emails contain the word "Free", while only of non-spam (ham) emails contain it. If a new email arrives containing the word "Free", what is the probability that it is spam?

def bayes_spam_filter():
    print("Bayes' Spam Filter")
    try:
        # 1. Get Priors from User
        p_spam = float(input("Enter P(Spam): "))
        p_ham = 1.0 - p_spam
        print(f"set P(Ham) to: {p_ham:.2f}")

        # 2. Get Likelihoods from User
        p_free_given_spam = float(input("Enter P(Free | Spam) : "))
        p_free_given_ham = float(input("Enter P(Free | Ham) : "))

        # 3. Step-by-Step Calculation
        print("\n" + "="*40)
        print("="*40)

        # Numerator: P(Free | Spam) * P(Spam)
        numerator = p_free_given_spam * p_spam
        print(f"P(Free|Spam) * P(Spam)")
        print(f"      {p_free_given_spam} * {p_spam} = {numerator:.4f}")

        # Denominator (Total Probability): P(Free) = P(Free|S)P(S) + P(Free|H)P(H)
        p_free = numerator + (p_free_given_ham * p_ham)
        print(f"\nTotal P(Free)")
        print(f"      ({p_free_given_spam}*{p_spam}) + ({p_free_given_ham}*{p_ham})")
        print(f"      {numerator:.4f} + {p_free_given_ham * p_ham:.4f} = {p_free:.4f}")

        # Final Bayes' Rule Calculation
        p_spam_given_free = numerator / p_free
        print(f"\nP(Spam | Free)")
        print(f"      {numerator:.4f} / {p_free:.4f} = {p_spam_given_free:.4f}")
        print("="*40)

        print(f"\nThe probability the email is spam is {p_spam_given_free:.4f}")

    except ValueError:
        print(" Error: Please enter numerical values (e.g., 0.5).")
    except ZeroDivisionError:
        print("Error: Total probability P(Free) resulted in zero.")

# Run the function
bayes_spam_filter()

Bayes' Spam Filter
Enter P(Spam): 0.3
set P(Ham) to: 0.70
Enter P(Free | Spam) : 0.8
Enter P(Free | Ham) : 0.1

========================================
========================================
P(Free|Spam) * P(Spam)
      0.8 * 0.3 = 0.2400

Total P(Free)
      (0.8*0.3) + (0.1*0.7)
      0.2400 + 0.0700 = 0.3100

P(Spam | Free)
      0.2400 / 0.3100 = 0.7742
========================================
The probability the email is spam is 0.7742

3)Given the Fully Joint Probability Distribution for three variables Rainy, Cloudy, and Wet calculate:
The Marginal Probability of it being Rainy.
The Conditional Probability that it is Rainy given that the ground is Wet.
Rain | Cloud | Wet | Prob
-------------------------
 1   |   1   |  1  | 0.08
 1   |   1   |  0  | 0.02
 1   |   0   |  1  | 0.09
 1   |   0   |  0  | 0.31
 0   |   1   |  1  | 0.01
 0   |   1   |  0  | 0.04
 0   |   0   |  1  | 0.10
 0   |   0   |  0  | 0.35

def weather_analysis_steps():
    print("Weather Probability")

    # R: Rain, C: Cloudy, W: Wet
    combos = [(1,1,1), (1,1,0), (1,0,1), (1,0,0),
              (0,1,1), (0,1,0), (0,0,1), (0,0,0)]

    joint_table = {}
    for r, c, w in combos:
        p = float(input(f"Enter P(Rain={r}, Cloudy={c}, Wet={w}): "))
        joint_table[(r, c, w)] = p

    print("\n" + "="*50)
    print("="*50)

    # 1. Marginal Probability of Rain P(R=1)
    # Get all probabilities where R=1
    rain_probs = [prob for (r, c, w), prob in joint_table.items() if r == 1]
    p_rain = sum(rain_probs)

    print(f"Marginal P(Rain)")
    print(f"Sum of all rows where Rain=1:")
    print(f"P = {' + '.join(map(str, rain_probs))} = {p_rain:.4f}")

    # 2. Conditional Probability P(Rain | Wet)
    # Step A: P(Rain  Wet)
    rw_probs = [prob for (r, c, w), prob in joint_table.items() if r == 1 and w == 1]
    p_rain_and_wet = sum(rw_probs)

    # Step B: P(Wet)
    wet_probs = [prob for (r, c, w), prob in joint_table.items() if w == 1]
    p_wet = sum(wet_probs)

    # Step C: Division
    p_rain_given_wet = p_rain_and_wet / p_wet if p_wet > 0 else 0

    print(f"\nonditional P(Rain | Wet)")
    print(f"Joint P(Rain Wet): {' + '.join(map(str, rw_probs))} = {p_rain_and_wet:.4f}")
    print(f"Total P(Wet):        {' + '.join(map(str, wet_probs))} = {p_wet:.4f}")
    print(f"P(Rain | Wet) = Joint / Total")
    print(f"   {p_rain_and_wet:.4f} / {p_wet:.4f} = {p_rain_given_wet:.4f}")
    print("="*50)

weather_analysis_steps()

Weather Probability
Enter P(Rain=1, Cloudy=1, Wet=1): 0.08
Enter P(Rain=1, Cloudy=1, Wet=0): 0.02
Enter P(Rain=1, Cloudy=0, Wet=1): 0.09
Enter P(Rain=1, Cloudy=0, Wet=0): 0.31
Enter P(Rain=0, Cloudy=1, Wet=1): 0.01
Enter P(Rain=0, Cloudy=1, Wet=0): 0.04
Enter P(Rain=0, Cloudy=0, Wet=1): 0.10
Enter P(Rain=0, Cloudy=0, Wet=0): 0.35

==================================================
==================================================
Marginal P(Rain)
Sum of all rows where Rain=1:
P = 0.08 + 0.02 + 0.09 + 0.31 = 0.5000

onditional P(Rain | Wet)
Joint P(Rain  Wet): 0.08 + 0.09 = 0.1700
Total P(Wet):        0.08 + 0.09 + 0.01 + 0.1 = 0.2800
P(Rain | Wet) = Joint / Total
   0.1700 / 0.2800 = 0.6071
==================================================.
