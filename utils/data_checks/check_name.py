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
            "Clean",
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
            "Social media",
            "TV",
            "Twitch",
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
            "Expense tracking",  # TODO: maybe remove?
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
            # TODO: undestand if it's better to put only courses without exams
            # to learn, or separate them.
            # Note: German shoud be anyway separated, but merge English into Learn.
            "Autonomous software agents",
            "Computer vision",
            "English",
            "Finance",
            "German",
            "Natural language understanding",
        ],
    }

    for cal, acts in act_names.items():
        df.loc[
            (df["Calendar"] == cal) & (~df["SUMMARY"].isin(acts)), "Error"
        ] = "Not categorized"
