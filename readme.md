Установка:
conda env create -f environment.yml
sudo apt-get install rabbitmq-server


Запуск:
в 1 терминале:
    sudo service rabbitmq-server start
    celery -A tasks worker --loglevel=info
в 2 терминале:
    python3 app.py