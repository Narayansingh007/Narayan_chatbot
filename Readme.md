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

## Attach Screenshot

<img src="./ss/Screenshot 2024-12-12 181528.png">