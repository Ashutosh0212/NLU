"""
Reggy++ - Extended regex-based chatbot
Assignment 1 - NLU
Ashutosh (P25CS0002)
Uses only: import re, from datetime import date
"""
import re
from datetime import date


def parse_birthday(text):
    """
    Parse birthday from various formats using regex.
    Returns (day, month, year) or None if parsing fails.
    """
    text = text.strip()
    
    months = {
        'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
        'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
        'aug': 8, 'august': 8, 'sep': 9, 'sept': 9, 'september': 9,
        'oct': 10, 'october': 10, 'nov': 11, 'november': 11,
        'dec': 12, 'december': 12
    }
    
    def fix_year(y):
        if y < 100:
            return y + 2000 if y < 50 else y + 1900
        return y
    
    def valid_date(d, m, y):
        try:
            date(y, m, d)
            return True
        except ValueError:
            return False
    
    # dd-mm-yyyy, dd/mm/yyyy, mm-dd-yyyy etc
    m = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})', text)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), fix_year(int(m.group(3)))
        # if one > 12 it must be day
        if a > 12 and b <= 12:
            return (a, b, y) if valid_date(a, b, y) else None
        if a <= 12 and b > 12:
            return (b, a, y) if valid_date(b, a, y) else None
        # both <= 12: try dd-mm first, then mm-dd
        if valid_date(a, b, y):
            return (a, b, y)
        if valid_date(b, a, y):
            return (b, a, y)
        return None
    
    # dd Month YYYY or dd Month yy (with optional st/nd/rd/th)
    pat = r'(\d{1,2})(?:st|nd|rd|th)?\s+(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+(\d{2,4})'
    m = re.search(pat, text, re.IGNORECASE)
    if m:
        d = int(m.group(1))
        mon_str = m.group(2).lower()[:3]
        for k, v in months.items():
            if k.startswith(mon_str) or mon_str in k:
                mo = v
                break
        else:
            mo = 1
        y = int(m.group(3))
        if y < 100:
            y += 2000 if y < 50 else 1900
        return (d, mo, y)
    
    # Month dd, YYYY or Month ddth, YYYY
    pat = r'(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{2,4})'
    m = re.search(pat, text, re.IGNORECASE)
    if m:
        mon_str = m.group(1).lower()[:3]
        mo = months.get(mon_str, 1)
        for k, v in months.items():
            if k.startswith(mon_str):
                mo = v
                break
        d = int(m.group(2))
        y = int(m.group(3))
        if y < 100:
            y += 2000 if y < 50 else 1900
        return (d, mo, y)
    
    return None


def calculate_age(birth_tuple):
    """Calculate age from (day, month, year)."""
    if not birth_tuple:
        return None
    d, m, y = birth_tuple
    today = date.today()
    try:
        bd = date(y, m, d)
        age = today.year - bd.year
        if (today.month, today.day) < (bd.month, bd.day):
            age -= 1
        return age
    except ValueError:
        return None


def get_surname(fullname):
    """Extract surname (last word) from full name. Returns None if single name."""
    fullname = fullname.strip()
    if not fullname:
        return None
    parts = re.split(r'\s+', fullname)
    parts = [p for p in parts if p]
    if len(parts) < 2:
        return None
    return parts[-1]


def match_mood(text):
    """
    Match mood from text. Handles common typos by using flexible patterns.
    Returns mood category or None.
    """
    t = text.strip().lower()
    
    # patterns with typo tolerance - optional extra/missing chars for common mistakes
    mood_patterns = [
        (r'hap+y+i*e*s*t*|hapy|hapi|hppy', 'happy'),
        (r'sa+d+d*y*|sadd|sad\b', 'sad'),
        (r'exci+ted|exited|exicited|excited', 'excited'),
        (r'angr+y|angery|angry', 'angry'),
        (r'tir+d+e*|tired|tierd', 'tired'),
        (r'bor+ed|bored|boared', 'bored'),
        (r'nervou+s|nervus|nervos', 'nervous'),
        (r'calm|clam', 'calm'),
        (r'stres+ed|stressed|stresed', 'stressed'),
        (r'goo+d|gud|good', 'good'),
        (r'gre+a+t|gret|great', 'great'),
        (r'awful|awfl', 'awful'),
        (r'\bok(ay)?\b|okey', 'okay'),
        (r'fine|fien|fne', 'fine'),
        (r'wonderful|wnderful', 'wonderful'),
        (r'depres+ed|depressed', 'depressed'),
        (r'anxious|anxous', 'anxious'),
    ]
    
    for pat, mood in mood_patterns:
        if re.search(pat, t):
            return mood
    return None


def get_mood_response(mood):
    """Return appropriate response based on detected mood."""
    responses = {
        'happy': "That's nice to hear! Hope it stays that way :)",
        'sad': "I'm sorry to hear that. Things will get better, hang in there.",
        'excited': "Awesome! What's got you so excited?",
        'angry': "I understand. Sometimes we all need to vent. Take a deep breath.",
        'tired': "Rest is important. Maybe take a short break?",
        'bored': "Maybe try something new? A walk or a hobby could help.",
        'nervous': "It's okay to feel nervous. Take things one step at a time.",
        'calm': "That's a good state to be in. Peaceful.",
        'stressed': "Stress is tough. Remember to take care of yourself.",
        'good': "Good to know you're doing well!",
        'great': "That's great! Keep it up!",
        'awful': "I'm sorry things are rough. Hope it improves soon.",
        'okay': "Alright. Let me know if you want to talk about anything.",
        'fine': "Okay, fine is fine I guess!",
        'wonderful': "Wonderful indeed! Glad to hear it.",
        'depressed': "I'm really sorry. Please consider talking to someone if it gets heavy.",
        'anxious': "Anxiety is hard. Breathing exercises sometimes help.",
    }
    return responses.get(mood, "I see. Thanks for sharing.")


