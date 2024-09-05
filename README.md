# Bitcoin Price Analysis and Real-Time Data API

As a Data Scientist with 3 years of experience, I am expanding my skill set to include FastAPI, a modern web framework for building APIs with Python. This repository serves as my first project based on my previous work on Bitcoin Price Analysis Before the 2024 Halving. This comprehensive API provides both historical and real-time Bitcoin price analysis, designed to be a valuable resource for developers, traders and analysts. The project is built with a focus on efficiency, scalability, and reliability, using FastAPI, PostgreSQL and real-time data integration with multiple cryptocurrency exchanges.

If you find this project useful, kindly consider giving it a star ⭐ on GitHub. Contributions are also welcome as it is intended for open-source collaboration!

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the API](#running-the-api)
  - [API Endpoints](#api-endpoints)
- [Database Setup](#database-setup)
- [Real-Time Data Integration](#real-time-data-integration)
- [API Implementation and Deployment](#api-implementation-and-deployment)
- [Benefits and Applications](#benefits-and-applications)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The Bitcoin Price Analysis and Real-Time Data API offers a comprehensive solution for accessing both historical and real-time Bitcoin prices. The API is built with FastAPI, leveraging its speed and ease of use and integrates multiple cryptocurrency exchanges to provide up-to-date market data.

## Features

- **Historical Data Retrieval**: Fetch daily Bitcoin prices for any year between 2013 and 2024.
- **Real-Time Data Access**: Get the latest Bitcoin prices from major exchanges like Bybit, Binance, Kraken and Coinbase.
- **API Endpoints**: A range of endpoints for accessing Bitcoin prices, including those around halving events.
- **Scalable and Efficient**: Built with FastAPI and PostgreSQL to handle large datasets and provide fast responses.

## Technologies Used

- **FastAPI**: For building the RESTful API.
- **SQLAlchemy**: For database ORM and query management.
- **PostgreSQL**: For storing Bitcoin price data.
- **Uvicorn**: ASGI server for running the FastAPI application.

## Getting Started

### Prerequisites

- Python 3.8 or later
- PostgreSQL database
- Git


### Installation
1. **Clone the repository**:
```bash   
git clone https://github.com/yourusername/Bitcoin-Price-Analysis-API.git
cd Bitcoin-Price-Analysis-API
``` 

2. **Create a virtual environment**:
```bash

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
``` 

3. **Install the required dependencies**:
```bash
pip install -r requirements.txt
``` 

4. **Set up the PostgreSQL database**:
- Create a PostgreSQL database for the project.
- Update the DATABASE_URL in the .env file with your PostgreSQL connection string.

### Usage: Running the API
1. **Start the FastAPI server**: 
```bash
uvicorn main:app --reload
``` 

2. **Access the API documentation**: 
Open your browser and navigate to http://127.0.0.1:8000/docs to see the interactive Swagger UI documentation.


### API Endpoints
1. **Historical Data Endpoints**:
```bash
- GET /root/
Description: Provides an overview of the API, including a list of available endpoints and their descriptions.

- GET /prices/
Description: Retrieves all historical Bitcoin prices from the PostgreSQL database. Returns a JSON response containing a complete dataset of price information.

- GET /prices/{year}
Description: Fetches Bitcoin prices for a specific year by providing the year as a parameter in the URL. The API returns a JSON response with the price data for the specified year.

- GET /prices/halving/{halving_number}
Description: Provides Bitcoin price data around specific halving events. The API returns a JSON response containing Bitcoin prices before, during and after the specified halving event.
```

2. **Real-Time Data Endpoints**:
```bash
- GET /prices/bybit
Description: Fetches the latest Bitcoin price from the Bybit exchange.

-GET /prices/binance
Description: Retrieves the most recent Bitcoin price from the Binance exchange.

- GET /prices/coinbase
Description: Retrieves the current Bitcoin price from the Coinbase exchange.

- GET /prices/kucoin
Description: Retrieves the current Bitcoin price from the Kucoin exchange.
```

3. **Additional Endpoint**:
```bash
- POST /prices/add
Description: Allows adding new Bitcoin price data to the database. This endpoint requires data in JSON format, including details such as date, price and exchange.

- GET /prices/statistics
Description: Retrieves various statistics on Bitcoin prices, such as average price, highest price and lowest price over a specified period.
```

### Database Setup
- Data Acquisition: Historical Bitcoin price data is sourced from Yahoo Finance and saved as a CSV file. This data is cleaned and validated for accuracy.
- Database Initialisation: A PostgreSQL database is set up to store the historical data, enabling efficient querying and analysis.
- Database Population: Use scripts to populate the database with historical data.

### Real-Time Data Integration
The API integrates with multiple cryptocurrency exchanges (Bybit, Binance, Kucoin and Coinbase) to provide real-time Bitcoin prices. This allows for up-to-date market analysis and decision-making.

### API Implementation and Deployment
- FastAPI: Chosen for its speed and ease of use, supporting asynchronous programming, automatic documentation and data validation.
- PostgreSQL: Serves as the robust database for historical data storage ensuring data integrity and scalability.

### Benefits and Applications
- Trading: Access to historical and real-time Bitcoin data for trading strategies, backtesting and alerts.
- Data Analysis: Tools for researchers and analysts to study Bitcoin price trends and build predictive models.
- Application Development: Supports the development of cryptocurrency-related applications such as wallets and price tracking tools.

### Future Enhancements
- Additional Exchange Integrations: Expanding data sources for broader market coverage.
- Advanced Analytics: Adding features like moving averages, volatility calculations and technical indicators.
- Real-Time Charts and Visualisations: Enhancing user experience with interactive charts.
- Machine Learning Integration: Implementing models for price prediction and sentiment analysis.

### Contributing
Contributions are welcome! Please read the contributing guidelines for details on how to contribute.
```bash
- Fork the repository.
- Create a new feature branch (git checkout -b feature-name).
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature-name).
- Open a pull request.
```
### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact
For any inquiries or feedback please contact me at https://nafisalawalidris.github.io/13/.