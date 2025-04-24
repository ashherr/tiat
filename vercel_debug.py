from flask import Flask, jsonify
import os
import sys
import traceback
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Simple root route to verify basic Flask functionality"""
    return "<h1>TIAT Debug Mode</h1><p>Basic Flask app is running. Check /debug for detailed diagnostics.</p>"

@app.route('/debug')
def debug():
    """Detailed diagnostics route"""
    try:
        # Collect environment information
        env_data = {
            "python_version": sys.version,
            "flask_version": Flask.__version__,
            "environment": "Production" if os.environ.get('VERCEL', False) else "Development",
            "available_env_vars": sorted(list(os.environ.keys())),
        }
        
        # Check for critical environment variables
        critical_vars = {
            "SUPABASE_URL": os.getenv('SUPABASE_URL', 'Not set'),
            "SUPABASE_KEY": os.getenv('SUPABASE_KEY', 'Not set') != 'Not set',
            "ENABLE_GCAL": os.getenv('ENABLE_GCAL', 'Not set'),
            "GOOGLE_CALENDAR_ID": os.getenv('GOOGLE_CALENDAR_ID', 'Not set'),
            "GOOGLE_SERVICE_ACCOUNT_EMAIL": os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL', 'Not set'),
            "GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY": bool(os.getenv('GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY')),
        }
        
        # Test imports that might fail
        import_tests = {}
        try:
            import flask_sqlalchemy
            import_tests["flask_sqlalchemy"] = "OK"
        except Exception as e:
            import_tests["flask_sqlalchemy"] = str(e)
            
        try:
            from google.oauth2 import service_account
            import_tests["google.oauth2"] = "OK"
        except Exception as e:
            import_tests["google.oauth2"] = str(e)
            
        try:
            import requests
            import_tests["requests"] = "OK"
        except Exception as e:
            import_tests["requests"] = str(e)
            
        # Test Google Calendar credential formation
        gcal_test = {}
        if os.getenv('ENABLE_GCAL', 'false').lower() == 'true':
            try:
                from google.oauth2 import service_account
                service_account_email = os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL')
                service_account_private_key = os.getenv('GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY')
                
                if service_account_email and service_account_private_key:
                    # Replace newline placeholders with actual newlines if needed
                    if "\\n" in service_account_private_key:
                        service_account_private_key = service_account_private_key.replace("\\n", "\n")
                    
                    # Create service account info dictionary
                    credentials_info = {
                        "type": "service_account",
                        "project_id": os.getenv('GOOGLE_PROJECT_ID', ''),
                        "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID', ''),
                        "private_key": service_account_private_key,
                        "client_email": service_account_email,
                        "client_id": os.getenv('GOOGLE_CLIENT_ID', ''),
                        "auth_uri": os.getenv('GOOGLE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
                        "token_uri": os.getenv('GOOGLE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
                        "auth_provider_x509_cert_url": os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URL', 'https://www.googleapis.com/oauth2/v1/certs'),
                        "client_x509_cert_url": os.getenv('GOOGLE_CLIENT_X509_CERT_URL', '')
                    }
                    
                    # Test credential creation
                    try:
                        credentials = service_account.Credentials.from_service_account_info(
                            credentials_info,
                            scopes=['https://www.googleapis.com/auth/calendar']
                        )
                        gcal_test["credentials"] = "OK"
                    except Exception as e:
                        gcal_test["credentials_error"] = str(e)
                        gcal_test["credentials_traceback"] = traceback.format_exc()
                else:
                    gcal_test["status"] = "Missing email or private key"
            except Exception as e:
                gcal_test["main_error"] = str(e)
                gcal_test["traceback"] = traceback.format_exc()
        else:
            gcal_test["status"] = "Google Calendar integration is disabled"
        
        # Combine all diagnostics
        result = {
            "env_data": env_data,
            "critical_vars": critical_vars,
            "import_tests": import_tests,
            "gcal_test": gcal_test
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 