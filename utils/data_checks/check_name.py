import pandas as pd


def check_name(df: pd.DataFrame) -> None:
    """Check for each calendar if activity is one of the list."""
    act_names = {
        "Commute": [
            "Bike",
            "Bus",
            "Car",
            "Train",
            "Walk",
        ],
        "Chores": [
            "Organization",
            "Shop",
            "Tidy up",
        ],
        "Eat": [
            "Breakfast",
            "Lunch",
            "Dinner",
        ],
        "Entertainment": [
            "Cinema",
            "Game",
            "Movie",
            "TV",
            "YouTube",
        ],
        "Personal care": [
            "Hair cut",
            "Shower",
        ],
        "Personal development": [
            "Activity Watch",
            "AI challenge",
            "Calendar analyzer",
            "CV",
            "EIT Kick-Off",
            "Expense tracking",  # Maybe remove?
            "Internet Archive Updater",
            "Learn",
            "Linux",
            "MPM bot",
            "Kide bot",
            "Simple Wikipedia",
            "Unitn autologin",
            "Website",
        ],
        "Spare time": [
            "Call Susanna",
            "Memories",
            "Phone",
            "Relax",
            "Sleep",
            "Talk",
        ],
        "Sport": [
            "Beach volleyball",
            "Bike",
            "Ping pong",
            "Run",
            "Ski",
            "Workout",
        ],
        "Work": [
            "DSH Website",
            "FBK",
            "Internship",
            "Kidney",
            "Meteo TN",
            "WebValley",
        ],
        "Study": unpack_dict(study_subjects()),
    }

    for cal, acts in act_names.items():
        df.loc[
            (df["Calendar"] == cal) & (~df["SUMMARY"].isin(acts)), "Error"
        ] = "Not categorized"


def study_subjects():
    return {
        "Bachelor": [
            "Algorithms",
            "Formal languages and compilers",
            "Human computer interaction",
            "Machine learning",
            "Operative systems",
            "Physics",
            "Software engineering 2",
            "Thesis",
            "Web",
        ],
        "Master": [
            "AI for innovation",
            "Complex networks",
            "Reinforcement",
            "Supervised",
            "Business",
            "Data mining",
        ],
        "Other": [
            "English",
            "German",
            # Studied also before Dec 2019
            "Database",  # Lectures and assignments
            "Java",  # Attended lectures
            "Kuper",  # Attended lectures
            "Logic",  # Attended lectures
            "Networks",  # Attended lectures
            "Security",  # Exam on Jan 2020
            "Software engineering 1",  # Exam on Jan 2020
        ],
    }


def unpack_dict(d: dict) -> list:
    """Unpack dict of lists to single list.

    From:
    {
        "Element1": [
            "A",
            "B",
        ],
        "Element2": [
            "C",
            "D",
        ],
    }
    To:
    ["A", "B", "C", "D"]

    Args:
        d (dict): dict of lists

    Returns:
        list: single list
    """

    ls = [d[a] for a in d]
    # From [[1, 2], [m3, 4]]
    # To   [1, 2, 3, 4]
    ls = [item for sublist in ls for item in sublist]
    return ls
