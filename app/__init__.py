import sqlite3
import os
from flask import Flask, g
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Database
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(app.config['DATABASE'])
            db.row_factory = sqlite3.Row
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    # Pass get_db to the routes
    app.get_db = get_db

    # Initialize DB schema if it doesn't exist and run migrations
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            import os
            schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    db.cursor().executescript(f.read())
                db.commit()
                
        # Migrations (Auto-apply)
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, source TEXT NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, date DATE NOT NULL, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users (id));")
            
            cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, target_amount REAL NOT NULL, current_amount REAL DEFAULT 0, deadline DATE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users (id));")
            
            # Check if is_recurring exists in expenses
            cursor.execute("PRAGMA table_info(expenses);")
            columns = [col['name'] for col in cursor.fetchall()]
            if 'is_recurring' not in columns:
                cursor.execute("ALTER TABLE expenses ADD COLUMN is_recurring BOOLEAN DEFAULT 0;")
                cursor.execute("ALTER TABLE expenses ADD COLUMN recurring_freq TEXT;")
                cursor.execute("ALTER TABLE expenses ADD COLUMN is_subscription BOOLEAN DEFAULT 0;")
            
            db.commit()
        except Exception as e:
            print(f"Migration error: {e}")

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.expenses import expenses_bp
    from app.routes.income import income_bp
    from app.routes.goals import goals_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(api_bp)

    return app
