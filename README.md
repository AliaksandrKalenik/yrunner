# yrunner

### Installation:
  `pip install -Ur requirements.txt`

### Run:
  `./manage.py runserver` # run server
  
  `celery worker -A yrunner --loglevel=INFO` # run celery

## HEROKU:
  
### Preparations:
    1. Create Heroku project
    
    2. Add Heroku add-ons:
      - database (Heroku PostgreSQL)
      - Heroku rabbitMQ
      
    3. Set ENVIRONMENT VARIABLE in heroku admin panel:
      DJANGO_SETTINGS_MODULE=yrunner.heroku_settings
      
    4. Enable dyno resources in heroku admin panel: 
      - web
      - worker
