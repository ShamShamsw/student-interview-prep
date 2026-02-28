# Data Engineering Interview Questions

Questions covering pipelines, databases, data warehousing, distributed systems, and the engineering practices that move and transform data at scale.

---

## Databases & Storage

1. **What is the difference between OLTP and OLAP databases?**
   - _OLTP (Online Transaction Processing): optimized for fast, frequent, small read/write operations (row-oriented). Example: order management, banking._
   - _OLAP (Online Analytical Processing): optimized for complex queries over large historical datasets (column-oriented). Example: data warehouse, business intelligence._

2. **What is a columnar database? Why is it better for analytics?**
   _Stores data column-by-column instead of row-by-row. Analytics queries typically read a few columns from millions of rows — columnar storage reads only the relevant columns, uses compression efficiently, and enables vectorized processing. Examples: Redshift, BigQuery, Snowflake, DuckDB._

3. **Explain database normalization. What are 1NF, 2NF, and 3NF?**
   - _1NF: each cell holds one atomic value; no repeating groups._
   - _2NF: 1NF + every non-key attribute fully depends on the entire primary key (no partial dependency)._
   - _3NF: 2NF + no transitive dependencies (non-key attributes do not depend on other non-key attributes)._
   - _In data warehousing, denormalization is often preferred for query speed._

4. **What is the difference between a data warehouse, a data lake, and a data lakehouse?**
   - _Data Warehouse: structured, processed data in a schema-on-write model. Fast queries, governed. Examples: Snowflake, BigQuery, Redshift._
   - _Data Lake: raw data at any scale in any format (CSV, Parquet, JSON) stored cheaply in object storage. Schema-on-read. Examples: S3, Azure Data Lake._
   - _Data Lakehouse: combines lake storage with warehouse-style SQL, ACID transactions, and governance. Examples: Delta Lake, Apache Iceberg, Apache Hudi._

5. **What is a star schema vs. a snowflake schema?**
   - _Star schema: one central fact table joined to multiple flat dimension tables. Simple, fast queries, slightly redundant._
   - _Snowflake schema: dimension tables are normalized into sub-dimensions. Less storage, more joins needed._

6. **What are the different types of database indexes? When would you use each?**
   - _B-Tree: default, good for equality and range queries on ordered data._
   - _Hash: extremely fast equality lookups; cannot do range scans._
   - _Bitmap: very low cardinality columns (gender, status); efficient for data warehouses._
   - _Composite: index on multiple columns; column order matters (leftmost prefix rule)._
   - _Covering: includes all columns needed to satisfy a query without touching the base table._

7. **What is partitioning vs. sharding?**
   - _Partitioning: splitting a table into physically separate pieces on the same server (e.g., by date, region). Improves query pruning._
   - _Sharding: distributing partitions across multiple servers. Enables horizontal scaling._

8. **Explain ACID vs. BASE properties.**
   - _ACID (relational DBs): Atomicity, Consistency, Isolation, Durability. Guarantees correctness._
   - _BASE (NoSQL / distributed): Basically Available, Soft state, Eventually consistent. Trades consistency for availability and scale._

9. **What is CAP theorem?**
   _A distributed system can guarantee at most two of: Consistency (every read gets the latest write), Availability (every request gets a response), Partition Tolerance (system continues despite network splits). In practice, partition tolerance is required, so you choose between CP (Zookeeper, HBase) and AP (Cassandra, DynamoDB)._

10. **What is a slowly changing dimension (SCD)? Describe Type 1, 2, and 3.**
    - _Type 1: overwrite old value. No history kept._
    - _Type 2: add a new row with a version/date range. Full history preserved._
    - _Type 3: add a "previous value" column. Keeps one version of history._

---

## ETL / ELT & Pipelines

11. **What is the difference between ETL and ELT?**
    - _ETL (Extract, Transform, Load): transform data before loading into the warehouse. Used when the warehouse can't handle raw transformations efficiently._
    - _ELT (Extract, Load, Transform): load raw data first, transform inside the warehouse using SQL. Modern approach; leverages cloud warehouse compute power._

12. **What makes a data pipeline idempotent? Why does it matter?**
    _An idempotent pipeline produces the same result if run multiple times with the same input. Matters because network failures, retries, and re-runs are inevitable. Achieved by: using MERGE (upsert) instead of INSERT, deleting the target partition before reloading, or using surrogate keys._

13. **What are the main failure modes in a data pipeline? How do you handle them?**
    - _Source data is late: use watermarks, allow configurable delay._
    - _Schema changes break parsing: use schema evolution (Avro, Parquet), add monitoring alerts._
    - _Duplicate records: deduplicate using window functions or set-based logic._
    - _Pipeline hangs: add timeout, heartbeat checks, and alerting._
    - _Bad data quality: validate with checks (null rates, row counts, range checks) before loading._

