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
            "Gaming",
            "Movie",
            "TV",
            "Twitch",
            "YouTube",
        ],
        "Personal care": [
            "Hair cut",
            # TODO: move 180 instances of Preparation to:
            # - “Preparation” close to breakfast → “Breakfast”
            # - “Preparation” far from breakfast → “Tidy up”
            # "Preparation",
            "Shower",
        ],
        "Personal development": [
            "Activity Watch",
            "AI challenge",
            "Calendar analyzer",
            "CV",
            "Internet Archive Updater",
            "Learn",
            "Linux",
            "MPM bot",
            "Simple Wikipedia",
            "SOI",
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
            # TODO: put the ones I didn't do an exam into personal development
            # Undestand if it's better to put everything to learn, or separate them.
            # Note: German shoud be anyway separated, but merge English into Learn
            "AI for innovation",
            "Algorithms",
            "Autonomous software agents",
            "Computer vision",
            "Data mining",
            "Database",
            "English",
            "Finance",
            "Formal languages and compilers",
            "German",
            "Human computer interaction",
            "Java",
            "Kuper",
            "Logic",
            "Machine learning",
            "Natural language understanding",
            "Networks",
            "Operative systems",
            "Physics",
            "Security",
            "Software engineering 1",
            "Software engineering 2",
            "Thesis",
            "Web",
        ],
    }

    for cal, acts in act_names.items():
        # TODO: check if an empty activity is given as error
        df.loc[
            (df["Calendar"] == cal) & (~df["SUMMARY"].isin(acts)), "Error"
        ] = "Not categorized"
        # print(set(df.loc[df["Calendar"] == "Work"]["SUMMARY"].tolist()))
