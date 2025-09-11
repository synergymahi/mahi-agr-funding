# Mahi Crowdfunding API

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

Welcome to the backend API for the Mahi Crowdfunding platform. This API is built with FastAPI and leverages Supabase for its database and authentication services, providing a robust, secure, and scalable foundation for a modern crowdfunding application.

## ✨ Features

-   **JWT Authentication:** Secure user registration and login using Supabase Auth.
-   **Role-Based Access Control (RBAC):**
    -   **Admin (`administrateur`):** Full access to manage users and platform data.
    -   **Project Owner (`porteur de projet`):** Can create and manage their own projects.
    -   **Investor (`donateur/prêteur`):** Can view projects and contribute (future functionality).
-   **API Key Authentication:** Secure endpoints for consumption by external applications (e.g., a frontend client).
-   **Full Project CRUD:** Complete Create, Read, Update, and Delete operations for crowdfunding projects.
-   **User Profile Management:** Users can view and update their own profiles, and administrators can manage any user.
-   **Dockerized Environment:** The entire application is containerized with Docker for easy setup and deployment.
-   **Pydantic Validation:** Robust data validation and serialization using Pydantic models.

## 🚀 Tech Stack

-   **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
-   **Database & Auth:** [Supabase](https://supabase.com/) (PostgreSQL)
-   **Containerization:** [Docker](https://www.docker.com/) & Docker Compose
-   **Data Validation:** [Pydantic](https://pydantic-docs.helpmanual.io/)
-   **Password Hashing:** [Passlib](https://passlib.readthedocs.io/en/stable/)
-   **JWT Handling:** [python-jose](https://python-jose.readthedocs.io/en/latest/)

## 📂 Project Structure

```
.
├── app/
│   ├── db/
│   │   └── supabase.py       # Supabase client initialization
│   ├── routers/
│   │   ├── auth.py           # Authentication routes
│   │   ├── users.py          # User profile routes
│   │   ├── projects.py       # Project CRUD routes
│   │   └── admin.py          # Admin-only routes
│   ├── schemas/
│   │   ├── user.py           # Pydantic models for users
│   │   └── project.py        # Pydantic models for projects
│   ├── security.py           # Role and API key dependencies
│   ├── dependencies.py       # Authentication dependencies
│   └── main.py               # Main FastAPI application
├── .env.example              # Environment variable template
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose setup
└── requirements.txt          # Python dependencies
```

## ⚙️ Setup and Installation

### Prerequisites

-   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
-   A [Supabase](https://supabase.com/) account with a new project created.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd mahi-crowdfunding
```

### 2. Configure Environment Variables

Create a `.env` file by copying the example file:

```bash
cp .env.example .env
```

Now, open the `.env` file and fill in the required values from your Supabase project dashboard (**Project Settings > API**).

```env
# Your Supabase project URL
SUPABASE_URL="https://<your-project-ref>.supabase.co"

# Your Supabase anon key (publicly safe)
SUPABASE_KEY="your_supabase_anon_key"

# Your Supabase service role key (SECRET - NEVER EXPOSE)
SUPABASE_SERVICE_KEY="your_supabase_service_role_key"

# A long, random string for signing JWTs (can be generated)
JWT_SECRET="your_jwt_secret"

# A long, random string for authenticating applications
API_KEY="your_secret_api_key"
```

### 3. Set up Supabase Table

You need to create the `projects` table in your Supabase database. Go to the **SQL Editor** in your Supabase dashboard and run the following query:

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titre TEXT NOT NULL,
    description TEXT NOT NULL,
    type_financement TEXT NOT NULL,
    montant_objectif NUMERIC NOT NULL,
    montant_minimum NUMERIC,
    montant_collecte NUMERIC DEFAULT 0.0,
    montant_maximum NUMERIC,
    date_lancement DATE NOT NULL,
    date_fin DATE NOT NULL,
    duree_collecte INTEGER NOT NULL,
    statut TEXT DEFAULT 'reçu',
    secteur TEXT NOT NULL,
    localisation TEXT NOT NULL,
    tags_impact TEXT[],
    medias TEXT[],
    owner_id UUID REFERENCES auth.users(id),
    coach_id UUID,
    comite_statut TEXT DEFAULT 'en attente',
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### 4. Run the Application

Use command

uvicorn app.main:app --host 0.0.0.0 --reload

or


Use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

The API will be running at `http://localhost:8000`. You can access the interactive documentation at `http://localhost:8000/docs`.

## 📖 API Endpoints

### Authentication (`/auth`)

-   `POST /register`: Register a new user.
-   `POST /login`: Log in and receive a JWT access token.

### Users (`/users`)

-   `GET /me`: Get the current authenticated user's profile.
-   `PUT /me`: Update the current authenticated user's profile.

### Projects (`/projects`)

-   `POST /`: Create a new project.
    -   *Requires `porteur de projet` role.*
-   `GET /`: Get a list of all projects.
    -   *Requires `APP` role (API Key).*
-   `GET /{project_id}`: Get a single project by its ID.
    -   *Requires user token OR API Key.*
-   `PUT /{project_id}`: Update a project.
    -   *Requires ownership of the project.*
-   `DELETE /{project_id}`: Delete a project.
    -   *Requires ownership OR `administrateur` role.*

### Admin (`/admin`)

-   `PUT /users/{user_id}`: Update any user's profile information.
    -   *Requires `administrateur` role.*

## 💡 How to Use

1.  **Register a user** by sending a `POST` request to `/auth/register`.
2.  **Log in** by sending a `POST` request to `/auth/login` with your email and password to get an access token.
3.  **Make authenticated requests** by including the token in the `Authorization` header:
    ```
    Authorization: Bearer <your_access_token>
    ```
4.  **Make application requests** by including the API key in the `X-API-KEY` header:
    ```
    X-API-KEY: <your_api_key>
    ```