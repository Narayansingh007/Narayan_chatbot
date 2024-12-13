# API Response Time and Static Data Documentation

## Overview
This document provides details about the performance and response behavior when testing the API endpoint using **Postman**. The purpose of this test was to measure the response time and assess the type of data returned from the API.

## Test Setup

- **API Endpoint Tested**: `/sale_script`
- **Test Tool Used**: Postman
- **Date of Test**: `12/12/2024`
- **Response Format**: String (Hardcoded)

## Test Details

- **Request Method**: `POST`
- **Headers Used**:
  - `Content-Type`: `application/json`
  - `x-access-token`: `Token` *(Replace with the actual token used)*
- **Body Data**: 
```json
{
  "history": [
    {
      "role": "user",
      "content": "Hi. I'm Scott from Freedom Property Investors. We're excited to share some amazing property investment opportunities! Are you interested in learning more about property investment strategies and our masterclass?"
    }
  ]
}
```

## Test Details

- **Time Taken for Response**: 5.56 seconds
- **Type of Data Returned**: Static Data

### Sample Response
String

- **Date of Test**: `13/12/2024`
In this update, the following changes have been made:

1. **`app.py`**:
   - Improved the JWT token validation and OpenAI integration.
   - Configured global JWT token and OpenAI API key.
   
2. **`processing.py`**:
   - Added global JWT token and OpenAI API key configurations.

3. **`utils.py`**:
   - Added JWT token validation logic to check whether the token is valid or invalid.

4. **`config.py`**:
   - Configured the JWT token and OpenAI API key in this file to be imported into other files as needed.

### Key Updates:
- **JWT Token Validation**: The app now validates the **JWT_SECRET_KEY** to ensure only authorized users can interact with the chatbot.
- **OpenAI Key Configuration**: The **OPENAI_API_KEY** has been centralized in the `config.py` file for easier management.


