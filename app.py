from flask import Flask, render_template, request, jsonify
import math
import re

app = Flask(__name__)

def safe_eval(expression):
    """Безопасное вычисление математических выражений"""
    try:
        print(f"Вычисляем: {expression}")
        
        # Заменяем запятые на точки для десятичных чисел
        expression = expression.replace(',', '.')
        print(f"После замены запятых: {expression}")
        
        # Заменяем специальные математические функции и символы
        expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
        expression = expression.replace('^', '**')
        print(f"После замены операторов: {expression}")
        
        # Обработка процентов - заменяем 50% на (50/100)
        expression = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expression)
        print(f"После обработки процентов: {expression}")
        
        # Обработка математических функций
        expression = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', expression)
        expression = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expression)
        expression = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expression)
        expression = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expression)
        expression = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expression)
        expression = re.sub(r'ln\(([^)]+)\)', r'math.log(\1)', expression)
        print(f"После обработки функций: {expression}")
        
        # Удаляем все пробелы
        expression = expression.replace(' ', '')
        print(f"После удаления пробелов: {expression}")
        
        # Проверяем на безопасные символы
        allowed_chars = set('0123456789+-*/.()abcdefghijklmnopqrstuvwxyz')
        if any(char not in allowed_chars for char in expression.lower()):
            return "Ошибка: Недопустимые символы"
        
        # Вычисляем выражение
        result = eval(expression, {"__builtins__": None}, {"math": math})
        print(f"Результат вычисления: {result}")
        
        # Форматируем результат
        if result == int(result):
            final_result = str(int(result))
        else:
            final_result = f"{result:.10f}".rstrip('0').rstrip('.').replace('.', ',')
        
        print(f"Финальный результат: {final_result}")
        return final_result
            
    except ZeroDivisionError:
        return "Ошибка: Деление на ноль"
    except Exception as e:
        print(f"Ошибка при вычислении: {str(e)}")
        return f"Ошибка: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        print(f"Полученные данные: {data}")
        
        if not data:
            return jsonify({'result': 'Ошибка: Нет данных'})
        
        expression = data.get('expression', '')
        print(f"Выражение для вычисления: '{expression}'")
        
        if not expression:
            return jsonify({'result': '0'})
        
        result = safe_eval(expression)
        print(f"Возвращаем результат: {result}")
        
        return jsonify({'result': result})
    
    except Exception as e:
        print(f"Ошибка в /calculate: {str(e)}")
        return jsonify({'result': f'Ошибка сервера: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)