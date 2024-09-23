def load_training_data(vn):
    vn.train(
        documentation="Netflix is one of the most popular media and video streaming platforms. They have over 8000 movies or tv shows available on their platform, as of mid-2021, they have over 200M Subscribers globally. This tabular dataset consists of listings of all the movies and tv shows available on Netflix, along with details such as - cast, directors, ratings, release year, duration, etc."
    )

    vn.train(
        ddl="""
        CREATE TABLE netflix_shows (
        date_added DATE,
        release_year INTEGER,
        title TEXT,
        director TEXT,
        cast_members TEXT,
        country TEXT,
        rating TEXT,
        duration TEXT,
        listed_in TEXT,
        show_id TEXT PRIMARY KEY,
        description TEXT,
        type TEXT
        );"""
    )

    vn.train(
        question="For each decade, starting at 1980, find the number of movies shot during that decade",
        sql="""
            SELECT decade, COUNT(*) AS movie_count
            FROM (
                SELECT (release_year / 10) * 10 AS decade
                FROM netflix_shows
                WHERE type = 'Movie'
            ) AS subquery
            GROUP BY decade
            HAVING decade >= 1980
            ORDER BY decade;
        """,
    )

    vn.train(
        question=(
            "List all movies released after 2000 that were directed by Christopher Nolan. "
            "Show the title, director, release year, date added, and rating."
        ),
        sql="""
            SELECT title, director, release_year, date_added, rating
            FROM netflix_shows
            WHERE release_year > 2000
                AND director = 'Christopher Nolan'
                AND type = 'Movie';
        """,
    )

    vn.train(
        question=(
            "Find all TV shows available in the United States that have a duration of one or more seasons. "
            "Show the title, country, rating, duration, and description."
        ),
        sql="""
            SELECT title, country, rating, duration, description
            FROM netflix_shows
            WHERE country = 'United States'
                AND type = 'TV Show'
                AND duration LIKE '%Season%';
        """,
    )

    vn.train(
        question=(
            "List all titles that include Leonardo DiCaprio in the cast, were released between 2010 and 2020, "
            "and belong to the 'Action & Adventure' genre. "
            "Show the title, cast members, release year, genres, and description."
        ),
        sql="""
            SELECT title, cast_members, release_year, listed_in, description
            FROM netflix_shows
            WHERE cast_members ILIKE '%Leonardo DiCaprio%'
                AND release_year BETWEEN 2010 AND 2020
                AND listed_in LIKE '%Action & Adventure%';
        """,
    )

    vn.train(
        question=(
            "Find the number of movies and TV shows that were added to Netflix between 2020 and 2023. "
            "Show the count of each type (Movie or TV Show)."
        ),
        sql="""
            SELECT type, COUNT(*) AS count
            FROM netflix_shows
            WHERE date_added BETWEEN '2020-01-01' AND '2023-12-31'
            GROUP BY type;
        """,
    )

    vn.train(
        question=(
            "Find the top 5 countries with the highest number of movies added to Netflix after 2015. "
            "Show the country and the number of movies."
        ),
        sql="""
            SELECT country, COUNT(*) AS movie_count
            FROM netflix_shows
            WHERE release_year > 2015
                AND type = 'Movie'
            GROUP BY country
            ORDER BY movie_count DESC
            LIMIT 5;
        """,
    )

    vn.train(
        question=(
            "List all TV shows that have been listed in both 'Action & Adventure' and 'Sci-Fi & Fantasy' genres. "
            "Show the title, genres, and release year."
        ),
        sql="""
            SELECT title, listed_in, release_year
            FROM netflix_shows
            WHERE type = 'TV Show'
                AND listed_in ILIKE '%Action & Adventure%'
                AND listed_in ILIKE '%Sci-Fi & Fantasy%';
        """,
    )

    vn.train(
        question=(
            "Find the average duration (in minutes) of all movies added to Netflix between 1990 and 2000, "
            "excluding any entries that represent seasons. Show only the average duration."
        ),
        sql="""
            SELECT AVG(CAST(SPLIT_PART(duration, ' ', 1) AS INTEGER)) AS average_duration
            FROM netflix_shows
            WHERE type = 'Movie'
            AND date_added BETWEEN '1990-01-01' AND '2000-12-31'
            AND duration NOT ILIKE '%Season%';
        """,
    )

    vn.train(
        question=(
            "List all directors who have directed more than 3 movies available on Netflix in the 'Documentaries' genre. "
            "Show the director's name and the number of documentaries."
        ),
        sql="""
            SELECT director, COUNT(*) AS documentary_count
            FROM netflix_shows
            WHERE type = 'Movie'
                AND listed_in ILIKE '%Documentaries%'
            GROUP BY director
            HAVING COUNT(*) > 3;
        """,
    )

    vn.train(
        question=(
            "Find the number of unique directors who have released movies or TV shows in the 'Drama' genre on Netflix "
            "between 2010 and 2020. Show the count of unique directors."
        ),
        sql="""
            SELECT COUNT(DISTINCT director) AS unique_directors
            FROM netflix_shows
            WHERE release_year BETWEEN 2010 AND 2020
                AND listed_in ILIKE '%Drama%';
        """,
    )

    vn.train(
        question=(
            "Find the total number of actors who appeared in movies released in 2020, "
            "counting each actor only once even if they appeared in multiple movies."
        ),
        sql="""
            WITH individual_actors AS (
                SELECT UNNEST(string_to_array(cast_members, ', ')) AS actor
                FROM netflix_shows
                WHERE release_year = 2020
                    AND type = 'Movie'
            ),
            unique_actors AS (
                SELECT DISTINCT actor
                FROM individual_actors
            )
            SELECT COUNT(*) AS total_number_of_actors
            FROM unique_actors;
        """,
    )