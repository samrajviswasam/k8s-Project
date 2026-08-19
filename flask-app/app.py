import os
import logging
from datetime import datetime, timezone

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

APP_NAME = os.getenv("APP_NAME", "DevOps Kubernetes Platform")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATABASE_URL = os.getenv("DATABASE_URL")

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Utility
# --------------------------------------------------

def current_timestamp():
    return datetime.now(timezone.utc).isoformat()


def check_db_connection():
    """
    Check whether PostgreSQL is reachable.
    A short timeout prevents the API from hanging
    if PostgreSQL is unavailable.
    """

    if not DATABASE_URL:
        logger.warning("DATABASE_URL is not configured")
        return False

    try:
        connection = psycopg2.connect(
            DATABASE_URL,
            connect_timeout=3
        )

        connection.close()

        return True

    except Exception as error:
        logger.error("Database connection failed: %s", error)

        return False


# --------------------------------------------------
# Root API
# --------------------------------------------------

@app.route("/")
def index():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "status": "running",
        "message": "DevOps backend API is running",
        "timestamp": current_timestamp(),
        "endpoints": {
            "health": "/health",
            "readiness": "/ready",
            "status": "/api/status",
            "info": "/api/info",
            "database": "/api/db-status"
        }
    })


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/health")
def health():
    """
    Kubernetes liveness probe.

    Only checks whether Flask itself is running.
    It does NOT check PostgreSQL.
    """

    return jsonify({
        "status": "healthy",
        "service": "flask",
        "timestamp": current_timestamp()
    }), 200


# --------------------------------------------------
# Readiness Check
# --------------------------------------------------

@app.route("/ready")
def ready():
    """
    Kubernetes readiness probe.

    Flask is ready only when PostgreSQL is reachable.
    """

    if check_db_connection():

        return jsonify({
            "status": "ready",
            "service": "flask",
            "database": "connected",
            "timestamp": current_timestamp()
        }), 200

    return jsonify({
        "status": "not ready",
        "service": "flask",
        "database": "not connected",
        "timestamp": current_timestamp()
    }), 503


# --------------------------------------------------
# Application Information
# --------------------------------------------------

@app.route("/api/info")
def application_info():

    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "framework": "Flask",
        "language": "Python",
        "containerized": True,
        "orchestration": "Kubernetes",
        "timestamp": current_timestamp()
    })


# --------------------------------------------------
# Database Status
# --------------------------------------------------

@app.route("/api/db-status")
def database_status():

    connected = check_db_connection()

    return jsonify({
        "service": "postgresql",
        "status": "connected" if connected else "disconnected",
        "timestamp": current_timestamp()
    }), 200 if connected else 503


# --------------------------------------------------
# Overall Application Status
# --------------------------------------------------

@app.route("/api/status")
def application_status():

    database_connected = check_db_connection()

    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "application_status": "running",
        "database_status": (
            "connected"
            if database_connected
            else "disconnected"
        ),
        "overall_status": (
            "healthy"
            if database_connected
            else "degraded"
        ),
        "timestamp": current_timestamp()
    }), 200 if database_connected else 503


# --------------------------------------------------
# Error Handling
# --------------------------------------------------

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "timestamp": current_timestamp()
    }), 404


@app.errorhandler(500)
def internal_error(error):

    logger.exception("Internal server error")

    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "timestamp": current_timestamp()
    }), 500


# --------------------------------------------------
# Application Startup
# --------------------------------------------------

if __name__ == "__main__":

    logger.info(
        "Starting %s version %s",
        APP_NAME,
        APP_VERSION
    )

    logger.info(
        "Environment: %s",
        ENVIRONMENT
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
