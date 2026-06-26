from src.extract import extract_movies


def test_extract():
    df = extract_movies()

    print(df.head())
    print(df.shape)


if __name__ == "__main__":
    test_extract()