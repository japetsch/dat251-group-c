# Blood app backend

This is a description of the backend stack, and how to work within it.

First comes a listing of the individual components and what they do in the project, with comparisons to Java.
Then, a guide on how to set up the backend locally for your own development purposes.
Finally, a step-by-step guide to developing a new feature in the backend.

## Components

| Component  | Java equivalent    | Purpose                                                           |
|------------|--------------------|-------------------------------------------------------------------|
| FastAPI    | Spring Boot        | Application framework for building restful APIs                   |
| sqlc       | Hibernate          | Connecting database queries to typed entities in application code |
| dbmate     | Liquibase / flyway | Versioning the database schema together with code                 |
| pytest     | JUnit              | Testing framework (unit and integration)                          |
| uv         | Gradle / maven     | Package manager (for software dependencies)                       |
| PostgreSQL | -                  | Database                                                          |

The most unique part of this setup is the usage of `sqlc` and `dbmate`.
These are programs originally from the Go ecosystem, for managing your relational database using **pure SQL**.
The idea is that this gives you the best of both worlds:
Deep integration with the database in application code in the form of typed calls to the database,
without the leaky abstraction of specifying the schema and queries as application code.

## Development setup

Make sure you have Python 3.14 installed with `python --version`. If you have an older version, update it.

Install `uv`, `sqlc`, and `dbmate`:
- MacOS: `brew install uv sqlc dbmate`
- Ubuntu (for example in Windows WSL):
  - `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - `sudo apt install golang curl`
  - `go install github.com/sqlc-dev/sqlc/cmd/sqlc@v1.30.0`
  - `sudo mv ~/go/bin/sqlc /usr/local/bin`
  - `sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64`
  - `sudo chmod +x /usr/local/bin/dbmate`
- Other Linux-es might have them in their package managers, or can follow similar instructions

In the project directory (`dat251-group-c/backend`),
create a virtual environment and install dependencies with: `uv sync`.

Make sure you have a Postgres database running. This can be spun up fast with Docker:
`docker run --name postgres -d -p 127.0.0.1:5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=bloodbank postgres:18-alpine`

Create our tables in the postgres database with: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bloodbank?sslmode=disable dbmate up`.
If you didn't use the Docker-command you might need to change the username and password in this connection string.

Create a configuration file name `.env` in the `backend` directory. If you use the Docker command for Postgres, insert the following content into it:
```.env
DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bloodbank
TEST_DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bloodbank_test
```

### Running the app

Now, everything is ready for you to run the app!
`uv run uvicorn app.main:app --port 8000 --reload`

Go to http://localhost:8000/docs in the browser to verify it is running and see the API docs.

### Other useful commands

- Run the tests with `uv run pytest`
- Open a shell where you can execute SQL statements for local testing:
  `docker exec -it postgres psql --user postgres --password bloodbank`.
  Enter `postgres` as a password in the prompt that will appear.
- Format the code with `uv run isort app tests` and `uv run black app tests`.

## Suggested workflow for adding a new feature

The following is a walkthrough of how to add a new feature to the backend.
I recommend reading every point to understand how the components fit together.

When actually implementing a feature, you only need to concern yourself with the points where
the answer to the question is *yes*.

### Do you need to change the database schema?

Consider if your new feature needs to add more tables,
fields to existing tables, or in other ways change the current database schema.

If it is the case that you do need to change the schema, you need to interact with `dbmate`.
We call changing the database schema a "migration". Every migration is stored in its own separate file,
in the `db/migrations` directory.

A migration has two parts: "up" and "down". The first is for making the change, the other for undoing it.
To create a migration file, run `dbmate new give_the_name_of_your_change_here`.
This should create a file in the migrations directory, with a timestamp and your chosen name.

In the migrations file, write SQL DDL statements under the `-- dbmate:up` comment for making your changes to the database
(creating tables, indexes, changing fields, etc.).
Under the `-- dbmate:down` comment, write statements that change the schema back
(dropping tables, indexes, changing fields to their originals, etc.).

To run your migration against your local database, do:
`DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bloodbank?sslmode=disable dbmate up`.

You might want to write your migration as an iterative process.
This is why you make the undo statements. To undo the latest migration run, use:
`DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bloodbank?sslmode=disable dbmate down`.

### Do you need to add more database queries?

If your feature requires a new pattern of extracting or adding data to the database,
you need to write one or more SQL queries for it.

This is done in the files under `db/queries`:
- Add your query to the file in which you feel it fits the best.
  It should have a comment above it on the form `-- name: MyAwesomeQueryName :many`.
  If the query does not return many rows, write either `:one` (returns only one row)
  or `:exec` (returns no rows) instead of `:many`.
- Run `sqlc generate`
- The file under `app/db/sqlc/` matching the name of the file where you put your query
  should now be updated with a (typed) function for calling your query.

### Are you adding a new route to the API?

Check the existing routes in the API by running the application and going to http://localhost:8000/docs.

Consider whether it fits within the existing controllers in `app/routes`.
If it does not, create a new file with a controller housing your route by copying another router and removing its methods.

Your route should be an asyncronous instance method on the class.
It takes parameters according to its dependencies (e.g. database connection), and input data from the user.
Refer to FastAPI documentation for how to write these methods.

The unique thing about this project is it's object-oriented style. This means that routes have to be *class methods*,
taking in `self` (reference to its object) as the first parameter.

You can also not use FastAPI annotations (like `@app.get("/")`) to specify the path the route lives on.
Instead, it is mounted to the router in the router class constructor (`__init__`-method), like this:
```python
self.add_api_route("", self.find_all, methods=["GET"])
```

### Are you changing an existing route to the API?

Check the existing routes in the API by running the application and going to http://localhost:8000/docs.

Locate the method handling the route you desire to change within its class in `app/routers`.
Change the code appropriately.
Refer to FastAPI documentation for how to write these methods.

### Is your route calling a database query?

SQLc generates a class for each file in `db/queries`, that have a method per query in the file.
These methods have typed inputs and outputs, allowing you to interact with the database through Python code.
These classes all have names ending in -`Querier`.

When using these classes, they need to be constructed with a database connection as their input parameter.

The following is an example FastAPI route method, that takes in a database connection as a dependency:
```python
async def find_all(self, engine: DBConnection) -> list[GetAllAppointmentsRow]:
    q = AppointmentQuerier(engine)

    rows: list[GetAllAppointmentsRow] = []
    async for x in q.get_all_appointments():
        rows.append(x)

    return rows
```

AppointmentQuerier takes in the database connection when constructed.
We can then call the `get_all_appointments()`-method on the constructed object to receive an
asynchronous iterator of appointments, to use in our code.

Here, `get_all_appointments` is a query specified in the underlying sqlc query file in `db/queries`.

### Remember to write tests!

Tests are found in the `tests/`-directory.
As of writing, there are only integration tests, and these are organized by the router they test.

Add to the appropriate testing file, a method to the class, testing your feature.
Make sure you create a `TestClient` in the same way as the other tests. Use this for querying the API.

Be mindful that a test run starts with a fresh database every time.
Your integration test might need to insert data to the database.

Run tests with `uv run pytest`
