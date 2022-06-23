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
            "Expense tracking",  # Maybe remove?
            "Internet Archive Updater",
            "Learn",
            "Linux",
            "MPM bot",
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
        "Study": [
            "AI for innovation",
            "Algorithms",
            "Data mining",
            "Database",
            "Formal languages and compilers",
            "Human computer interaction",
            "Java",
            "Kuper",
            "Logic",
            "Machine learning",
            "Networks",
            "Operative systems",
            "Physics",
            "Security",
            "Software engineering 1",
            "Software engineering 2",
            "Thesis",
            "Web",
            # Non-University subjects
            "English",
            "German",
        ],
    }

    for cal, acts in act_names.items():
        df.loc[
            (df["Calendar"] == cal) & (~df["SUMMARY"].isin(acts)), "Error"
        ] = "Not categorized"
