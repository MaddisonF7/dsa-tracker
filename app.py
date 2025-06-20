# Import os
import os
# Import create_app function from init.py
from init import create_app

# Set Flask instance from create_app
app = create_app()

# Runs create_app Flask application only on file execution
if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=port)
