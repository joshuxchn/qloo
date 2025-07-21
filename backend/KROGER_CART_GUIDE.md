# Kroger Cart API Integration Guide

## Overview

This integration provides seamless access to Kroger's Cart API, allowing users to add items to their Kroger cart programmatically. The system implements **persistent authentication** with automatic token refresh, meaning users only need to authorize once.

## Architecture

### Core Components

1. **`kroger.py`** - Main KrogerAPI class with all functionality
2. **`test_kroger.py`** - Test interface with direct method imports
3. **`kroger_tokens.json`** - Persistent token storage
4. **`.env`** - Configuration and credentials

## Authentication Flow

### OAuth2 Authorization Code Grant with PKCE

The Kroger Cart API uses OAuth2 Authorization Code flow for secure user authentication:

```
User → Browser → Kroger Login → Authorization → Access Token → Cart Access
```

### Token Types

1. **Access Token**
   - **Purpose**: Authenticates cart API requests
   - **Duration**: 30 minutes (1800 seconds)
   - **Usage**: Bearer token in Authorization header
   - **Auto-refresh**: Yes, using refresh token

2. **Refresh Token**
   - **Purpose**: Obtains new access tokens without re-authorization
   - **Duration**: Extended (weeks/months)
   - **Usage**: Automatic background refresh
   - **Storage**: Persistent in `kroger_tokens.json`

## Detailed Function Documentation

### Core API Methods

#### `getAuthorizationUrl(scopes, state)`
```python
def getAuthorizationUrl(scopes="cart.basic:write profile.compact", state="auth_state"):
```

**Purpose**: Generates OAuth2 authorization URL for user consent

**Process**:
1. Constructs authorization URL with required parameters
2. Includes client_id, redirect_uri, scopes, and CSRF state
3. Returns URL for browser-based user authentication

**Parameters**:
- `scopes`: OAuth permissions (default: cart write + profile read)
- `state`: CSRF protection token

**Returns**: Full authorization URL string

**Example**:
```python
auth_url = kroger.getAuthorizationUrl()
# Returns: https://api.kroger.com/v1/connect/oauth2/authorize?scope=cart.basic:write+profile.compact&response_type=code&client_id=...
```

#### `exchangeAuthCode(authorization_code)`
```python
def exchangeAuthCode(authorization_code):
```

**Purpose**: Exchanges authorization code for access and refresh tokens

**Process**:
1. Sends POST request to token endpoint with authorization code
2. Includes client credentials in Authorization header (Basic auth)
3. Calculates token expiration timestamp
4. Saves tokens to `kroger_tokens.json`

**Security**: Uses client_id:client_secret Basic authentication

**Token Storage Format**:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "BgafSulyQ-IyYQwcw2KP...",
  "token_type": "bearer",
  "expires_in": 1800,
  "expires_at": 1753142060.280598
}
```

#### `addToCart(upc, quantity, modality)`
```python
def addToCart(upc, quantity=1, modality="PICKUP"):
```

**Purpose**: Adds items to user's Kroger cart

**Process**:
1. Calls `_get_valid_token()` for current access token
2. Auto-refreshes token if expired
3. Sends PUT request to cart endpoint with item details
4. Handles authentication and API errors

**Parameters**:
- `upc`: Product UPC code (string)
- `quantity`: Number of items (integer, default: 1)
- `modality`: Fulfillment method ("PICKUP" or "DELIVERY")

**API Endpoint**: `PUT /v1/cart/add`

**Request Format**:
```json
{
  "items": [
    {
      "upc": "0001111042850",
      "quantity": 1,
      "modality": "PICKUP"
    }
  ]
}
```

**Success Response**: HTTP 204 No Content

### Token Management Methods

#### `_get_valid_token()`
```python
def _get_valid_token():
```

**Purpose**: Returns valid access token, auto-refreshing if necessary

**Logic**:
1. Reads current token from `kroger_tokens.json`
2. Checks expiration with 5-minute buffer
3. Calls `_refresh_token()` if expired
4. Returns fresh access token

**Expiration Check**:
```python
current_time = time.time()
if current_time >= (expires_at - 300):  # 5-minute buffer
    # Refresh token
```

#### `_refresh_token()`
```python
def _refresh_token():
```

**Purpose**: Obtains new access token using refresh token

**Process**:
1. Reads refresh token from storage
2. Sends POST request with `grant_type=refresh_token`
3. Updates token file with new access token
4. Preserves refresh token if not returned in response

**API Request**:
```
POST /v1/connect/oauth2/token
Authorization: Basic {base64(client_id:client_secret)}
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token={refresh_token}
```

## Usage Workflows

### One-Time Setup (Required Once)

```python
from test_kroger import getAuthorizationUrl, exchangeAuthCode

# Step 1: Get authorization URL
auth_url = getAuthorizationUrl()
print(auth_url)

# Step 2: User visits URL, logs in, authorizes app
# Browser redirects to: http://localhost:8080/callback?code=AUTHORIZATION_CODE

# Step 3: Extract code and exchange for tokens
authorization_code = "AUTHORIZATION_CODE_FROM_REDIRECT"
token_info = exchangeAuthCode(authorization_code)

# Tokens now saved - no further authorization needed!
```

### Ongoing Cart Operations (Seamless)

```python
from test_kroger import addToCart, productSearch

# Search for products (no auth required)
productSearch("milk", 3)

# Add items to cart (auto-handles token refresh)
addToCart("0001111042850", 1, "PICKUP")     # Milk for pickup
addToCart("0001111008485", 2, "DELIVERY")   # Bread for delivery
addToCart("0007225003706", 1, "PICKUP")     # More items...