def main():
    print("=" * 50)
    print("Hi! I'm Reggy++. Nice to meet you!")
    print("=" * 50)
    
    # Greeting / name
    name = None
    surname = None
    age = None
    mood_asked = False
    
    # Simple pattern matching for basic chat
    patterns = [
        (r'\b(hi|hello|hey|hola)\b', "Hello! How can I help you today?"),
        (r'\b(my name is|i am|i\'m|call me)\s+(.+)', None),  # extract name
        (r'\b(name is|name\'s)\s+(.+)', None),
        (r'\b(what is your name|who are you)\b', "I'm Reggy++, a simple chatbot. What's your name?"),
        (r'\b(bye|goodbye|see ya|exit|quit)\b', "Goodbye! Take care!"),
    ]
    
    while True:
        try:
            user = input("\nYou: ").strip()
        except EOFError:
            break
        if not user:
            print("Reggy++: Say something!")
            continue
        
        user_lower = user.lower()
        responded = False
        
        # Check for exit
        if re.search(r'\b(bye|goodbye|exit|quit)\b', user_lower):
            print("Reggy++: Goodbye! Take care!")
            break
        
        # Ask for name if we don't have it
        if name is None and not re.search(r'\b(bye|quit|exit)\b', user_lower):
            m = re.search(r'(?:my name is|i am|i\'m|call me|name is|name\'s)\s+(.+)', user_lower)
            if m:
                name = m.group(1).strip()
                surname = get_surname(name)
                if surname:
                    print(f"Reggy++: Nice to meet you! I see your surname is {surname}.")
                else:
                    print(f"Reggy++: Hi {name}! Nice to meet you.")
                responded = True
            else:
                # maybe they just said their name (exclude greetings)
                is_greeting = bool(re.search(r'^\s*(hi|hello|hey|hola|yo)\s*$', user_lower))
                words = re.split(r'\s+', user.strip())
                looks_like_date = bool(re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', user) or
                                    re.search(r'\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', user_lower))
                if (not is_greeting and len(words) >= 1 and len(user) < 40
                        and not re.search(r'\?|what|when|how', user_lower)
                        and not looks_like_date):
                    name = user.strip()
                    surname = get_surname(name)
                    if surname:
                        print(f"Reggy++: Hi! So {surname} is your surname. Nice to meet you!")
                    else:
                        print(f"Reggy++: Hi {name}!")
                    responded = True
        
        if not responded and name is None:
            if re.search(r'\b(hi|hello|hey|hola)\b', user_lower):
                print("Reggy++: Hello! What's your name?")
            else:
                print("Reggy++: What's your name?")
            responded = True
        
        # Ask for birthday if we have name but not age
        if responded is False and name and age is None:
            m = re.search(r'\b(birthday|born|dob|date of birth)\b', user_lower)
            date_like = (re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', user) or
                        re.search(r'\d{1,2}(?:st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', user_lower) or
                        re.search(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}', user_lower))
            if m or date_like:
                parsed = parse_birthday(user)
                if parsed:
                    age = calculate_age(parsed)
                    if age is not None and 0 <= age <= 120:
                        print(f"Reggy++: So you're {age} years old! Cool.")
                    else:
                        print("Reggy++: Hmm, that date seems off. Could you give your birthday again?")
                    responded = True
                else:
                    print("Reggy++: I couldn't quite get that date. Try formats like 15-02-2000 or 15 Feb 2000")
                    responded = True
        
        if not responded and name and age is None:
            print("Reggy++: When's your birthday? (e.g. 15-02-2000 or 15 Feb 2000)")
            responded = True
        
        # Ask for mood if we have age
        if not responded and name and age is not None and not mood_asked:
            mood = match_mood(user)
            if mood:
                mood_asked = True
                print("Reggy++:", get_mood_response(mood))
                responded = True
        
        if not responded and name and age is not None and not mood_asked:
            print("Reggy++: How are you feeling today? (happy, sad, tired, etc.)")
            responded = True
        
        # General pattern responses
        if not responded:
            for pat, resp in patterns:
                if resp and re.search(pat, user_lower):
                    print("Reggy++:", resp)
                    responded = True
                    break
        
        if not responded:
            # Check if they're giving surname info
            if re.search(r'\b(surname|last name)\s+is\s+(.+)', user_lower):
                m = re.search(r'\b(surname|last name)\s+is\s+(.+)', user_lower)
                surname = m.group(2).strip()
                print(f"Reggy++: Got it, {surname}. Thanks!")
                responded = True
            
            if not responded:
                print("Reggy++: I'm not sure I got that. Could you rephrase?")


if __name__ == "__main__":
    main()