14. **What is a DAG in the context of data pipelines?**
    _A Directed Acyclic Graph represents task dependencies in a pipeline. Each node is a task; edges define execution order. Acyclic means no circular dependencies. Used by Airflow, Dagster, Prefect to schedule and monitor pipelines._

15. **Explain Airflow's key components.**
    - _DAG: Python file defining the workflow and its schedule._
    - _Operator: a single task (BashOperator, PythonOperator, BigQueryOperator, etc.)._
    - _Task Instance: a specific run of an operator for a given execution date._
    - _Scheduler: parses DAGs and creates task instances._
    - _Executor: runs tasks (SequentialExecutor, LocalExecutor, CeleryExecutor, KubernetesExecutor)._
    - _XCom: lightweight mechanism to pass data between tasks._

16. **What is the difference between batch processing and stream processing?**
    - _Batch: processes bounded chunks of data on a schedule (hourly, daily). Higher latency, simpler logic. Tools: Spark, dbt, SQL._
    - _Streaming: processes unbounded events in real time as they arrive. Low latency. Tools: Kafka Streams, Flink, Spark Structured Streaming._

17. **What is dbt? What problem does it solve?**
    _dbt (data build tool) brings software engineering practices (version control, testing, documentation, modular design) to SQL-based data transformations inside the warehouse. Models are `.sql` SELECT statements; dbt handles dependency ordering and materialization (view, table, incremental, ephemeral)._

18. **What is an incremental model? Why is it important?**
    _An incremental model only processes new or changed data since the last run, rather than reprocessing the entire table. Critical for large tables where full refresh is too slow or expensive. Requires a `unique_key` for upsert logic and a `updated_at` or event timestamp column._

---

## Data Quality & Observability

19. **What data quality dimensions do you test in a pipeline?**
    - _Completeness: no unexpected nulls, row counts in expected range._
    - _Uniqueness: no duplicate primary keys._
    - _Timeliness: data arrived within expected SLA._
    - _Validity: values within expected ranges or in valid enum sets._
    - _Consistency: same metric computed the same way across systems._
    - _Referential integrity: foreign keys resolve in dimension tables._

20. **What is data observability?**
    _The ability to understand the health of your data pipelines at all times — detecting schema changes, volume anomalies, freshness failures, and field-level anomaly detection. Tools: Monte Carlo, Great Expectations, dbt tests, Soda._

21. **How do you detect and handle data drift?**
    _Monitor summary statistics (mean, std, null rate, cardinality) of key columns over time. Alert when they deviate beyond a threshold. Handle by: re-running the upstream pipeline, alerting data consumers, or tagging the affected period in the warehouse._

---

## Cloud & Infrastructure

22. **What is object storage? How is it different from a traditional filesystem?**
    _Object storage (S3, GCS, Azure Blob) stores data as immutable objects with metadata and a flat namespace. No directory hierarchy (paths are prefixes). Extremely cheap at scale, highly durable, but higher latency than local filesystem. Ideal for a data lake._

23. **What is Parquet? Why is it preferred over CSV for data engineering?**
    _Apache Parquet is a columnar binary file format. Benefits over CSV: column pruning (read only needed columns), predicate pushdown (skip row groups outside filter range), compression (Snappy, GZIP, ZSTD), schema embedded in file, no type ambiguity. Typically 5–10× smaller than equivalent CSV._

24. **What is Apache Kafka? Describe producers, consumers, topics, and partitions.**
    - _Topic: a named stream of records, like a database table._
    - _Partition: a topic is divided into partitions; each partition is an ordered, immutable log. Enables parallelism._
    - _Producer: writes records to a topic._
    - _Consumer: reads records from a topic, tracked by offset._
    - _Consumer Group: multiple consumers sharing the work of consuming a topic._

25. **What is Apache Spark? When would you use it over pandas?**
    _Spark is a distributed data processing framework. Use when: data doesn't fit in memory (>10 GB), joining or aggregating across very large tables, or running batch ML at scale. Use pandas for < 1 GB interactive analysis where single-machine speed is fine._

26. **What is the difference between Spark RDD, DataFrame, and Dataset?**
    - _RDD (Resilient Distributed Dataset):  low-level, untyped, functional API — rarely used in new code._
    - _DataFrame: distributed table with named columns; uses Catalyst optimizer; equivalent to pandas but distributed._
    - _Dataset: typed DataFrame (Scala/Java only); compile-time type safety._

27. **What is data partitioning in Spark? How do you control it?**
    _Spark splits data across worker nodes into partitions. Use `repartition(n)` to increase partitions (full shuffle), `coalesce(n)` to decrease (no full shuffle). Partition on commonly filtered columns (e.g., date) to enable partition pruning._

---

## Data Modeling & Architecture

28. **What is a fact table vs. a dimension table?**
    - _Fact table: records of events / measurements (orders, page views, transactions). Contains foreign keys to dimensions and numeric measures._
    - _Dimension table: descriptive context (customers, products, dates, geography). Contains attributes used for filtering and grouping._

