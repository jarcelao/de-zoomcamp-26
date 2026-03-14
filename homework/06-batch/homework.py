import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
    """)
    return


@app.cell
def _():
    import os

    from pathlib import Path
    from typing import List, Union

    import marimo as mo

    from pyspark.sql import SparkSession

    return List, Path, SparkSession, Union, mo, os


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answers
    """)
    return


@app.cell
def _(SparkSession):
    # Q1

    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("06-batch")
        .getOrCreate()
    )
    print(spark.version)
    return (spark,)


@app.cell
def _(spark):
    # Q2

    yellow_df = spark.read.parquet("data/yellow_tripdata_2025-11.parquet")
    yellow_df.show()
    return (yellow_df,)


@app.cell
def _(yellow_df):
    yellow_df_partitioned = yellow_df.repartition(4)
    yellow_df_partitioned.write.parquet("data/yellow_tripdata_partitioned/", mode="overwrite")
    return


@app.cell
def _(List, Path, Union, os):
    def get_average_dir_size(path: Union[str, Path]) -> float:
        sizes: List[int] = []

        for dirpath, _, filenames in os.walk(path):
            for name in filenames:
                if name.endswith(".parquet"):
                    filepath = os.path.join(dirpath, name)
                    filesize = os.path.getsize(filepath)
                    sizes.append(filesize)

        if len(sizes) == 0:
            raise ValueError("No files found in path")

        return sum(sizes) / len(sizes)

    # bytes to MB
    print(get_average_dir_size("data/yellow_tripdata_partitioned/") / 1000000)
    return


@app.cell
def _(yellow_df):
    # Q3

    yellow_df.createOrReplaceTempView("yellow_df")
    return


@app.cell
def _(spark):
    q3_query = """
        SELECT
            COUNT(*)
        FROM
            yellow_df
        WHERE
            TO_DATE(tpep_pickup_datetime) = '2025-11-15';
    """

    spark.sql(q3_query)
    return


@app.cell
def _(spark):
    # Q4

    q4_query = """
        SELECT
            MAX(
                (unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 60 / 60
            ) AS max_trip_length
        FROM
            yellow_df;
    """

    spark.sql(q4_query)
    return


@app.cell
def _(spark):
    # Q6

    lookup_df = spark.read.csv("data/taxi_zone_lookup.csv", header=True)
    lookup_df.show()
    return (lookup_df,)


@app.cell
def _(lookup_df):
    lookup_df.createOrReplaceTempView("lookup_df")
    return


@app.cell
def _(spark):
    q6_query = """
        SELECT
            y.DOLocationID AS DoLocationID,
            l.Zone AS Zone,
            COUNT(y.DoLocationID) AS dropoff_count
        FROM
            yellow_df y
        JOIN
            lookup_df l
            ON
            y.DOLocationID = l.LocationID
        GROUP BY
            y.DOLocationID, l.Zone
        ORDER BY
            dropoff_count ASC
        LIMIT
            1;
    """

    spark.sql(q6_query)
    return


if __name__ == "__main__":
    app.run()
