// MongoDB initialization script
// This script runs when the container is first created

// Switch to the target database
db = db.getSiblingDB('misinformation_detection');

// Create collections with validation schemas (optional)
db.createCollection('datapoints', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['id', 'source_type', 'title', 'content', 'published_at'],
      properties: {
        id: {
          bsonType: 'string',
          description: 'Unique identifier for the datapoint'
        },
        source_type: {
          bsonType: 'string',
          enum: ['rss', 'tavily'],
          description: 'Source type of the datapoint'
        },
        title: {
          bsonType: 'string',
          description: 'Title of the article/datapoint'
        },
        content: {
          bsonType: 'string',
          description: 'Content of the article/datapoint'
        },
        published_at: {
          bsonType: 'date',
          description: 'Publication timestamp'
        },
        embedding: {
          bsonType: 'array',
          items: {
            bsonType: 'double'
          },
          description: 'Vector embedding for the datapoint'
        }
      }
    }
  }
});

// Create indexes for efficient queries
db.datapoints.createIndex({ "id": 1 }, { unique: true });
db.datapoints.createIndex({ "published_at": 1 });
db.datapoints.createIndex({ "ingested_at": 1 });
db.datapoints.createIndex({ "source_type": 1 });
db.datapoints.createIndex({ "source_name": 1 });
db.datapoints.createIndex({ "processed": 1 });
db.datapoints.createIndex({ "clustered": 1 });
db.datapoints.createIndex({ "cluster_id": 1 });
db.datapoints.createIndex({ "title": "text", "content": "text" });

// Create a user for the application (optional, if using auth)
// db.createUser({
//   user: 'app_user',
//   pwd: 'app_password',
//   roles: [
//     {
//       role: 'readWrite',
//       db: 'misinformation_detection'
//     }
//   ]
// });

print('Database initialized successfully!');

