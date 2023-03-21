# AutoKnct

This is a web application designed to predict vehicle prices for upcoming auctions by aggregating past sales data. The application is built using Svelte for the frontend, Python in AWS Lambda with API Gateway for the backend, MongoDB for the database, and AWS Cognito for authentication.

Prerequisites

* Node.js
* Svelte
* AWS Account
* AWS CLI
* AWS Cognito User Pool and App Client

## Installation

* Clone the repository to your local machine.
* Navigate to the root directory of the project and run npm install to install the necessary dependencies for the Svelte frontend.
* Ensure that you have a MongoDB instance set up and running. You will need to have the connection string handy.
* Set up the AWS Lambda functions using Python. You will need to set up an API Gateway to route requests to the appropriate function.
* Set up an AWS Cognito User Pool and App Client for authentication.
* Start the Svelte frontend using the command npm run dev.

## Usage

* Users can sign up and log in to the application using their email and password.
* Once logged in, users can view past sales data for vehicles.
* Users can select a vehicle from the list of past sales and view its details.
* Users can also enter the details of a vehicle they are interested in selling and get a predicted price based on the past sales data.
* Users can also view upcoming auctions and predicted prices for vehicles in those auctions.

## Contributing

If you wish to contribute to this project, please fork the repository and create a pull request. Ensure that any changes made to the code are well-documented and include tests.

## License

This project is licensed under the MIT License.
