
# BEHEMOH

A project to help analyze the demand for small businesses in catering.

### Data 

As an example of the work, three residential complexes of the Murino and Devyatkino districts were taken.

Residential complex DREAM

https://drive.google.com/file/d/1F6E_UHSyxzQVCkcSdxDN22uzNXqyzO_V/view ;

https://drive.google.com/file/d/1-J72CTRw-MLc7kO4Ho9cVPj1QSvo6f0J/view - 200;
...


### Сamera data source
http://www.cactus.tv

### Data-driven scheme 

![](/gifs/interests.png)
![](/gifs/camera.png)


### Client (Инструкция по запуску клиента и сервера)
Переходим в папку server, тянем зависимость и запускаем
cd server && pip install -U flask-cors && python main.py

Переходим в корень проекта и устанавливаем express как веб-сервер для клиента
cd ../
npm install

Запускаем клиент
node index.js