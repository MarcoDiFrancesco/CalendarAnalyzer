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
            "Preparation",
            "Shower",
        ],
        "Personal development": [
            "AI challenge",
            "Article Calendar analyzer",
            "CV",
            "Calendar analyzer",
            "Learn",
            "Linux",
            "MPM bot",
            # TODO: about 167, split in:
            # - Learn: if non-typing leraning
            # - Linux: if typing, and no projects
            "Activity Watch",
            "Android",
            "Biblioteca bot",
            "Bitwarden",
            "Cyber challenge",
            "Data visualization",
            "Heroku",
            "Internet Archive Updater",
            "Leetcode",
            "Machine learning",
            "Markdown",
            "Organization",
            "Podcast",
            "Project UnitnCal",
            "Project docker tools",
            "Python",
            "Pytorch lightning",
            "Raspberry",
            "SOI",
            "Samsung innovation",
            "Security keys",
            "Seminar machine learning",
            "Simple Wikipedia",
            "Speck and tech",
            "Twilio",
            "Ublock",
            "Unitn autologin",
            "Wathsapp analyzer",
            "Website",
            "Workshop",
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
