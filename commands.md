### Redis Server Setup


#### Start Redis Server
```bash
wsl
redis-server  
```
##### or
```bash
sudo service redis-server start
```

#### Access Redis CLI
```bash
redis-cli
```

### Celery Commands
#### Start Celery Worker
```bash
celery -A proj_name worker -l info
```

#### Start Celery Beat
```bash
celery -A proj_name beat -l info
```

#### Monitor Celery Worker and Beat
```bash
flower -A proj_name
```


```bash
celery -A proj_name worker -l info --pool=solo
```


