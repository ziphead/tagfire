# tagfire
Tag wrapping tool for django html templates. 
Give it your django app name and it will look and modify all your html templates recursively in <your_app>/templates folder:

1)Wraps text and alt=""  with Django's {% trans 'Your text' %} tag.

2)Finds all href/img/src tags and wraps its content with {% static 'your_local_link' %}.
Doesn't wrap http/https links. Only (jpg/png/svg/gif/css/js) files.

### Installation
  -put the file in <your_app>\management\commands directory.
 ```sh
 python manage.py tagifire <app_name1> <app_name2>
 ```
  
