#!/bin/bash

# API Security Validation Test Runner
# This script runs tests in groups to avoid rate limiting issues

echo "================================================"
echo "API Security Validation Framework - Test Runner"
echo "================================================"
echo ""

# Clear MongoDB test database
echo "Cleaning test database..."
mongosh --quiet --eval "db.getSiblingDB('test_database').dropDatabase()" > /dev/null 2>&1

# Create test reports directory
mkdir -p /app/test_reports

echo "Running test suite..."
echo ""

# Run authentication tests
echo "1. Running Authentication Tests..."
pytest /app/tests/test_authentication.py -v --tb=short -m auth
sleep 65  # Wait for rate limit reset
echo ""

# Run authorization tests  
echo "2. Running Authorization Tests..."
mongosh --quiet --eval "db.getSiblingDB('test_database').users.deleteMany({})" > /dev/null 2>&1
pytest /app/tests/test_authorization.py -v --tb=short -m authz
sleep 65
echo ""

# Run JWT scope tests
echo "3. Running JWT Scope Validation Tests..."
mongosh --quiet --eval "db.getSiblingDB('test_database').users.deleteMany({})" > /dev/null 2>&1
pytest /app/tests/test_jwt_scopes.py -v --tb=short -m scope
sleep 65
echo ""

# Run schema validation tests
echo "4. Running Schema Validation Tests..."
mongosh --quiet --eval "db.getSiblingDB('test_database').users.deleteMany({})" > /dev/null 2>&1
pytest /app/tests/test_schema_validation.py -v --tb=short -m schema
sleep 10
echo ""

# Run rate limiting tests (these are designed to trigger rate limits)
echo "5. Running Rate Limiting Tests..."
mongosh --quiet --eval "db.getSiblingDB('test_database').users.deleteMany({})" > /dev/null 2>&1
pytest /app/tests/test_rate_limiting.py -v --tb=short -m rate_limit
echo ""

echo "================================================"
echo "Generating comprehensive HTML report..."
mongosh --quiet --eval "db.getSiblingDB('test_database').dropDatabase()" > /dev/null 2>&1
pytest /app/tests/ --html=/app/test_reports/complete_security_report.html --self-contained-html --tb=short
echo ""
echo "================================================"
echo "Test execution complete!"
echo "HTML Report: /app/test_reports/complete_security_report.html"
echo "================================================"
