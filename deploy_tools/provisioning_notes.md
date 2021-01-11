# Обеспечение работы нового сайта  

==================================================================
## Необходимые пакеты
* nginx
* Python 3.8
* Django 3.1.2
* virtualenv + pip
* Git

Например, в Ubuntu:  
`apt install software-properties-common`    
`add-apt-repository ppa:deadsnakes/ppa`   
`apt install python3.8 python3.8-venv git nginx`  
## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME на доменное имя
* `export $SITENAME=name_your_site`
* `cp nginx.template.conf /etc/nginx/sites-available/$SITENAME`
* `sudo ln -s /etc/nginx/sites-avaliable/$SITENAME /etc/nginx/sites-enabled/$SITENAME`
* `sudo rm /etc/nginx/sites-enabled/default`
* `sudo systemctl reload nginx`

## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME на ваш сайт
* `cp gunicorn-systemd.template.service /etc/systemd/system/gunicorn-YOUR_SITE.service`
* `sudo systemctl daemon-reload`
* `sudo systemctl enable gunicorn-YOUR_SITE`
* `sudo systemctl start gunicorn-YOUR_SITE`

## Стуктура папок
/home/username
--- sites
    |--- SITENAME
        |--- database
        |--- source
        |--- static
        |--- virtualenv
