import os

def replace_in_files(directory, old_string, new_string):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not (file_path[-5:] == ".html"):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # Выполняем замену строки
                new_content = file_content.replace(old_string, new_string)
                
                # Записываем изменения обратно в файл
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"Замена выполнена в файле: {file_path}")

            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {str(e)}")

if __name__ == "__main__":
    m = [
        "https://bootstrap5.ru/img/favicons/apple-touch-icon.png",
        "https://bootstrap5.ru/img/favicons/favicon-32x32.png",
        "https://bootstrap5.ru/img/favicons/favicon-16x16.png",
        "https://bootstrap5.ru/img/favicons/favicon.ico"
        ]
    for e in m:
        directory_path = "./"
        old_line = e
        new_line = "{{ url_for('static', filename='icon.png') }}"

        replace_in_files(directory_path, old_line, new_line)
