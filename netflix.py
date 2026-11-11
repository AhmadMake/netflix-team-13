
import logging
from collections import Counter

# Bonus: Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


# Classes
class Movie:
    def __init__(self, movie_id, title, genre):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name


class WatchHistory:
    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating


# Part 1: Extract
def extract_data():
    logging.info("Extracting data...")

    movies = [
        Movie(1, "The Matrix", "Sci-Fi"),
        Movie(2, "Inception", "Sci-Fi"),
        Movie(3, "Interstellar", "Sci-Fi")
    ]

    users = [
        User(101, "Ada"),
        User(102, "Charles"),
        User(103, "Linus")
    ]

    history = [
        WatchHistory(101, 1, 5),
        WatchHistory(101, 2, 4),
        WatchHistory(102, 1, 5),
        WatchHistory(103, 3, 5),
        WatchHistory(103, 1, 4),
        WatchHistory(103, 2, 3)
    ]

    return movies, users, history


# Part 2: Transform
def transform_data(movies, users, history):
    logging.info("Transforming data...")

    total_events = len(history)

    average_rating = (
        sum(record.rating for record in history) / total_events
        if total_events else 0
    )

    movie_counts = Counter(
        record.movie_id for record in history
    )

    user_counts = Counter(
        record.user_id for record in history
    )

    movie_names = {
        movie.movie_id: movie.title for movie in movies
    }

    user_names = {
        user.user_id: user.name for user in users
    }

    most_watched = (
        movie_names[movie_counts.most_common(1)[0][0]]
        if movie_counts else "None"
    )

    most_active = (
        user_names[user_counts.most_common(1)[0][0]]
        if user_counts else "None"
    )

    ranking = [
        f"{movie_names[movie_id]} ({count} views)"
        for movie_id, count in movie_counts.most_common()
    ]

    report = {
        "Total Watch Events": total_events,
        "Average Rating": round(average_rating, 2),
        "Most Watched Movie": most_watched,
        "Most Active User": most_active,
        "Active Users": len(user_counts),
        "Movie Popularity Ranking": ranking
    }

    return report


# Part 3: Load
def load_report(report):
    logging.info("Saving report...")

    lines = [
        "NETFLIX VIEWING ANALYTICS REPORT",
        "================================"
    ]

    for key, value in report.items():
        if key == "Movie Popularity Ranking":
            lines.append("\nMovie Popularity Ranking:")
            for position, movie in enumerate(value, start=1):
                lines.append(f"{position}. {movie}")
        else:
            lines.append(f"{key}: {value}")

    report_text = "\n".join(lines)

    print("\n" + report_text)

    with open("netflix_report.txt", "w", encoding="utf-8") as file:
        file.write(report_text)

    logging.info("Report saved to netflix_report.txt")


# Part 4: Complete Pipeline
def main():
    movies, users, history = extract_data()
    report = transform_data(movies, users, history)
    load_report(report)


if __name__ == "__main__":
    main()
