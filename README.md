# Oracle Database Query API

This project provides a simple API to execute queries on an Oracle database.

## Description

This API allows users to send SQL queries to an Oracle database and retrieve the results in JSON format. It is built using Flask and connects to the Oracle database using the `oracledb` library.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/oracle-query-api.git
    cd oracle-query-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Environment Variables

The following environment variables need to be set:

- `ORACLE_HOST`: The hostname of the Oracle database.
- `ORACLE_PORT`: The port number of the Oracle database.
- `ORACLE_SERVICE_NAME`: The service name of the Oracle database.
- `ORACLE_USER`: The username for the Oracle database.
- `ORACLE_PASSWORD`: The password for the Oracle database.

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Make a POST request to the `/consulta` endpoint with a JSON body containing the SQL query:
    ```json
    {
        "query": "SELECT * FROM your_table"
    }
    ```

## Docker Compose

You can also run the application using Docker Compose.

1. Ensure you have Docker and Docker Compose installed.
2. Create a `.env` file in the project root with the following content:
    ```env
    ORACLE_HOST=your_oracle_host
    ORACLE_PORT=your_oracle_port
    ORACLE_SERVICE_NAME=your_oracle_service_name
    ORACLE_USER=your_oracle_user
    ORACLE_PASSWORD=your_oracle_password
    ```
3. Build and run the services:
    ```sh
    docker-compose up --build
    ```

## Endpoints

- `POST /consulta`: Executes the provided SQL query and returns the results.

## Error Handling

- If the `query` parameter is missing, the API returns a 400 status code with an error message.
- If there is a connection issue with the Oracle database, the API returns a 500 status code with an error message.
- If there is an error executing the query, the API returns a 500 status code with the error message.

## Dependencies

- Flask
- oracledb

## License

This project is licensed under the MIT License.