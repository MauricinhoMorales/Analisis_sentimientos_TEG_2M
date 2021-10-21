CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS [dbo].[tweets] (
	tweet_id uuid PRIMARY KEY DEFAULT UUID_GENERATE_V4(), 
	tweet_date VARCHAR (50) NOT NULL,
	tweet_username VARCHAR ( 50 ) NOT NULL,
	tweet VARCHAR (500) NOT NULL,
	tweet_translate VARCHAR (500),
	tweet_sentiment VARCHAR (50) NOT NULL,
	tweet_opinion VARCHAR (50) NOT NULL
);

INSERT INTO tweets (tweet_date, tweet_username,tweet,tweet_translate,tweet_sentiment,tweet_opinion)
VALUES ('10/3/2021','yocsinm','Si no vas a hacer nada por tu pais mejor vete','If you are not going to do anything for your country, you better leave.','ira','en contra');

SELECT * FROM tweets