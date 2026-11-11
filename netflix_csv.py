"""Netflix CSV analytics mini-project: extract, validate, transform, analyze, load."""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent


def extract_data():
    """Read the three CSV files from the project folder."""
    movies = pd.read_csv(BASE_DIR / "movies.csv")
    users = pd.read_csv(BASE_DIR / "users.csv")
    history = pd.read_csv(BASE_DIR / "watchhistory.csv")
    return movies, users, history


def transform_data(movies, users, history):
    """Validate IDs and ratings, then join viewing records with users and movies."""
    if movies["movie_id"].duplicated().any() or users["user_id"].duplicated().any():
        raise ValueError("Movie IDs and user IDs must be unique in their CSV files.")
    if not history["rating"].between(1, 5).all():
        raise ValueError("Ratings must be between 1 and 5.")
    if history.isna().any().any():
        raise ValueError("Watch history contains missing values.")

    result = history.merge(users, on="user_id", how="left", validate="many_to_one")
    result = result.merge(movies, on="movie_id", how="left", validate="many_to_one")
    if result[["name", "title"]].isna().any().any():
        raise ValueError("Some watch-history IDs are missing from users.csv or movies.csv.")
    return result


def analyze_data(result):
    """Answer common Netflix viewing analytics questions."""
    print("\n=== COMPLETE WATCH HISTORY ===")
    print(result.to_string(index=False))

    print("\nTotal viewing events:", len(result))
    print("Unique movies watched:", result["movie_id"].nunique())
    print("Most active user:", result.groupby("name").size().idxmax())

    average_ratings = result.groupby("title")["rating"].mean().sort_values(ascending=False)
    print("\nAverage rating per movie:\n", average_ratings)
    print("Highest average-rated movie:", average_ratings.idxmax())

    genre_ratings = result.groupby("genres")["rating"].mean().sort_values(ascending=False)
    print("\nAverage rating per genre:\n", genre_ratings)

    print("\nUsers who watched The Matrix:")
    print(result.loc[result["title"] == "The Matrix", "name"].tolist())

    print("\nMovies watched by Ada:")
    print(result.loc[result["name"] == "Ada", "title"].tolist())

    print("\nMovies watched by 2 or more different users:")
    movie_counts = result.groupby("title")["user_id"].nunique()
    print(movie_counts[movie_counts >= 2])

    print("\nUsers who watched more than 2 different movies:")
    user_counts = result.groupby("name")["movie_id"].nunique()
    print(user_counts[user_counts > 2])


def load_data(result):
    """Save the merged results to a new CSV file."""
    output_path = BASE_DIR / "netflix_results.csv"
    result.to_csv(output_path, index=False)
    print(f"\nSaved merged data to: {output_path.name}")


def main():
    movies, users, history = extract_data()
    result = transform_data(movies, users, history)
    analyze_data(result)
    load_data(result)


if __name__ == "__main__":
    main()
