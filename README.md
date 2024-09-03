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
