# Docker MongoDB Setup Guide

This guide explains how to set up MongoDB in a Docker container with persistent storage for the misinformation detection system.

## Quick Start

### 1. Start MongoDB Container

```bash
docker-compose up -d
```

This will:
- Pull the MongoDB 7.0 image (if not already present)
- Create a container named `misinformation_mongodb`
- Set up persistent volumes for data storage
- Expose MongoDB on port 27017
- Initialize the database with indexes

### 2. Verify MongoDB is Running

```bash
docker-compose ps
```

You should see the `misinformation_mongodb` container running.

### 3. Check MongoDB Logs

```bash
docker-compose logs mongodb
```

### 4. Connect to MongoDB

Using MongoDB Shell (mongosh):
```bash
docker exec -it misinformation_mongodb mongosh
```

Or using MongoDB Compass:
- Connection string: `mongodb://localhost:27017`
- Or with auth: `mongodb://admin:changeme@localhost:27017`

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

**Option 1: Without Authentication (Development)**
```bash
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=misinformation_detection

# Leave MONGO_ROOT_USERNAME and MONGO_ROOT_PASSWORD unset
```

**Option 2: With Authentication (Recommended)**
```bash
# MongoDB Configuration
MONGODB_URL=mongodb://admin:changeme@localhost:27017/misinformation_detection?authSource=admin
MONGODB_DB_NAME=misinformation_detection

# MongoDB Docker Configuration
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=changeme
```

### Persistent Storage

Data is stored in Docker volumes:
- `mongodb_data`: Main database data
- `mongodb_config`: MongoDB configuration

**Volume locations:**
- Linux: `/var/lib/docker/volumes/mumbaihacks2025_mongodb_data`
- Mac/Windows: Managed by Docker Desktop

### Port Configuration

MongoDB is exposed on port `27017` by default. To change it, modify `docker-compose.yml`:

```yaml
ports:
  - "27018:27017"  # Use 27018 on host
```

## Common Operations

### Start MongoDB

```bash
docker-compose up -d
```

### Stop MongoDB (keeps data)

```bash
docker-compose stop
```

### Stop and Remove Container (keeps data)

```bash
docker-compose down
```

### Stop and Remove Everything (including data)

```bash
docker-compose down -v
```

**Warning**: This will delete all your data!

### View Logs

```bash
docker-compose logs -f mongodb
```

### Access MongoDB Shell

```bash
docker exec -it misinformation_mongodb mongosh
```

### Backup Database

```bash
docker exec misinformation_mongodb mongodump --out /data/backup
docker cp misinformation_mongodb:/data/backup ./backup
```

### Restore Database

```bash
docker cp ./backup misinformation_mongodb:/data/backup
docker exec misinformation_mongodb mongorestore /data/backup
```

## Connection Strings

### Without Authentication (Development)

```python
MONGODB_URL=mongodb://localhost:27017
```

**To disable authentication**: Don't set `MONGO_ROOT_USERNAME` and `MONGO_ROOT_PASSWORD` in your `.env` file.

### With Authentication (Recommended)

```python
MONGODB_URL=mongodb://admin:changeme@localhost:27017/misinformation_detection?authSource=admin
```

**To enable authentication**: Set `MONGO_ROOT_USERNAME` and `MONGO_ROOT_PASSWORD` in your `.env` file.

### From Application Code

The application automatically uses the `MONGODB_URL` environment variable:

```python
from app.dependencies import get_mongo_client

client = get_mongo_client()
# Connects to MongoDB using MONGODB_URL from .env
```

## Database Initialization

The database is automatically initialized with:
- Database: `misinformation_detection`
- Collection: `datapoints`
- Indexes on: id, published_at, ingested_at, source_type, cluster_id, etc.
- Text index on: title, content

Initialization scripts are in `docker/mongo-init/`.

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs mongodb
```

**Common issues:**
- Port 27017 already in use: Change port in `docker-compose.yml`
- Permission errors: Check Docker volume permissions

### Can't Connect to MongoDB

**Verify container is running:**
```bash
docker-compose ps
```

**Test connection:**
```bash
docker exec -it misinformation_mongodb mongosh --eval "db.adminCommand('ping')"
```

### Data Not Persisting

**Check volumes:**
```bash
docker volume ls
docker volume inspect mumbaihacks2025_mongodb_data
```

**Verify data directory:**
```bash
docker exec misinformation_mongodb ls -la /data/db
```

### Reset Database

**Remove container and volumes:**
```bash
docker-compose down -v
docker-compose up -d
```

This will recreate everything from scratch.

## Production Considerations

For production use, consider:

1. **Stronger Authentication:**
   - Use strong passwords
   - Create application-specific users
   - Enable MongoDB authentication

2. **Network Security:**
   - Don't expose MongoDB port publicly
   - Use Docker networks
   - Consider MongoDB Atlas for managed hosting

3. **Backup Strategy:**
   - Regular automated backups
   - Test restore procedures
   - Store backups off-container

4. **Resource Limits:**
   Add to `docker-compose.yml`:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
   ```

5. **MongoDB Configuration:**
   - Tune WiredTiger cache
   - Configure replication for high availability
   - Set up monitoring

## Integration with Application

The application is already configured to use this MongoDB setup:

1. Set `MONGODB_URL` in `.env`
2. Start MongoDB: `docker-compose up -d`
3. Run your application - it will connect automatically

```python
# app/dependencies.py automatically uses MONGODB_URL
from app.dependencies import get_storage_service

storage = get_storage_service()
# Ready to use!
```

## Volume Management

### List Volumes

```bash
docker volume ls | grep mongodb
```

### Inspect Volume

```bash
docker volume inspect mumbaihacks2025_mongodb_data
```

### Remove Volume (careful!)

```bash
docker volume rm mumbaihacks2025_mongodb_data
```

## Health Check

The container includes a health check that verifies MongoDB is responding:

```bash
docker inspect misinformation_mongodb | grep -A 10 Health
```

## Next Steps

1. Start MongoDB: `docker-compose up -d`
2. Verify connection: `docker-compose ps`
3. Test with application: Run ingestion tests
4. Monitor logs: `docker-compose logs -f mongodb`

For more information, see:
- [MongoDB Docker Hub](https://hub.docker.com/_/mongo)
- [MongoDB Documentation](https://docs.mongodb.com/)

