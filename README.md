# S3 Dashboard

The S3 Dashboard provides an at-a-glance summary of Amazon S3 (Simple Storage Service) buckets and their contents. It classifies both buckets and objects as either 'public' or 'private' based on their S3 ACL (Access Control List) settings and bucket privacy policies. Specifically, it focuses on identifying publicly accessible resources, ignoring individual permissions assigned to specific AWS users.

## Getting Started

To run the project locally for development, follow these steps. The application is also deployed on PythonAnywhere and Vercel, and you can access it publicly via this URL: [S3 Dashboard](https://s3-dashboard.vercel.app/).

### Prerequisites

```bash
- Python 3.8
- Node.js 14+
- npm 9.8+
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mohamedsaad308/s3-access-monitor.git
```

2. Change to the project directory:

```bash
cd your-project

```

3. Create and activate a virtual environment for the Flask app:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Set up the backend (Flask):

```bash
cd app
pip install -r requirements.txt
python run.py
```

5. Set up the frontend (ReactJS):

```bash
Copy code
cd client
npm install
npm start
```

## Project Structure

- app: Contains the Flask backend.
  - routes.py: Define your API routes and controllers.
  - utils.py: Utility functions used by the backend.
- client: Contains the ReactJS frontend.
  - src: Source code for the frontend.
    - api: Frontend API calls.
    - components: Reusable React components.
    - pages: Main pages of your web app.
  - public: Static assets, including HTML files.
- config.py: Configuration settings for your project.
- requirements.txt: List of Python dependencies.
- run.py: Start the Flask development server.

# Usage

To use the application, start by logging in with your AWS credentials. This login grants you access to view the buckets and objects within your S3 service.

## Built With

- Flask
- ReactJS

## Notes

I'm still trying to fully understand the business case, so I've had to make some assumptions. Getting permissions can be a complex process, and to make informed decisions, I need to know how permissions are managed within our S3 service.

Currently, I have to retrieve all objects to check their permissions, which could be very time-consuming if we have a large number of objects in our buckets, potentially even millions.

From what I understand, there doesn't appear to be a direct way to retrieve only permissions without fetching all the files. Even if I tried to use paginated list object calls, it wouldn't provide a comprehensive overview of all object permissions at once.

If it's feasible, I would recommend implementing a database to store information about objects and buckets along with their permissions. This database could be periodically updated by a cron job every couple of hours, depending on our business needs, and it could be synchronized with any changes that occur.

With this approach, the S3 Dashboard would communicate with the database instead of directly querying the S3 API, which could improve efficiency and make it easier to manage permissions."