# All operations work seamlessly without re-authorization
```

### Error Handling and Recovery

```python
# If refresh token expires (rare), re-authorization required
success = addToCart("0001111042850", 1, "PICKUP")
if not success:
    # Check error - may need re-authorization
    auth_url = getAuthorizationUrl()
    # Repeat authorization process
```

## File Structure and Storage

### Token Storage (`kroger_tokens.json`)

**Location**: `/backend/kroger_tokens.json`

**Format**:
```json
{
  "access_token": "JWT_ACCESS_TOKEN",
  "refresh_token": "REFRESH_TOKEN_STRING", 
  "token_type": "bearer",
  "expires_in": 1800,
  "expires_at": 1753142060.280598
}
```

**Security Considerations**:
- Contains sensitive authentication data
- Should be in `.gitignore` for production
- Consider encryption for production deployments
- File permissions should be restricted

### Environment Configuration (`.env`)

**Required Variables**:
```env
KROGER_CLIENT_ID=your_client_id
KROGER_CLIENT_SECRET=your_client_secret
KROGER_REDIRECT_URI=http://localhost:8080/callback
ZIP_CODE=98075
```

**Setup Requirements**:
1. Register application at https://developer.kroger.com/
2. Configure redirect URI in Kroger developer console
3. Obtain client_id and client_secret
4. Set environment variables

## API Endpoints and Specifications

### Authorization Endpoint
```
GET https://api.kroger.com/v1/connect/oauth2/authorize
```

**Parameters**:
- `scope`: cart.basic:write profile.compact
- `response_type`: code
- `client_id`: Your application client ID
- `redirect_uri`: Registered redirect URI
- `state`: CSRF protection token

### Token Endpoint
```
POST https://api.kroger.com/v1/connect/oauth2/token
```

**Headers**:
- `Authorization`: Basic {base64(client_id:client_secret)}
- `Content-Type`: application/x-www-form-urlencoded

**Grant Types**:
1. **Authorization Code**: `grant_type=authorization_code`
2. **Refresh Token**: `grant_type=refresh_token`

### Cart Add Endpoint
```
PUT https://api.kroger.com/v1/cart/add
```

**Headers**:
- `Authorization`: Bearer {access_token}
- `Content-Type`: application/json

**Request Body**:
```json
{
  "items": [
    {
      "upc": "product_upc_code",
      "quantity": integer,
      "modality": "PICKUP|DELIVERY"
    }
  ]
}
```

## Error Handling

### Common Error Scenarios

1. **401 Unauthorized**
   - **Cause**: Expired or invalid access token
   - **Handling**: Automatic token refresh
   - **Fallback**: Re-authorization if refresh fails

2. **403 Forbidden** 
   - **Cause**: Insufficient scopes or permissions
   - **Handling**: Check scope configuration
   - **Solution**: Re-authorize with correct scopes

3. **404 Not Found**
   - **Cause**: Invalid UPC code
   - **Handling**: Validate UPC before adding to cart
   - **Solution**: Use product search to get valid UPCs

4. **429 Too Many Requests**
   - **Cause**: Rate limiting (5,000 calls/day)
   - **Handling**: Implement request throttling
   - **Solution**: Add delays between requests

### Token Expiration Handling

```python
def _get_valid_token(self):
    # Load current token
    token_info = load_token()
    
    # Check expiration (5-minute buffer)
    if current_time >= (expires_at - 300):
        if self._refresh_token():
            # Success: return new token
            return new_access_token
        else:
            # Failure: need re-authorization
            return None
    
    return current_access_token
```

## Testing and Development

### Test Functions Available

```python
# Product search (no auth required)
test_product_search()

# One-time authorization setup
test_cart_authorization()
test_cart_token_exchange("auth_code")

# Cart operations (persistent auth)
test_add_to_cart("upc", quantity, "modality")
quick_cart_test()

# Complete workflow
full_workflow()
```

### Development Tips

1. **First-time Setup**: Run `test_cart_authorization()` once
2. **Daily Usage**: Use `addToCart()` directly - no setup needed
3. **Testing**: Use `quick_cart_test()` to verify cart access
4. **Debugging**: Check `kroger_tokens.json` for token status

## Security Best Practices

### Development Environment
- Use localhost redirect URI for testing
- Store credentials in `.env` file
- Add `kroger_tokens.json` to `.gitignore`

### Production Environment
- Use HTTPS redirect URI
- Encrypt token storage
- Implement secure credential management
- Monitor token refresh patterns
- Set up proper logging and alerting

### Token Security
- Never log access tokens
- Implement secure token storage
- Use proper file permissions
- Consider token encryption
- Monitor for unauthorized access

## Integration with Grocery Platform

### Recommended Usage Pattern

```python
class GroceryOptimizer:
    def __init__(self):
        self.kroger = KrogerAPI()
    
    def add_optimized_list_to_cart(self, grocery_list):
        """Add optimized grocery list to Kroger cart"""
        for item in grocery_list:
            upc = item['upc']
            quantity = item['quantity'] 
            modality = item.get('modality', 'PICKUP')
            
            success = self.kroger.addToCart(upc, quantity, modality)
            if not success:
                # Handle error - log, retry, or alert user
                self.handle_cart_error(item)
    
    def handle_cart_error(self, item):
        # Implement error handling strategy
        pass
```

This integration provides robust, persistent cart access that scales from development to production deployment.