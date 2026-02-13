import app

def test_message_is_correct():
    """Проверяем, что приложение возвращает правильную фразу"""
    expected = "Hello from Docker! The application is running successfully."
    assert app.get_message() == expected
    