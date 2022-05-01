from flask import Flask


from pasta_user.user import user_blueprint
from pasta_executor.executor import executor_blueprint


app = Flask(__name__)

app.register_blueprint(user_blueprint)
app.register_blueprint(executor_blueprint)

if __name__ == "__main__":
    app.run(debug=True)