29. **What is grain in a data model?**
    _The level of detail each row represents. Example: "one row per customer per day" or "one row per order line item." Defining grain is the first and most critical step in designing a fact table._

30. **What is a surrogate key vs. a natural key?**
    - _Natural key: a real-world identifier (email, SSN, order number). Can change or be reused._
    - _Surrogate key: a system-generated integer or UUID with no business meaning. Stable, smallerfor joins, safer for SCD Type 2._

31. **What is the medallion architecture (Bronze / Silver / Gold)?**
    - _Bronze: raw ingested data, exactly as received from the source. Immutable._
    - _Silver: cleaned, validated, deduplicated. Conformed types, standard naming._
    - _Gold: business-level aggregates and models ready for analysts, BI tools, and ML._

32. **What is semantic layer / metrics layer?**
    _A centralized layer (MetricFlow, Cube.dev, LookML) that defines business metrics consistently once and serves them to any BI tool or query. Prevents "metric sprawl" where the same metric is computed differently in 5 different dashboards._

---

## Python for Data Engineering

33. **What Python libraries do data engineers commonly use?**
    - _`pandas` / `polars`: in-memory data manipulation._
    - _`pyspark`: distributed Spark in Python._
    - _`SQLAlchemy`: database connections and ORM._
    - _`psycopg2` / `pymysql`: raw database drivers._
    - _`boto3`: AWS SDK for S3, Glue, etc._
    - _`apache-airflow`: pipeline orchestration._
    - _`great_expectations` / `soda-core`: data quality testing._
    - _`dbt-core`: SQL transformation framework._
    - _`pyarrow`: read/write Parquet, Arrow IPC._
    - _`fastparquet` / `pyarrow`: Parquet I/O._

34. **How do you efficiently write a large pandas DataFrame to a database?**
    ```python
    # Slow — sends row-by-row
    df.to_sql("table", con=engine)

    # Fast — bulk COPY via psycopg2 for PostgreSQL
    from io import StringIO
    import psycopg2

    buf = StringIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)
    with psycopg2.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.copy_from(buf, "table", sep=",", columns=df.columns)

    # Even faster for analytics — write Parquet directly to S3
    df.to_parquet("s3://bucket/prefix/file.parquet", engine="pyarrow")
    ```

35. **What is connection pooling? Why does it matter in a pipeline?**
    _Reusing database connections instead of creating a new one per query. Creating a connection is expensive (~50–200 ms). In a pipeline that runs thousands of queries, connection creation overhead becomes significant. Use SQLAlchemy's `create_engine(pool_size=10)` or pgBouncer for PostgreSQL._

36. **How do you run SQL queries with parameterized inputs safely?**
    ```python
    # NEVER use string formatting — SQL injection risk
    query = f"SELECT * FROM users WHERE email = '{user_input}'"  # BAD

    # Use parameterized queries
    cur.execute("SELECT * FROM users WHERE email = %s", (user_input,))  # psycopg2
    pd.read_sql("SELECT * FROM users WHERE email = :email", con=engine,
                params={"email": user_input})                           # SQLAlchemy
    ```

---

## SQL for Data Engineering (Advanced)

37. **How do you implement an upsert (INSERT or UPDATE) in SQL?**
    ```sql
    -- PostgreSQL: INSERT ... ON CONFLICT
    INSERT INTO employees (id, name, salary, updated_at)
    VALUES (123, 'Alice', 95000, NOW())
    ON CONFLICT (id)
    DO UPDATE SET
        name       = EXCLUDED.name,
        salary     = EXCLUDED.salary,
        updated_at = EXCLUDED.updated_at;

    -- BigQuery: MERGE statement
    MERGE target_table T
    USING source_table S ON T.id = S.id
    WHEN MATCHED THEN UPDATE SET T.salary = S.salary
    WHEN NOT MATCHED THEN INSERT (id, name, salary) VALUES (S.id, S.name, S.salary);
    ```

38. **How do you detect duplicate records in a large table?**
    ```sql
    -- Find exact duplicates
    SELECT email, COUNT(*) AS cnt
    FROM users
    GROUP BY email
    HAVING COUNT(*) > 1;

    -- Keep only the latest record per email
    WITH deduped AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated_at DESC) AS rn
        FROM users
    )
    DELETE FROM users WHERE id IN (SELECT id FROM deduped WHERE rn > 1);
    ```

39. **What is query optimization? How do you approach a slow query?**
    1. `EXPLAIN ANALYZE` — read the query plan, find the most expensive node.
    2. Check for sequential scans on large tables → add an index.
    3. Check for nested loop joins on large tables → ensure join columns are indexed.
    4. Avoid `SELECT *` — fetch only needed columns.
    5. Push filters down (earlier `WHERE` = fewer rows processed).
    6. Rewrite correlated subqueries as JOINs or window functions.
    7. Materialize intermediate results with CTEs or temp tables if reused.
    8. Partition large tables and use partition pruning.
